from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from event.models import Event
from schooladmin.common import paginator

from ..models import Person


@login_required
@permission_required("event.view_event")
def frequency_ps_list(request, person_id):
    person = get_object_or_404(Person, id=person_id)

    queryset = person.event_set.all()

    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object_list": object_list,
        "title": "frequencies list",
        "person": person,  # to header element
    }
    return render(request, "person/frequency_list.html", context)


@login_required
@permission_required("person.change_person")
def frequency_ps_insert(request, person_id):
    person = get_object_or_404(Person, id=person_id)

    if request.GET.get("pk"):
        event = get_object_or_404(Event, pk=request.GET.get("pk"))

        if request.method == "POST":
            person.event_set.add(event)
            messages.success(request, "The Frequency has been inserted!")
            return redirect("frequency_ps_list", person_id=person_id)

        context = {
            "person": person,
            "insert_to": f"{event.activity.name} {event.center}",
            "title": "confirm to insert",
        }
        return render(
            request, "person/elements/confirm_to_insert.html", context
        )

    date = (
        datetime.strptime(request.GET.get("date"), "%Y-%m-%d")
        if request.GET.get("date")
        else timezone.now()
    )
    _query = [
        Q(date=date),
        Q(is_active=True),
        Q(center=request.user.person.center),
    ]

    if request.GET.get("d30"):
        _query.remove(Q(date=date))
        if request.GET.get("lastNext") == "last":
            _query.append(Q(date__range=[date - timedelta(30), date]))
        else:
            _query.append(Q(date__range=[date, date + timedelta(30)]))
    if request.GET.get("all"):
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))

    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    queryset = Event.objects.filter(query).order_by("-date")

    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object_list": object_list,
        "title": "insert frequencies",
        "person": person,  # to header element
        "date": date.strftime("%Y-%m-%d"),
        "all": True if request.GET.get("all") else False,
        "d30": True if request.GET.get("d30") else False,
        "lastNext": "last"
        if request.GET.get("lastNext") == "last"
        else "next",
    }
    return render(request, "person/frequency_insert.html", context)


@login_required
@permission_required("person.change_person")
def frequency_ps_delete(request, person_id, event_id):
    person = get_object_or_404(Person, id=person_id)
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        person.event_set.remove(event)
        messages.success(request, "The Frequency has been removed!")
        return redirect("frequency_ps_list", person_id=person_id)

    context = {
        "person": person,
        "event": event,
        "title": "confirm to delete",
    }
    return render(
        request, "person/elements/confirm_to_delete_freq.html", context
    )

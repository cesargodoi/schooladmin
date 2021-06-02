from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from event.models import Event
from base.searchs import event_search
from schooladmin.common import paginator, ACTIVITY_TYPES

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
        "person": person,  # to header element,
        "tab": "frequencies",
    }
    return render(request, "person/person_detail.html", context)


@login_required
@permission_required("person.change_person")
def frequency_ps_insert(request, person_id):
    person = Person.objects.get(id=person_id)

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

    queryset, page = event_search(request, Event)
    object_list = paginator(queryset, page=page)

    context = {
        "object_list": object_list,
        "title": "insert frequencies",
        "person": person,  # to header element
        "type_list": ACTIVITY_TYPES,
        "pre_freqs": [
            person.event.pk for person in person.frequency_set.all()
        ],
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

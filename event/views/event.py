import os
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from schooladmin.common import paginator

from ..forms import EventForm
from ..models import Event


@login_required
@permission_required("event.view_event")
def event_home(request):
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
    if request.GET.get("act_type"):
        _query.append(Q(activity__activity_type=request.GET.get("act_type")))
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
        "title": "event home",
        "date": date.strftime("%Y-%m-%d"),
        "all": True if request.GET.get("all") else False,
        "d30": True if request.GET.get("d30") else False,
        "lastNext": "last"
        if request.GET.get("lastNext") == "last"
        else "next",
    }
    return render(request, "event/event_home.html", context)


@login_required
@permission_required("event.view_event")
def event_detail(request, pk):
    object = get_object_or_404(Event, pk=pk)

    queryset = object.frequencies.all().order_by("name_sa")

    object_list = paginator(queryset, 25, request.GET.get("page"))

    context = {
        "object": object,
        "object_list": object_list,
        "title": "event detail",
    }
    return render(request, "event/event_detail.html", context)


@login_required
@permission_required("event.add_event")
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            message = "The Event has been created!"
            messages.success(request, message)
            return redirect(reverse("event_home") + "?d30=on&lastNext=last")

    context = {
        "form": EventForm(initial={"made_by": request.user}),
        "to_create": True,
    }
    return render(request, "event/event_form.html", context)


@login_required
@permission_required("event.change_event")
def event_update(request, pk):
    object = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            message = "The Event has been updated!"
            messages.success(request, message)
            return redirect("event_detail", pk=pk)

    context = {
        "form": EventForm(instance=object),
        "pk": pk,
    }
    return render(request, "event/event_form.html", context)


@login_required
@permission_required("event.delete_event")
def event_delete(request, pk):
    object = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        os.remove(object.qr_code.path)
        object.delete()
        message = "The Event has been deleted!"
        messages.success(request, message)
        return redirect("event_home")

    context = {
        "object": object,
        "title": "confirm to delete",
    }
    return render(request, "base/confirm_delete.html", context)

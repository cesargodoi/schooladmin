from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from schooladmin.common import paginator
from django.urls import reverse
from django.utils import timezone

from center.models import Center
from base.searchs import search_seeker, search_lecture

from ..forms import ListenerForm
from ..models import Lecture, Seeker, Listener, Historic_of_seeker


@login_required
@permission_required("publicwork.add_listener")
def add_listener(request, lect_pk):
    lecture = Lecture.objects.get(pk=lect_pk)

    if request.GET.get("seek_pk"):
        seeker = Seeker.objects.get(pk=request.GET["seek_pk"])

        if request.method == "POST":
            # isert historic if necessary
            if seeker.historic_of_seeker_set.last().occurrence in [
                "NEW",
                "MT1",
            ]:
                insert_historic_if_necessary(request, seeker)
            # create listener
            Listener.objects.create(
                lecture=lecture,
                seeker=seeker,
                ranking=int(request.POST["ranking"]),
                observations=request.POST["observations"],
            )
            messages.success(
                request, "The seeker has been inserted on lecture!"
            )
            return redirect("lecture_detail", pk=lect_pk)

        context = {
            "seeker": seeker,
            "form": ListenerForm,
            "insert_to": f"{lecture.theme} {lecture.center}",
            "title": "confirm to insert",
        }
        return render(
            request,
            "publicwork/elements/confirm_add_listener.html",
            context,
        )

    queryset, page = search_seeker(request, Seeker)
    object_list = paginator(queryset, page=page)

    context = {
        "object_list": object_list,
        "pre_listeners": [seek.pk for seek in lecture.listeners.all()],
        "title": "add listener",
        "object": lecture,
        "centers": [[str(cnt.pk), str(cnt)] for cnt in Center.objects.all()],
    }
    return render(request, "publicwork/listener_add.html", context)


@login_required
@permission_required("publicwork.change_listener")
def update_listener(request, lect_pk, lstn_pk):
    listener = Listener.objects.get(pk=lstn_pk)

    if request.method == "POST":
        listener.ranking = int(request.POST["ranking"])
        listener.observations = request.POST["observations"]
        listener.save()
        messages.success(request, "The Listener has been updated!")

        return redirect("lecture_detail", pk=lect_pk)

    context = {
        "form": ListenerForm(instance=listener),
        "title": "update listener",
        "listener": listener,
        "object": listener.lecture,
    }
    return render(request, "publicwork/listener_update.html", context)


@login_required
@permission_required("publicwork.delete_listener")
def remove_listener(request, lect_pk, lstn_pk):
    listener = Listener.objects.get(pk=lstn_pk)

    if request.method == "POST":
        listener.delete()
        return redirect("lecture_detail", pk=lect_pk)

    context = {"object": listener, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


# from seeker side
@login_required
@permission_required("publicwork.add_listener")
def add_frequency(request, pk):
    seeker = Seeker.objects.get(pk=pk)

    if request.GET.get("lect_pk"):
        lecture = Lecture.objects.get(pk=request.GET["lect_pk"])

        if request.method == "POST":
            # isert historic if necessary
            if seeker.historic_of_seeker_set.last().occurrence in [
                "NEW",
                "MT1",
            ]:
                insert_historic_if_necessary(request, seeker)
            # create listener
            Listener.objects.create(
                lecture=lecture,
                seeker=seeker,
                ranking=int(request.POST["ranking"]),
                observations=request.POST["observations"],
            )
            messages.success(
                request, "The seeker has been inserted on lecture!"
            )
            return redirect("seeker_frequencies", pk=pk)

        context = {
            "seeker": seeker,
            "form": ListenerForm,
            "insert_to": f"{lecture.theme} - {lecture.center}",
            "title": "confirm to insert",
        }
        return render(
            request,
            "publicwork/elements/confirm_add_listener.html",
            context,
        )

    queryset, page = search_lecture(request, Lecture)
    object_list = paginator(queryset, page=page)

    context = {
        "object": seeker,
        "object_list": object_list,
        "title": "add frequency",
        "pre_freqs": [lect.pk for lect in seeker.lecture_set.all()],
        "tab": "frequencies",
        "add": True,
        "goback": reverse("seeker_frequencies", args=[pk]),
    }
    return render(request, "publicwork/seeker_add_or_change.html", context)


@login_required
@permission_required("publicwork.change_listener")
def update_frequency(request, seek_pk, freq_pk):
    seeker = Seeker.objects.get(pk=seek_pk)
    listener = Listener.objects.get(pk=freq_pk)
    if request.method == "POST":
        listener.ranking = (
            int(request.POST["ranking"]) if request.POST.get("ranking") else 0
        )
        listener.observations = request.POST["observations"]
        listener.save()
        messages.success(request, "The Listener has been updated!")
        return redirect("seeker_frequencies", pk=seek_pk)

    context = {
        "object": seeker,
        "listener": listener,
        "form": ListenerForm(instance=listener),
        "title": "update frequency | seeker side",
        "seeker_side": True,
        "goback": reverse("seeker_frequencies", args=[seek_pk]),
    }
    return render(request, "publicwork/listener_update.html", context)


@login_required
@permission_required("publicwork.delete_listener")
def remove_frequency(request, seek_pk, freq_pk):
    listener = Listener.objects.get(pk=freq_pk)

    if request.method == "POST":
        listener.delete()
        return redirect("seeker_frequencies", pk=seek_pk)

    context = {"object": listener, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


# handlers
def insert_historic_if_necessary(request, obj):
    if obj.historic_of_seeker_set.last().occurrence in ["NEW", "MT1"]:
        new_historic = dict(
            seeker=obj,
            date=timezone.now().date(),
            description="automatically added by frequency",
            made_by=request.user,
        )

        if obj.historic_of_seeker_set.last().occurrence == "NEW":
            new_historic["occurrence"] = "MT1"
        elif obj.historic_of_seeker_set.last().occurrence == "MT1":
            new_historic["occurrence"] = "MT2"

        Historic_of_seeker.objects.create(**new_historic)

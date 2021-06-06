from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from schooladmin.common import ACTIVITY_TYPES, paginator
from base.searchs import search_event

from person.models import Person
from event.models import Event, Frequency
from ..forms import MentoringFrequencyForm
from ..models import Workgroup, Membership


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_home(request):
    groups = Membership.objects.filter(
        person=request.user.person, role_type="MTR"
    )
    context = {"groups": groups, "title": "mentoring"}
    return render(request, "workgroup/mentoring/home.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_group_detail(request, pk):
    object = Workgroup.objects.get(pk=pk)

    queryset = object.membership_set.all().order_by("person__name_sa")

    object_list = paginator(queryset, 25, request.GET.get("page"))

    context = {
        "object": object,
        "object_list": object_list,
        "title": "workgroup detail",
    }
    return render(request, "workgroup/mentoring/group_detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_member_detail(request, group_pk, person_pk):
    object = Person.objects.get(pk=person_pk)
    age = (date.today() - object.birth).days // 365
    context = {
        "object": object,
        "title": "member detail",
        "tab": "info",
        "age": age,
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, "workgroup/mentoring/member_detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_member_frequencies(request, group_pk, person_pk):
    object = Person.objects.get(pk=person_pk)
    page = request.GET["page"] if request.GET.get("page") else 1
    object_list = object.frequency_set.all().order_by("-event__date")
    ranking = sum([f.ranking for f in object_list])
    context = {
        "object": object,
        "title": "member detail | frequencies",
        "object_list": paginator(object_list, page=page),
        "tab": "frequencies",
        "ranking": ranking,
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, "workgroup/mentoring/member_detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_member_historics(request, group_pk, person_pk):
    object = Person.objects.get(pk=person_pk)
    page = request.GET["page"] if request.GET.get("page") else 1
    object_list = object.historic_set.all().order_by("-date")
    context = {
        "object": object,
        "title": "member detail | frequencies",
        "object_list": paginator(object_list, page=page),
        "tab": "historics",
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, "workgroup/mentoring/member_detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def membership_add_frequency(request, group_pk, person_pk):
    object = Person.objects.get(pk=person_pk)

    if request.GET.get("pk"):
        event = Event.objects.get(pk=request.GET.get("pk"))

        if request.method == "POST":
            object.frequency_set.create(
                person=object,
                event=event,
                aspect=object.aspect,
                ranking=request.POST.get("ranking"),
                observations=request.POST.get("observations"),
            )
            messages.success(request, "The Frequency has been inserted!")
            return redirect(
                "mentoring_member_frequencies",
                group_pk=group_pk,
                person_pk=person_pk,
            )

        context = {
            "person": object,
            "form": MentoringFrequencyForm,
            "insert_to": f"{event.activity.name} {event.center}",
            "title": "confirm to insert",
        }
        return render(
            request, "workgroup/elements/confirm_add_frequency.html", context
        )

    queryset, page = search_event(request, Event)
    object_list = paginator(queryset, page=page)

    context = {
        "object": object,
        "object_list": object_list,
        "title": "insert frequencies",
        "type_list": ACTIVITY_TYPES,
        "pre_freqs": [obj.event.pk for obj in object.frequency_set.all()],
        "group_pk": group_pk,
    }
    return render(
        request, "workgroup/mentoring/member_add_frequency.html", context
    )


@login_required
@permission_required("workgroup.view_workgroup")
def membership_update_frequency(request, group_pk, person_pk, freq_pk):
    person = Person.objects.get(pk=person_pk)
    frequency = Frequency.objects.get(pk=freq_pk)

    if request.method == "POST":
        frequency.ranking = (
            int(request.POST["ranking"]) if request.POST.get("ranking") else 0
        )
        frequency.observations = request.POST["observations"]
        frequency.save()
        messages.success(request, "The Frequency has been updated!")
        return redirect(
            "mentoring_member_frequencies",
            group_pk=group_pk,
            person_pk=person_pk,
        )

    context = {
        "object": person,
        "event": frequency.event,
        "form": MentoringFrequencyForm(instance=frequency),
        "title": "update frequency | person side",
        "goback": reverse(
            "mentoring_member_frequencies", args=[group_pk, person_pk]
        ),
    }
    return render(
        request, "workgroup/mentoring/update_frequency.html", context
    )

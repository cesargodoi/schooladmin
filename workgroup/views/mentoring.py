from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from schooladmin.common import WORKGROUP_TYPES, paginator

from person.models import Person
from ..forms import WorkgroupForm
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
@permission_required("workgroup.add_workgroup")
def workgroup_create(request):
    if request.method == "POST":
        form = WorkgroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The Workgroup has been created!")

        return redirect("workgroup_home")

    context = {
        "form": WorkgroupForm(initial={"made_by": request.user}),
        "form_name": "Workgroup",
        "form_path": "workgroup/forms/workgroup.html",
        "goback": reverse("workgroup_home"),
        "title": "create workgroup",
        "to_create": True,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("workgroup.change_workgroup")
def workgroup_update(request, pk):
    workgroup = get_object_or_404(Workgroup, pk=pk)
    if request.method == "POST":
        form = WorkgroupForm(request.POST, instance=workgroup)
        if form.is_valid():
            form.save()
            messages.success(request, "The Workgroup has been updated!")

        return redirect("workgroup_detail", pk=pk)

    context = {
        "form": WorkgroupForm(
            instance=workgroup, initial={"made_by": request.user}
        ),
        "form_name": "Workgroup",
        "form_path": "workgroup/forms/workgroup.html",
        "goback": reverse("workgroup_detail", args=[pk]),
        "title": "update workgroup",
        "pk": pk,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("workgroup.delete_workgroup")
def workgroup_delete(request, pk):
    workgroup = get_object_or_404(Workgroup, pk=pk)
    if request.method == "POST":
        if workgroup.members:
            workgroup.members.clear()
        workgroup.delete()
        return redirect("workgroup_home")

    context = {
        "object": workgroup,
        "members": [
            m
            for m in workgroup.membership_set.all().order_by("-role_type")[:4]
        ],
        "title": "confirm to delete",
    }
    return render(
        request, "workgroup/elements/confirm_to_delete_workgroup.html", context
    )

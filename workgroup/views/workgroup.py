from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from schooladmin.common import WORKGROUP_TYPES, paginator

from ..forms import WorkgroupForm
from ..models import Workgroup


@login_required
@permission_required("workgroup.view_workgroup")
def workgroup_home(request):
    term = request.GET.get("term") if request.GET.get("term") else ""

    _query = [
        Q(name__icontains=term),
        Q(is_active=True),
        Q(center=request.user.person.center),
    ]

    if request.GET.get("all"):
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    if request.GET.get("wg_type"):
        _query.append(Q(workgroup_type=request.GET.get("wg_type")))

    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    queryset = Workgroup.objects.filter(query).order_by("name")

    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object_list": object_list,
        "title": "workgroups",
        "workgroup_types": WORKGROUP_TYPES,
        "all": True if request.GET.get("all") else False,
        "term": request.GET.get("term"),
        "wg_type": request.GET.get("wg_type"),
    }
    return render(request, "workgroup/workgroup_home.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def workgroup_detail(request, pk):
    object = Workgroup.objects.get(pk=pk)

    queryset = object.membership_set.all().order_by("person__name_sa")

    object_list = paginator(queryset, 25, request.GET.get("page"))

    context = {
        "object": object,
        "object_list": object_list,
        "title": "workgroup detail",
    }
    return render(request, "workgroup/workgroup_detail.html", context)


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
        "title": "create workgroup",
        "to_create": True,
    }
    return render(request, "workgroup/workgroup_form.html", context)


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
        "title": "update workgroup",
        "pk": pk,
    }
    return render(request, "workgroup/workgroup_form.html", context)


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
            m for m in workgroup.membership_set.all().order_by("-role_type")[:4]
        ],
        "title": "confirm to delete",
    }
    return render(
        request, "workgroup/elements/confirm_to_delete_workgroup.html", context
    )

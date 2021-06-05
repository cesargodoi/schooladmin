from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from person.models import Person
from schooladmin.common import ASPECTS, STATUS, paginator

from ..forms import MembershipForm
from ..models import Membership, Workgroup
from base.searchs import search_person


@login_required
@permission_required("workgroup.add_membership")
def membership_insert(request, workgroup_id):
    workgroup = get_object_or_404(Workgroup, pk=workgroup_id)

    if request.GET.get("pk"):
        person = get_object_or_404(Person, pk=request.GET.get("pk"))

        if request.method == "POST":
            workgroup.members.add(person)
            messages.success(
                request, "The person has been inserted on workgroup!"
            )
            return redirect("workgroup_detail", pk=workgroup_id)

        context = {
            "person": person,
            "insert_to": f"{workgroup.name} {workgroup.center}",
            "title": "confirm to insert",
        }
        return render(
            request,
            "workgroup/elements/confirm_to_insert_membership.html",
            context,
        )

    queryset, page = search_person(request, Person)
    object_list = paginator(queryset, 25, page=page)

    context = {
        "object_list": object_list,
        "aspect_list": ASPECTS,
        "status_list": STATUS,
        "form": MembershipForm(initial={"workgroup": workgroup}),
        "title": "create membership",
        "object": workgroup,
    }

    return render(request, "workgroup/membership_insert.html", context)


@login_required
@permission_required("workgroup.change_membership")
def membership_update(request, workgroup_id, pk):
    membership = get_object_or_404(Membership, pk=pk)

    if request.method == "POST":
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            messages.success(request, "The Membership has been updated!")

        return redirect("workgroup_detail", pk=workgroup_id)

    context = {
        "form": MembershipForm(instance=membership),
        "title": "update membership",
        "object": membership.workgroup,
    }
    return render(request, "workgroup/membership_update.html", context)


@login_required
@permission_required("workgroup.delete_membership")
def membership_delete(request, workgroup_id, pk):
    membership = get_object_or_404(Membership, pk=pk)
    if request.method == "POST":
        membership.delete()
        return redirect("workgroup_detail", pk=workgroup_id)

    context = {"object": membership, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)

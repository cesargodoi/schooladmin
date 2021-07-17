from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from schooladmin.common import paginator, clear_session
from base.searchs import search_center

from .forms import CenterForm, SelectNewCenterForm
from .models import Center


@login_required
@permission_required("center.view_center")
def center_home(request):
    object_list = None
    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page = search_center(request, Center)
        object_list = paginator(queryset, page=page)

    context = {
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "title": "center home",
        "nav": "home",
    }
    return render(request, "center/center_home.html", context)


@login_required
@permission_required("center.view_center")
def center_detail(request, pk):
    center = Center.objects.get(pk=pk)
    users = len([p.id for p in center.person_set.all() if p.is_active])

    context = {
        "object": center,
        "title": "center detail",
        "users": users,
        "nav": "detail",
    }
    return render(request, "center/center_detail.html", context)


@login_required
@permission_required("center.add_center")
def center_create(request):
    if request.method == "POST":
        form = CenterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = f"The Center '{request.POST['name']}' has been created!"
            messages.success(request, message)
            return redirect("center_home")

    context = {
        "form": CenterForm(initial={"made_by": request.user}),
        "form_name": "Center",
        "form_path": "center/forms/center.html",
        "goback": reverse("center_home"),
        "title": "create center",
        "to_create": True,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("center.change_center")
def center_update(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == "POST":
        form = CenterForm(request.POST, request.FILES, instance=center)
        if form.is_valid():
            form.save()
            message = f"The Center '{request.POST['name']}' has been updated!"
            messages.success(request, message)
            return redirect("center_detail", pk=pk)

    context = {
        "form": CenterForm(instance=center),
        "form_name": "Center",
        "form_path": "center/forms/center.html",
        "goback": reverse("center_detail", args=[pk]),
        "title": "update center",
        "id": pk,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("center.delete_center")
def center_delete(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == "POST":
        if request.POST.get("conf_center"):
            _center = Center.objects.get(pk=request.POST.get("conf_center"))
            persons = center.person_set.all()
            for person in persons:
                person.center = _center
                person.save()
        center.is_active = False
        center.save()
        return redirect("center_home")

    context = {
        "object": center,
        "new_center": SelectNewCenterForm() if center.person_set.all() else "",
        "title": "confirm to delete",
    }
    return render(request, "center/confirm_delete.html", context)


@login_required
@permission_required("center.add_center")
def center_reinsert(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == "POST":
        center.is_active = True
        center.save()
        return redirect("center_home")

    context = {"object": center, "title": "confirm to reinsert"}
    return render(request, "center/confirm_reinsert.html", context)

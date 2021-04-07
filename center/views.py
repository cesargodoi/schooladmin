from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from schooladmin.common import paginator

from .forms import CenterForm, SelectNewCenterForm
from .models import Center


@login_required
@permission_required("center.view_center")
def center_home(request):
    queryset, page = center_search(request)
    object_list = paginator(queryset, page=page)

    context = {
        "object_list": object_list,
        "title": "center home",
    }
    return render(request, "center/center_home.html", context)


@login_required
@permission_required("center.view_center")
def center_detail(request, pk):
    center = get_object_or_404(Center, pk=pk)
    users = len([p.id for p in center.person_set.all() if p.is_active])

    context = {
        "object": center,
        "title": "center detail",
        "users": users,
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
        "title": "create center",
        "to_create": True,
    }
    return render(request, "center/center_form.html", context)


@login_required
@permission_required("center.change_center")
def center_update(request, pk):
    center = get_object_or_404(Center, pk=pk)
    if request.method == "POST":
        form = CenterForm(request.POST, request.FILES, instance=center)
        if form.is_valid():
            form.save()
            message = f"The Center '{request.POST['name']}' has been updated!"
            messages.success(request, message)
            return redirect("center_detail", pk=pk)

    context = {
        "form": CenterForm(instance=center),
        "title": "update center",
        "id": pk,
    }
    return render(request, "center/center_form.html", context)


@login_required
@permission_required("center.delete_center")
def center_delete(request, pk):
    center = get_object_or_404(Center, pk=pk)
    if request.method == "POST":
        if request.POST.get("conf_center"):
            _center = get_object_or_404(
                Center, pk=request.POST.get("conf_center")
            )
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
    center = get_object_or_404(Center, pk=pk)
    if request.method == "POST":
        center.is_active = True
        center.save()
        return redirect("center_home")

    context = {"object": center, "title": "confirm to reinsert"}
    return render(request, "center/confirm_reinsert.html", context)


# auxiliar functions
def center_search(request):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "term": "",
            "all": "",
            "page": 1,
        }
    # adjust search
    search = request.session["search"]
    if request.GET.get("page"):
        search["page"] = request.GET["page"]
    else:
        search["page"] = 1
        search["term"] = request.GET["term"] if request.GET.get("term") else ""
        search["all"] = "on" if request.GET.get("all") else ""
    # save session
    request.session.modified = True
    # basic query
    _query = [
        Q(is_active=True),
        Q(name__icontains=search["term"]),
    ]
    # adding more complexity
    if search["all"]:
        _query.remove(Q(is_active=True))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return Center.objects.filter(query).order_by("name"), search["page"]

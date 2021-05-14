from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from schooladmin.common import paginator, belongs_center

from ..forms import SeekerForm
from ..models import Seeker
from ..utils import seeker_search


@login_required
@permission_required("publicwork.view_seeker")
def seeker_home(request):
    queryset, page = seeker_search(request, Seeker)
    object_list = paginator(queryset, page=page)

    context = {
        "object_list": object_list,
        "title": "seeker home",
    }

    return render(request, "publicwork/seeker_home.html", context)


@login_required
@permission_required("publicwork.view_seeker")
def seeker_detail(request, pk):
    belongs_center(request, pk, Seeker)
    seeker = Seeker.objects.get(pk=pk)
    age = (date.today() - seeker.birth).days // 365

    context = {
        "object": seeker,
        "title": "seeker detail",
        "tab": "info",
        "age": age,
    }
    return render(request, "publicwork/seeker_detail.html", context)


@login_required
@permission_required("publicwork.add_seeker")
def seeker_create(request):
    if request.method == "POST":
        seeker_form = SeekerForm(request.POST, request.FILES)
        if seeker_form.is_valid():
            seeker_form.save()
            message = f"The Seeker '{request.POST['name']}' has been created!"
            messages.success(request, message)
            return redirect("seeker_home")

    context = {
        "form": SeekerForm(
            initial={
                "made_by": request.user,
                "center": request.user.person.center,
            }
        ),
        "title": "create seeker",
        "to_create": True,
    }
    return render(request, "publicwork/seeker_form.html", context)


@login_required
@permission_required("publicwork.change_seeker")
def seeker_update(request, pk):
    belongs_center(request, pk, Seeker)

    seeker = Seeker.objects.get(pk=pk)
    if request.method == "POST":
        seeker_form = SeekerForm(request.POST, request.FILES, instance=seeker)
        if seeker_form.is_valid():
            seeker_form.save()
            message = f"The Seeker '{request.POST['name']}' has been updated!"
            messages.success(request, message)

        return redirect("seeker_detail", pk=pk)

    seeker_form = SeekerForm(
        instance=seeker,
        initial={"made_by": request.user},
    )

    context = {
        "form": seeker_form,
        "title": "update seeker",
        "pk": pk,
    }
    return render(request, "publicwork/seeker_form.html", context)


@login_required
@permission_required("publicwork.delete_seeker")
def seeker_delete(request, pk):
    seeker = Seeker.objects.get(pk=pk)
    if request.method == "POST":
        if seeker.listener_set.all():
            seeker.is_active = False
            seeker.save()
        else:
            seeker.delete()
        return redirect("seeker_home")

    context = {"object": seeker, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


@login_required
@permission_required("publicwork.add_seeker")
def seeker_reinsert(request, pk):
    seeker = Seeker.objects.get(pk=pk)
    if request.method == "POST":
        seeker.is_active = True
        seeker.save()
        return redirect("seeker_home")

    context = {"object": seeker, "title": "confirm to reinsert"}
    return render(
        request, "publicwork/elements/confirm_to_reinsert_seeker.html", context
    )


# seeker frequencies
@login_required
@permission_required("publicwork.view_seeker")
def seeker_frequencies(request, pk):
    belongs_center(request, pk, Seeker)
    page = request.GET["page"] if request.GET.get("page") else 1

    seeker = Seeker.objects.get(pk=pk)
    frequencies = seeker.listener_set.all()
    ranking = sum([f.ranking for f in frequencies])

    context = {
        "object": seeker,
        "title": "seeker detail | frequencies",
        "object_list": paginator(frequencies, page=page),
        "tab": "frequencies",
        "ranking": ranking,
    }

    return render(request, "publicwork/seeker_detail.html", context)


# seeker historics
@login_required
@permission_required("publicwork.view_seeker")
def seeker_historics(request, pk):
    belongs_center(request, pk, Seeker)
    page = request.GET["page"] if request.GET.get("page") else 1

    seeker = Seeker.objects.get(pk=pk)
    historics = seeker.historic_set.all().order_by("-date")

    context = {
        "object": seeker,
        "title": "seeker detail | historics",
        "object_list": paginator(historics, page=page),
        "tab": "historics",
    }

    return render(request, "publicwork/seeker_detail.html", context)

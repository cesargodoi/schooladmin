from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from ..forms import HistoricForm
from ..models import Seeker, Historic_of_seeker


@login_required
@permission_required("publicwork.add_historic")
def create_historic(request, pk):
    seeker = Seeker.objects.get(pk=pk)

    if request.method == "POST":
        form = HistoricForm(request.POST)
        if form.is_valid():
            form.save()
            adjust_seeker_side(
                seeker,
                request.POST.get("occurrence"),
                request.POST.get("date"),
            )
            if request.POST["occurrence"] == "RST":
                seeker.is_active = False
                seeker.save()
            messages.success(request, "The Historic has been created!")

        return redirect("seeker_historics", pk=pk)

    context = {
        "object": seeker,
        "form": HistoricForm(
            initial={
                "seeker": seeker,
                "date": timezone.now(),
                "made_by": request.user,
            }
        ),
        "title": "add historic",
        "tab": "historic",
        "add": True,
        "goback": reverse("seeker_historics", args=[pk]),
    }
    return render(request, "publicwork/seeker_add_or_change.html", context)


@login_required
@permission_required("publicwork.change_historic")
def update_historic(request, seek_pk, hist_pk):
    seeker = Seeker.objects.get(pk=seek_pk)
    historic = Historic_of_seeker.objects.get(pk=hist_pk)
    if request.method == "POST":
        form = HistoricForm(request.POST, instance=historic)
        if form.is_valid():
            form.save()
            adjust_seeker_side(
                seeker,
                request.POST.get("occurrence"),
                request.POST.get("date"),
            )
            messages.success(request, "The Historic has been updated!")

        return redirect("seeker_historics", pk=seek_pk)

    context = {
        "object": seeker,
        "form": HistoricForm(instance=historic),
        "title": "change historic",
        "tab": "historic",
        "goback": reverse("seeker_historics", args=[seek_pk]),
    }
    return render(request, "publicwork/seeker_add_or_change.html", context)


@login_required
@permission_required("publicwork.add_historic")
def delete_historic(request, seek_pk, hist_pk):
    historic = Historic_of_seeker.objects.get(pk=hist_pk)
    if request.method == "POST":
        historic.delete()
        return redirect("seeker_historics", pk=seek_pk)

    context = {"object": historic, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


# handlers
def adjust_seeker_side(seeker, occur, dt):
    date = datetime.strptime(dt, "%Y-%m-%d").date()
    if not seeker.status_date or date >= seeker.status_date:
        seeker.status = occur
        seeker.status_date = date
        seeker.save()

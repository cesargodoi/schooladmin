from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from ..forms import HistoricForm
from ..models import Seeker, Historic


@login_required
@permission_required("publicwork.add_historic")
def create_historic(request, pk):
    seeker = get_object_or_404(Seeker, pk=pk)

    if request.method == "POST":
        form = HistoricForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
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
    seeker = get_object_or_404(Seeker, pk=seek_pk)
    historic = get_object_or_404(Historic, pk=hist_pk)
    if request.method == "POST":
        form = HistoricForm(request.POST, instance=historic)
        if form.is_valid():
            form.save()
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
    historic = get_object_or_404(Historic, pk=hist_pk)
    if request.method == "POST":
        historic.delete()
        return redirect("seeker_historics", pk=seek_pk)

    context = {"object": historic, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)

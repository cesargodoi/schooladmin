from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ActivityForm
from ..models import Activity


@login_required
@permission_required("event.view_activity")
def activity_home(request):
    activities = Activity.objects.all()

    context = {"object_list": activities, "title": "Activities"}
    return render(request, "event/activity_home.html", context)


@login_required
@permission_required("event.add_activity")
def activity_create(request):
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            message = "The Activity has been created!"
            messages.success(request, message)
            return redirect("activity_home")

    context = {
        "form": ActivityForm(),
        "to_create": True,
        "title": "Create Activity",
    }
    return render(request, "event/activity_form.html", context)


@login_required
@permission_required("event.change_activity")
def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            message = "The Activity has been updated!"
            messages.success(request, message)
            return redirect("activity_home")

    context = {
        "form": ActivityForm(instance=activity),
        "title": "Update Activity",
    }
    return render(request, "event/activity_form.html", context)


@login_required
@permission_required("event.delete_activity")
def activity_delete(request, pk):
    object = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        if object.event_set.all():
            object.is_active = False
            object.save()
        else:
            object.delete()
        message = "The Activity has been deleted!"
        messages.success(request, message)
        return redirect("activity_home")

    context = {"object": object, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)

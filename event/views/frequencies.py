from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from person.models import Person

from ..forms import FrequenciesAddForm
from ..models import Event


@login_required
@permission_required(["event.change_event", "person.change_person"])
def frequency_delete(request, pk, person_id):
    event = get_object_or_404(Event, pk=pk)
    person = event.frequencies.get(id=person_id)
    object = f"Remove: {person.name} from: {event}"
    if request.method == "POST":
        event.frequencies.remove(person)
        message = "The Frequency has been deleted!"
        messages.success(request, message)
        return redirect("event_detail", pk=pk)

    context = {"object": object, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


@login_required
@permission_required(["event.change_event", "person.change_person"])
def frequencies_add(request, pk):
    object = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        from_request = set(
            request.POST.get("frequencies").replace(" ", "").split(",")
        )
        regs, unknow = [], []
        for reg in from_request:
            try:
                person = Person.objects.get(reg=reg)
                object.frequencies.add(person)
                regs.append(reg)
            except:
                unknow.append(reg)
        if len(regs) > 0:
            message = f"{len(regs)} persons were launched at this Event. "
            messages.success(request, message)
        if unknow:
            message = (
                f"{len(unknow)} registration numbers are unknown: {unknow}"
            )
            messages.warning(request, message)

        return redirect("event_detail", pk=pk)

    context = {
        "object": object,
        "form": FrequenciesAddForm(),
        "title": "insert frequencies",
    }
    return render(request, "event/frequencies_add.html", context)

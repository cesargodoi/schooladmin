from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import Http404
from schooladmin.common import paginator, LECTURE_TYPES

from ..forms import LectureForm
from ..models import Lecture
from ..utils import lecture_search


@login_required
@permission_required("publicwork.view_lecture")
def lecture_home(request):
    queryset, page = lecture_search(request, Lecture)

    object_list = paginator(queryset, page=page)

    context = {
        "object_list": object_list,
        "title": "lecture home",
        "type_list": LECTURE_TYPES,
    }

    return render(request, "publicwork/lecture_home.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def lecture_detail(request, pk):
    object = get_object_or_404(Lecture, pk=pk)
    queryset = object.listener_set.all().order_by("seeker__name_sa")

    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object": object,
        "object_list": object_list,
        "title": "lecture detail",
    }
    return render(request, "publicwork/lecture_detail.html", context)


@login_required
@permission_required("publicwork.add_lecture")
def lecture_create(request):
    if request.method == "POST":
        form = LectureForm(request.POST)
        if form.is_valid():
            form.save()
            message = (
                f"The lecture '{request.POST['theme']}' has been created!"
            )
            messages.success(request, message)
            return redirect("lecture_home")

    lecture_form = LectureForm(
        initial={
            "made_by": request.user,
            "center": request.user.person.center,
        }
    )

    context = {
        "form": lecture_form,
        "title": "create lecture",
        "to_create": True,
    }
    return render(request, "publicwork/lecture_form.html", context)


@login_required
@permission_required("publicwork.change_lecture")
def lecture_update(request, pk):
    object = Lecture.objects.get(pk=pk)
    if object.center != request.user.person.center:
        raise Http404
    if request.method == "POST":
        form = LectureForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            message = (
                f"The lecture '{request.POST['theme']}' has been updated!"
            )
            messages.success(request, message)
            return redirect("lecture_detail", pk=pk)

    lecture_form = LectureForm(
        instance=object,
        initial={"made_by": request.user},
    )

    context = {
        "form": lecture_form,
        "title": "update lecture",
        "pk": pk,
    }
    return render(request, "publicwork/lecture_form.html", context)


@login_required
@permission_required("publicwork.delete_lecture")
def lecture_delete(request, pk):
    object = get_object_or_404(Lecture, pk=pk)
    if object.center != request.user.person.center:
        raise Http404
    if request.method == "POST":
        object.delete()
        message = "The lecture has been deleted!"
        messages.success(request, message)
        return redirect("lecture_home")

    context = {
        "object": object,
        "title": "confirm to delete",
    }
    return render(request, "base/confirm_delete.html", context)

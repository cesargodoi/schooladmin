import os
from datetime import datetime, timedelta
from django.http.response import Http404
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from center.models import Center


@login_required
def home(request):
    if request.user.person.center:
        center = Center.objects.get(id=request.user.person.center.id)
    elif Center.objects.count() > 0:
        center = Center.objects.first()
    else:
        raise Http404

    context = {"object": center}
    return render(request, "base/home.html", context)


def change_color_scheme(request):
    if request.is_ajax():
        if (
            not request.session.get("color_theme")
            or request.session["color_theme"] == "light"
        ):
            request.session["color_theme"] = "dark"
        else:
            request.session["color_theme"] = "light"

        return JsonResponse({"change": True}, safe=False)

    return render(request, "base/home.html")


def error_404(request, exception):
    return render(request, "base/404.html")


def clear_session(request):
    for key in request.session.keys():
        del request.session[key]

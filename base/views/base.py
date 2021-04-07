from datetime import datetime, timedelta
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from center.models import Center


@login_required
def home(request):
    try:
        center = get_object_or_404(Center, id=request.user.person.center.id)
    except:
        raise Http404

    context = {"object": center}
    return render(request, "base/home.html", context)


def error_404(request, exception):
    return render(request, "base/404.html")

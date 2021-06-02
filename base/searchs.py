from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone


def event_search(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "dt1": "",
            "dt2": "",
            "type": "SRV",
            "all": "",
            "page": 1,
        }
    # adjust search
    search = request.session["search"]
    if request.GET.get("page"):
        search["page"] = request.GET["page"]
    else:
        search["page"] = 1
        dt1 = (
            datetime.strptime(request.GET["dt1"], "%Y-%m-%d")
            if request.GET.get("dt1")
            else timezone.now() - timedelta(30)
        )
        search["dt1"] = dt1.strftime("%Y-%m-%d")
        dt2 = (
            datetime.strptime(request.GET["dt2"], "%Y-%m-%d")
            if request.GET.get("dt2")
            else timezone.now()
        )
        search["dt2"] = dt2.strftime("%Y-%m-%d")
        search["type"] = request.GET["type"] if request.GET.get("type") else ""
        search["all"] = "on" if request.GET.get("all") else ""
    # save session
    request.session.modified = True
    # basic query
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(date__range=[search["dt1"], search["dt2"]]),
    ]
    # adding more complexity
    if search["type"]:
        _query.append(Q(activity__activity_type=search["type"]))
    if search["all"]:
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (
        obj.objects.filter(query).order_by("-date"),
        search["page"],
    )

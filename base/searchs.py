from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone


#  center  ####################################################################
def search_center(request, obj):
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

    return (obj.objects.filter(query).order_by("name"), search["page"])


#  person  ####################################################################
def search_person(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "term": "",
            "aspect": "",
            "status": "",
            "all": "",
            "page": 1,
        }
    # adjust search
    search = request.session["search"]
    search["page"] = request.GET["page"] if request.GET.get("page") else 1
    search["term"] = request.GET["term"] if request.GET.get("term") else ""
    search["aspect"] = (
        request.GET["aspect"] if request.GET.get("aspect") else ""
    )
    search["status"] = (
        request.GET["status"] if request.GET.get("status") else ""
    )
    search["all"] = "on" if request.GET.get("all") else ""

    # save session
    request.session.modified = True
    # basic query
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(name_sa__icontains=search["term"]),
    ]
    # adding more complexity
    if search["aspect"]:
        _query.append(Q(aspect=search["aspect"]))
    if search["status"]:
        _query.append(Q(status=search["status"]))
        if search["status"] in ["DIS", "REM", "DEA"]:
            _query.remove(Q(is_active=True))
    if search["all"]:
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("name_sa"), search["page"])


#  envent  ####################################################################
def search_event(request, obj):
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

    return (obj.objects.filter(query).order_by("-date"), search["page"])


#  workgroups  ################################################################
def search_workgroup(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "term": "",
            "type": "SRV",
            "all": "",
            "page": 1,
        }
    # adjust search
    search = request.session["search"]
    search["page"] = request.GET["page"] if request.GET.get("page") else 1
    search["term"] = request.GET["term"] if request.GET.get("term") else ""
    search["type"] = request.GET["type"] if request.GET.get("type") else ""
    search["all"] = "on" if request.GET.get("all") else ""
    # save session
    request.session.modified = True
    # basic query
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(name__icontains=search["term"]),
    ]
    # adding more complexity
    if search["type"]:
        _query.append(Q(workgroup_type=search["type"]))
    if search["all"]:
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("name"), search["page"])


#  seeker  ####################################################################
def search_seeker(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "name": "",
            "center": request.user.person.center.pk,
            "city": "",
            "all": "",
            "page": 1,
        }
    # adjust search
    search = request.session["search"]
    search["page"] = request.GET["page"] if request.GET.get("page") else 1
    search["name"] = request.GET["name"] if request.GET.get("name") else ""
    search["center"] = (
        request.GET["center"] if request.GET.get("center") else ""
    )
    search["city"] = request.GET["city"] if request.GET.get("city") else ""
    search["all"] = "on" if request.GET.get("all") else ""
    # save session
    request.session.modified = True
    # basic query
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(name_sa__icontains=search["name"]),
    ]
    # adding more complexity
    if search["center"]:
        _query.remove(Q(center=request.user.person.center))
        _query.append(Q(center__pk=search["center"]))
    if search["city"]:
        _query.append(Q(city__icontains=search["city"]))
    if search["all"]:
        _query.remove(Q(is_active=True))
        if Q(center=request.user.person.center) in _query:
            _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("name_sa"), search["page"])


#  lecture  ###################################################################
def search_lecture(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "dt1": "",
            "dt2": "",
            "type": "CTT",
            "all": "",
            "page": 1,
        }
    # adjust search
    search = request.session["search"]
    search["page"] = request.GET["page"] if request.GET.get("page") else 1
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
        _query.append(Q(type=search["type"]))
    if search["all"]:
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("-date"), search["page"])


#  orders  ####################################################################
def search_order(request, obj):
    if not request.session.get("search"):
        request.session["search"] = {
            "term": "",
            "status": "",
            "dt1": (timezone.now().date() - timedelta(30)).strftime(
                "%Y-%m-%d"
            ),
            "dt2": timezone.now().date().strftime("%Y-%m-%d"),
        }
    # adjust search
    search = request.session["search"]
    search["page"] = request.GET["page"] if request.GET.get("page") else 1
    search["term"] = request.GET.get("term") if request.GET.get("term") else ""
    search["status"] = (
        request.GET.get("status") if request.GET.get("status") else ""
    )
    dt1 = (
        datetime.strptime(request.GET["dt1"], "%Y-%m-%d")
        if request.GET.get("dt1")
        else datetime.strptime(search["dt1"], "%Y-%m-%d")
    )
    search["dt1"] = dt1.strftime("%Y-%m-%d")
    dt2 = (
        datetime.strptime(request.GET["dt2"], "%Y-%m-%d")
        if request.GET.get("dt2")
        else datetime.strptime(search["dt2"], "%Y-%m-%d")
    )
    search["dt2"] = dt2.strftime("%Y-%m-%d")
    # save session
    request.session.modified = True
    # basic query
    _query = [
        Q(center=request.user.person.center),
        Q(person__name__icontains=search["term"]),
        Q(created_on__date__range=[dt1, dt2]),
    ]
    # adding more complexity
    if search["status"]:
        _query.append(Q(status=search["status"]))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("-created_on"), search["page"])

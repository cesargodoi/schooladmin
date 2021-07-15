from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone


#  center  ####################################################################
def search_center(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "page": 1,
            "term": "",
            "all": "",
        }
    # adjust search
    search = request.session["search"]
    search["page"] = request.GET["page"] if request.GET.get("page") else 1
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
            "page": 1,
            "term": "",
            "aspect": "all",
            "status": "all",
            "all": "",
        }
    # adjust search
    search = request.session["search"]
    search["page"] = request.GET["page"] if request.GET.get("page") else 1
    search["term"] = (
        request.GET["term"] if request.GET.get("term") else search["term"]
    )
    search["aspect"] = (
        request.GET["aspect"]
        if request.GET.get("aspect")
        else search["aspect"]
    )
    search["status"] = (
        request.GET["status"]
        if request.GET.get("status")
        else search["status"]
    )
    search["all"] = "on" if request.GET.get("all") else search["all"]
    # save session
    request.session.modified = True
    # basic query
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(name_sa__icontains=search["term"]),
    ]
    # adding more complexity
    if search["aspect"] != "all":
        _query.append(Q(aspect=search["aspect"]))
    if search["status"] != "all":
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


#  event  ####################################################################
def search_event(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "page": 1,
            "dt1": "",
            "dt2": "",
            "type": "SRV",
            "all": "",
        }
    # adjust search
    search = request.session["search"]

    search["page"] = request.GET["page"] if request.GET.get("page") else 1
    search["page"] = 1
    search["dt1"] = get_date(request, "dt1", days=30)
    search["dt2"] = get_date(request, "dt2")
    search["type"] = (
        request.GET["type"] if request.GET.get("type") else search["type"]
    )
    search["all"] = "on" if request.GET.get("all") else search["all"]
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
            "city": "",
            "center": request.user.person.center.pk,
            "status": "all",
            "all": "",
            "page": 1,
        }
    # adjust search
    search = request.session["search"]
    search["page"] = request.GET["page"] if request.GET.get("page") else 1
    search["name"] = (
        request.GET["name"] if request.GET.get("name") else search["name"]
    )
    search["city"] = (
        request.GET["city"] if request.GET.get("city") else search["city"]
    )
    search["center"] = (
        request.GET["center"]
        if request.GET.get("center")
        else search["center"]
    )
    search["status"] = (
        request.GET["status"]
        if request.GET.get("status")
        else search["status"]
    )
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
    if search["status"] != "all":
        _query.append(Q(status=search["status"]))
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
            "type": "",
            "all": "",
            "page": 1,
        }
    # adjust search
    search = request.session["search"]
    search["page"] = request.GET["page"] if request.GET.get("page") else 1
    search["dt1"] = get_date(request, "dt1", days=30)
    search["dt2"] = get_date(request, "dt2")
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


#  lecture  ###################################################################
def search_pw_group(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "name": "",
            "center": request.user.person.center.pk,
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
    search["all"] = "on" if request.GET.get("all") else ""
    # save session
    request.session.modified = True
    # basic query
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(name__icontains=search["name"]),
    ]
    # adding more complexity
    if search["center"]:
        _query.remove(Q(center=request.user.person.center))
        _query.append(Q(center__pk=search["center"]))
    if search["all"]:
        _query.remove(Q(is_active=True))
        if Q(center=request.user.person.center) in _query:
            _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("name"), search["page"])


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
    search["dt1"] = get_date(request, "dt1", days=30)
    search["dt2"] = get_date(request, "dt2")
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


# handlers
def get_date(request, dtx, days=0):
    date = (
        datetime.strptime(request.GET[dtx], "%Y-%m-%d")
        if request.GET.get(dtx)
        else timezone.now() - timedelta(days)
    )
    return date.strftime("%Y-%m-%d")

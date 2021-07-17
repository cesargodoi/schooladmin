from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone


#  center  ####################################################################
def search_center(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {"term": "", "page": 1, "all": ""}
    adjust_session(request, ["term", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True)]
    # adding more complexity
    if search["term"]:
        _query.append(Q(name__icontains=search["term"]))
    if search["all"] == "on":
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
            "aspect": "all",
            "status": "all",
            "page": 1,
            "all": "off",
        }
    adjust_session(request, ["term", "aspect", "status", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["term"]:
        _query.append(Q(name_sa__icontains=search["term"]))
    if search["aspect"] != "all":
        _query.append(Q(aspect=search["aspect"]))
    if search["status"] != "all":
        _query.append(Q(status=search["status"]))
        if search["status"] in ["DIS", "REM", "DEA"]:
            _query.remove(Q(is_active=True))
    if search["all"] == "on":
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
            "dt1": "",
            "dt2": "",
            "type": "all",
            "page": 1,
            "all": "off",
        }
    adjust_session(request, ["dt1", "dt2", "type", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(date__range=[search["dt1"], search["dt2"]]),
    ]
    # adding more complexity
    if search["type"] != "all":
        _query.append(Q(activity__activity_type=search["type"]))
    if search["all"] == "on":
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
            "type": "all",
            "page": 1,
            "all": "off",
        }
    adjust_session(request, ["term", "type", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["term"]:
        _query.append(Q(name__icontains=search["term"]))
    if search["type"] != "all":
        _query.append(Q(workgroup_type=search["type"]))
    if search["all"] == "on":
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
            "page": 1,
            "all": "off",
        }
    adjust_session(
        request, ["name", "city", "center", "status", "page", "all"]
    )
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["name"]:
        _query.append(Q(name_sa__icontains=search["name"]))
    if search["center"]:
        _query.remove(Q(center=request.user.person.center))
        _query.append(Q(center__pk=search["center"]))
    if search["city"]:
        _query.append(Q(city__icontains=search["city"]))
    if search["status"] != "all":
        _query.append(Q(status=search["status"]))
    if search["all"] == "on":
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
            "type": "all",
            "page": 1,
            "all": "off",
        }
    adjust_session(request, ["dt1", "dt2", "type", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(date__range=[search["dt1"], search["dt2"]]),
    ]
    # adding more complexity
    if search["type"] != "all":
        _query.append(Q(type=search["type"]))
    if search["all"] == "on":
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("-date"), search["page"])


#  pw group  ##################################################################
def search_pw_group(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "name": "",
            "center": request.user.person.center.pk,
            "page": 1,
            "all": "off",
        }
    adjust_session(request, ["name", "center", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["name"]:
        _query.append(Q(name__icontains=search["name"]))
    if search["center"]:
        _query.remove(Q(center=request.user.person.center))
        _query.append(Q(center__pk=search["center"]))
    if search["all"] == "on":
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
            "dt1": "",
            "dt2": "",
            "name": "",
            "status": "all",
            "page": 1,
        }
    adjust_session(request, ["dt1", "dt2", "name", "status", "page"])
    # basic query
    search = request.session["search"]
    # basic query
    _query = [
        Q(center=request.user.person.center),
        Q(created_on__date__range=[search["dt1"], search["dt2"]]),
    ]
    # adding more complexity
    if search["name"]:
        _query.append(Q(person__name_sa__icontains=search["name"]))
    if search["status"] != "all":
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


def adjust_session(request, fields):
    search = request.session["search"]
    for field in fields:
        if field == "all":
            if request.GET.get(field) == "on":
                search[field] = request.GET[field]
            if request.GET.get(field) == "off":
                search[field] = request.GET[field]
        elif field in ["dt1", "dt2", "dt", "date"]:
            search[field] = (
                get_date(request, "dt1", days=30)
                if field == "dt1"
                else get_date(request, "dt2")
            )
        else:
            if request.GET.get(field):
                search[field] = request.GET[field]
    # save session
    request.session.modified = True

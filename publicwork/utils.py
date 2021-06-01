from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone
from schooladmin.common import SEEKER_STATUS, LECTURE_TYPES


def seeker_search(request, obj):
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
    if request.GET.get("page"):
        search["page"] = request.GET["page"]
    else:
        search["page"] = 1
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

    return (
        obj.objects.filter(query).order_by("name_sa"),
        search["page"],
    )


def lecture_search(request, obj):
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
        _query.append(Q(type=search["type"]))
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


def queryset_per_date(request, Table):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "dt1": "",
            "dt2": "",
            "all": "",
        }
    # adjust search
    search = request.session["search"]
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
    if search["all"]:
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return Table.objects.filter(query).order_by("-date")


def queryset_per_status(request, model):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "status": "",
        }
    # adjust search
    search = request.session["search"]
    search["status"] = (
        request.GET["status"] if request.GET.get("status") else ""
    )
    # save session
    request.session.modified = True
    # basic query
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["status"] != "all":
        _query.append(Q(status=search["status"]))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return model.objects.filter(query).order_by("name_sa")


# reports
def get_lectures_dict(request, model):
    _dict = []
    for obj in queryset_per_date(request, model):
        row = dict(
            pk=obj.pk,
            date=obj.date,
            theme=obj.theme,
            type=str([lt[1] for lt in LECTURE_TYPES if lt[0] == obj.type][0]),
            listeners=obj.listener_set.count(),
            center=str(obj.center),
            center_city=obj.center.city,
            center_state=obj.center.state,
            center_country=obj.center.country,
        )
        _dict.append(row)
    return _dict


def get_frequencies_dict(request, model):
    _dict = []
    for obj in queryset_per_date(request, model):
        if obj.listener_set.count():
            for freq in obj.listener_set.all():
                row = dict(
                    pk=freq.pk,
                    ranking=freq.ranking,
                    obs=freq.observations,
                    lect_pk=freq.lecture.pk,
                    lect_theme=freq.lecture.theme,
                    lect_type=str(
                        [lt[1] for lt in LECTURE_TYPES if lt[0] == obj.type][0]
                    ),
                    lect_date=freq.lecture.date,
                    lect_center=str(freq.lecture.center),
                    seek_pk=freq.seeker.pk,
                    seek_name=freq.seeker.short_name,
                    seek_birth=freq.seeker.birth,
                    seek_gender=freq.seeker.gender,
                    seek_city=freq.seeker.city,
                    seek_state=freq.seeker.state,
                    seek_country=freq.seeker.country,
                    seek_local="{} ({}-{})".format(
                        freq.seeker.city,
                        freq.seeker.state,
                        freq.seeker.country,
                    ),
                    seek_center=str(freq.seeker.center),
                    seek_status=str(
                        [
                            stt[1]
                            for stt in SEEKER_STATUS
                            if stt[0] == freq.seeker.status
                        ][0]
                    ),
                    seek_status_date=freq.seeker.status_date,
                )
                _dict.append(row)
    return _dict


def get_seekers_dict(request, model):
    queryset = queryset_per_status(request, model)
    _dict = []
    for obj in queryset:
        row = dict(
            pk=obj.pk,
            name=obj.short_name,
            birth=obj.birth,
            gender=obj.gender,
            city=obj.city,
            state=obj.state,
            country=obj.country,
            local="{} ({}-{})".format(obj.city, obj.state, obj.country),
            center=str(obj.center),
            status=str(
                [stt[1] for stt in SEEKER_STATUS if stt[0] == obj.status][0]
            ),
            status_date=obj.status_date,
        )
        _dict.append(row)
    return _dict

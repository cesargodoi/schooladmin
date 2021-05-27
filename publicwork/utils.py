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


# reports
def get_lectures_big_dict(request, Table):
    big_dict = []
    for obj in queryset_per_date(request, Table):
        row = dict(
            lect_pk=obj.pk,
            lect_date=obj.date,
            lect_theme=obj.theme,
            lect_type=str(
                [lt[1] for lt in LECTURE_TYPES if lt[0] == obj.type][0]
            ),
            lect_listeners=obj.listener_set.count(),
            lect_center=str(obj.center),
            lect_center_city=obj.center.city,
            lect_center_state=obj.center.state,
            lect_center_country=obj.center.country,
        )
        big_dict.append(row)
    return big_dict


def get_frequencies_big_dict(request, model):
    big_dict = []
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
                    seek_historic=str(
                        [
                            h[1]
                            for h in SEEKER_STATUS
                            if h[0]
                            == freq.seeker.historic_set.last().occurrence
                        ][0]
                    ),
                    seek_historic_date=freq.seeker.historic_set.last().date,
                )
                big_dict.append(row)
    return big_dict


def get_status_big_dict(request, model):
    queryset = queryset_per_status(request, model)
    big_dict = []
    for obj in queryset:
        row = dict(
            seek_pk=obj.pk,
            seek_name=obj.short_name,
            seek_birth=obj.birth,
            seek_gender=obj.gender,
            seek_city=obj.city,
            seek_state=obj.state,
            seek_country=obj.country,
            seek_local="{} ({}-{})".format(
                obj.city,
                obj.state,
                obj.country,
            ),
            seek_center=str(obj.center),
            seek_historic=str(
                [
                    h[1]
                    for h in SEEKER_STATUS
                    if h[0] == obj.historic_set.last().occurrence
                ][0]
            ),
            seek_historic_date=obj.historic_set.last().date,
        )
        big_dict.append(row)
    return big_dict


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
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return model.objects.filter(query).order_by("name_sa")

import pandas as pd

from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone


def seeker_search(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "name": "",
            "city": "",
            "center": "",
            "page": 1,
            "all": "",
        }
    # adjust search
    search = request.session["search"]
    if request.GET.get("page"):
        search["page"] = request.GET["page"]
    else:
        search["page"] = 1
        search["name"] = request.GET["name"] if request.GET.get("name") else ""
        search["city"] = request.GET["city"] if request.GET.get("city") else ""
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
        Q(name_sa__icontains=search["name"]),
    ]
    # adding more complexity
    if search["city"]:
        _query.append(Q(city__icontains=search["city"]))
    if search["center"]:
        _query.remove(Q(center=request.user.person.center))
        _query.append(Q(center__name__icontains=search["center"]))
    if search["all"]:
        _query.remove(Q(is_active=True))
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
            "page": "",
            "dt1": "",
            "dt2": "",
            "type": "CTT",
            "all": "",
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

    return (
        obj.objects.filter(query).order_by("-date"),
        search["page"],
    )


# reports
def get_dataframe(request, Table):
    big_dict = []
    for obj in queryset_per_date(request, Table):
        for freq in obj.listener_set.all():
            row = dict(
                id=freq.id,
                ranking=freq.ranking,
                observations=freq.observations,
                lecture_id=freq.lecture.pk,
                lecture_theme=freq.lecture.theme,
                lecture_type=freq.lecture.type,
                lecture_date=freq.lecture.date,
                lecture_center=freq.lecture.center.name,
                lecture_center_country=freq.lecture.center.country,
                seeker_id=freq.seeker.id,
                seeker_name=freq.seeker.name,
                seeker_birth=freq.seeker.birth,
                seeker_gender=freq.seeker.gender,
                seeker_city=freq.seeker.city,
                seeker_country=freq.seeker.country,
                seeker_center=freq.seeker.center.name,
                seeker_center_country=freq.seeker.center.country,
            )
            big_dict.append(row)
    return pd.DataFrame(big_dict)


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

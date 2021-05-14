import json
from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from schooladmin.common import LECTURE_TYPES

from ..models import Lecture
from ..utils import get_dataframe


@login_required
@permission_required("publicwork.view_lecture")
def publicwork_home(request):
    context = {"title": "Public work"}
    return render(request, "publicwork/publicwork_home.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def frequencies_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        # generate a pandas dataframe
        dataframe = get_dataframe(request, Lecture)
        # count frequencies and insert on each row as lectures column
        dataframe["lectures"] = dataframe.groupby("seeker_id")[
            "seeker_name"
        ].transform("count")
        # select columns to report
        columns = [
            "seeker_id",
            "seeker_name",
            "seeker_city",
            "seeker_country",
            "seeker_center",
            "seeker_center_country",
            "lectures",
        ]
        # generate a new data frame with the sum of ranking column
        set_the_target = (
            dataframe.groupby(columns)
            .sum("ranking")
            .sort_values("ranking", ascending=False)
        )
        # drop unnecessary columns
        report_data = set_the_target.drop(columns=["id", "lecture_id"])
        # convert to json
        to_json = report_data.reset_index().to_json(orient="records")
        frequencies_per_period = json.loads(to_json)

        context = {
            "title": "frequencies per period",
            "object_list": frequencies_per_period,
        }

        return render(
            request, "publicwork/reports/frequencies_per_period.html", context
        )

    context = {"title": "frequencies per period"}

    return render(
        request, "publicwork/reports/frequencies_per_period.html", context
    )


@login_required
@permission_required("publicwork.view_lecture")
def lectures_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        # generate a pandas dataframe
        dataframe = get_dataframe(request, Lecture)
        # count seekers and insert on each row as listeners column
        dataframe["listeners"] = dataframe.groupby("lecture_id")[
            "lecture_theme"
        ].transform("count")
        # select columns to report
        columns = [
            "lecture_id",
            "lecture_theme",
            "lecture_type",
            "lecture_date",
            "lecture_center",
            "lecture_center_country",
            "listeners",
        ]
        # generate a new data frame grouping by lectures
        set_the_target = (
            dataframe.groupby(columns)
            .mean()
            .sort_values("listeners", ascending=False)
        )
        # drop unnecessary columns
        report_data = set_the_target.drop(
            columns=["id", "ranking", "seeker_id"]
        )
        # convert to json
        to_json = report_data.reset_index().to_json(orient="records")
        lectures_per_period = json.loads(to_json)

        for lecture in lectures_per_period:
            lecture["lecture_type"] = [
                x[1] for x in LECTURE_TYPES if x[0] == lecture["lecture_type"]
            ][0]
            lecture["lecture_date"] = datetime.utcfromtimestamp(
                lecture["lecture_date"] // 1e3
            ).date()

        context = {
            "title": "lectures per period",
            "object_list": lectures_per_period,
        }

        return render(
            request, "publicwork/reports/lectures_per_period.html", context
        )

    context = {"title": "lectures per period"}

    return render(
        request, "publicwork/reports/lectures_per_period.html", context
    )

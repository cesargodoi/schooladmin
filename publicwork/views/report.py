import json
import pandas as pd
from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from ..models import Lecture
from ..utils import get_frequencies_big_dict, get_lectures_big_dict
from schooladmin.common import SEEKER_STATUS


@login_required
@permission_required("publicwork.view_lecture")
def publicwork_home(request):
    context = {"title": "Public work"}
    return render(request, "publicwork/publicwork_home.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def frequencies_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        # get frequencies big dict
        big_dict = get_frequencies_big_dict(request, Lecture)
        # select columns to report
        columns = [
            "seek_pk",
            "seek_name",
            "seek_local",
            "seek_center",
            "seek_historic",
        ]
        # generate pandas dataframe
        dataframe = pd.DataFrame(big_dict, columns=columns + ["ranking"])
        # count frequencies and insert on each row as lectures column
        dataframe["lectures"] = dataframe.groupby("seek_pk")[
            "seek_name"
        ].transform("count")
        # .sort_values('ranking', ascending=False)
        report_data = (
            dataframe.groupby(columns + ["lectures"])
            .sum("ranking")
            .sort_values("ranking", ascending=False)
            .reset_index()
        )
        # adjust session
        search = request.session["search"]
        search["status"] = (
            request.GET["status"] if request.GET.get("status") else ""
        )
        request.session.modified = True
        # filter report_data
        if search["status"]:
            filter = report_data["seek_historic"] == search["status"]
            report_data = report_data[filter]
        # convert to json
        to_json = report_data.reset_index().to_json(orient="records")

        context = {
            "title": "frequencies per period",
            "object_list": json.loads(to_json),
            "status": SEEKER_STATUS,
            "dt1": datetime.strptime(request.GET["dt1"], "%Y-%m-%d"),
            "dt2": datetime.strptime(request.GET["dt2"], "%Y-%m-%d"),
        }

        return render(
            request, "publicwork/reports/frequencies_per_period.html", context
        )

    context = {"title": "frequencies per period", "status": SEEKER_STATUS}

    return render(
        request, "publicwork/reports/frequencies_per_period.html", context
    )


@login_required
@permission_required("publicwork.view_lecture")
def lectures_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        context = {
            "title": "lectures per period",
            "object_list": get_lectures_big_dict(request, Lecture),
        }
        return render(
            request, "publicwork/reports/lectures_per_period.html", context
        )

    context = {"title": "lectures per period"}

    return render(
        request, "publicwork/reports/lectures_per_period.html", context
    )


# @login_required
# @permission_required("publicwork.view_seeker")
# def seekers_per_status(request):
#     if request.GET.get("dt1") and request.GET.get("dt2"):
#         # generate a pandas dataframe
#         dataframe = get_dataframe(request, Lecture)
#         # count frequencies and insert on each row as lectures column
#         dataframe["lectures"] = dataframe.groupby("seek_id")[
#             "seek_name"
#         ].transform("count")
#         # select columns to report
#         columns = [
#             "seek_id",
#             "seek_name",
#             "seek_local",
#             "seek_center",
#             "seek_historic",
#             "lectures",
#         ]
#         # generate a new data frame with the sum of ranking column
#         set_the_target = (
#             dataframe.groupby(columns)
#             .sum("ranking")
#             .sort_values("ranking", ascending=False)
#         )
#         # drop unnecessary columns
#         report_data = set_the_target.drop(columns=["id", "lect_id"])
#         # convert to json
#         to_json = report_data.reset_index().to_json(orient="records")
#         frequencies_per_period = json.loads(to_json)

#         context = {
#             "title": "frequencies per period",
#             "object_list": frequencies_per_period,
#         }

#         return render(
#             request, "publicwork/reports/frequencies_per_period.html", context
#         )

#     context = {"title": "seekers per status"}

#     return render(
#         request, "publicwork/reports/seekers_per_status.html", context
#     )

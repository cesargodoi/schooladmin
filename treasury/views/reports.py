from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from person.models import Person
from schooladmin.common import paginator

from .useful import OrderByPeriod, OrderToJson


def vue_get_order(request):
    if request.is_ajax and request.method == "GET":
        order = OrderToJson(request.GET.get("order_id"))
        return JsonResponse(order.json, safe=False)


@login_required
def treasury_home(request):
    # clear session
    if request.session.get("order"):
        del request.session["order"]
    if request.session.get("search"):
        del request.session["search"]
    # create an object list
    object_list = OrderByPeriod(
        request,
        timezone.now().date() - timedelta(30),
        timezone.now().date(),
    )

    last_payments, last_payments_total = object_list.summary("concluded")
    self_payed, self_payed_total = object_list.summary("self_payed")

    context = {
        "last_payments": last_payments,
        "last_payments_total": last_payments_total,
        "self_payed": len(self_payed),
        "self_payed_total": self_payed_total,
        "title": "Treasury",
    }
    return render(request, "treasury/treasury_home.html", context)


@login_required
def cash_balance(request):
    search = search_dates(request)
    date1 = (
        datetime.strptime(request.GET["date1"], "%Y-%m-%d")
        if request.GET.get("date1")
        else datetime.strptime(search["date1"], "%Y-%m-%d")
    )
    search["date1"] = date1.strftime("%Y-%m-%d")
    date2 = (
        datetime.strptime(request.GET["date2"], "%Y-%m-%d")
        if request.GET.get("date2")
        else datetime.strptime(search["date2"], "%Y-%m-%d")
    )
    search["date2"] = date2.strftime("%Y-%m-%d")
    # get an object list
    object_list = OrderByPeriod(request, date1, date2)
    last_payments, last_payments_total = object_list.summary("concluded")

    context = {
        "last_payments": last_payments,
        "last_payments_total": last_payments_total,
        "period": "from {} to {}".format(
            date1.strftime("%d/%m/%y"), date2.strftime("%d/%m/%y")
        ),
        "object_list": object_list.all_payforms,
        "title": "Cash Balance",
    }
    return render(request, "treasury/reports/cash_balance.html", context)


@login_required
def period_payments(request):
    search = search_dates(request)
    date1 = (
        datetime.strptime(request.GET["date1"], "%Y-%m-%d")
        if request.GET.get("date1")
        else datetime.strptime(search["date1"], "%Y-%m-%d")
    )
    search["date1"] = date1.strftime("%Y-%m-%d")
    date2 = (
        datetime.strptime(request.GET["date2"], "%Y-%m-%d")
        if request.GET.get("date2")
        else datetime.strptime(search["date2"], "%Y-%m-%d")
    )
    search["date2"] = date2.strftime("%Y-%m-%d")
    # get an object list
    object_list = OrderByPeriod(request, date1, date2)
    payments, payments_total = object_list.summary_of_payments()

    context = {
        "last_payments": payments,
        "last_payments_total": payments_total,
        "period": "from {} to {}".format(
            date1.strftime("%d/%m/%y"), date2.strftime("%d/%m/%y")
        ),
        "object_list": object_list.all_payments,
        "title": "Period payments",
    }
    return render(request, "treasury/reports/period_payments.html", context)


@login_required
def payments_by_person(request):
    if not request.session.get("order"):
        request.session["order"] = {
            "person": {},
            "payments": [],
            "payforms": [],
            "total_payments": 0.0,
            "total_payforms": 0.0,
            "missing": 0.0,
            "status": None,
            "description": "",
            "self_payed": False,
        }

    person = None
    object_list = []

    if request.GET.get("person"):
        person = Person.objects.get(name=request.GET.get("person"))
        request.session["order"]["person"] = {
            "name": person.name,
            "id": str(person.id),
        }
        request.session.modified = True
        payments = person.payment_set.all().order_by("-created_on")
        object_list = paginator(payments, page=request.GET.get("page"))
    elif request.session["order"]["person"]:
        person = Person.objects.get(
            id=request.session["order"]["person"]["id"]
        )
        payments = person.payment_set.all().order_by("-created_on")

        object_list = paginator(payments, page=request.GET.get("page"))

    context = {
        "title": "Payment by person",
        "object": person,
        "object_list": object_list,
    }
    return render(request, "treasury/reports/payments_by_person.html", context)


# helpers
# get person by jQuery
def reports_search_person(request):
    if request.is_ajax():
        term = request.GET.get("term")
        persons = Person.objects.filter(
            name__icontains=term, center=request.user.person.center
        )[:20]
        results = [person.name for person in persons]
        return JsonResponse(results, safe=False)

    return render(request, "treasury/reports/payment_by_person.html")


# search dates
def search_dates(request):
    if not request.session.get("search"):
        request.session["search"] = {
            "date1": (timezone.now().date() - timedelta(30)).strftime(
                "%Y-%m-%d"
            ),
            "date2": timezone.now().date().strftime("%Y-%m-%d"),
        }
    return request.session["search"]

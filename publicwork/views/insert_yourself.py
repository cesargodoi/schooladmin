import requests

from datetime import datetime, timedelta

from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings

from user.models import User
from ..forms import TempRegOfSeekerForm
from ..models import TempRegOfSeeker, Seeker
from schooladmin.common import clear_session, send_email


def insert_yourself(request):
    clear_session(request, ["fbk"])
    if request.method == "POST":
        # reCAPTCHA validation
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify", data=data
        )
        result = r.json()
        # if reCAPTCHA returns False
        if not result["success"]:
            request.session["fbk"] = {"type": "recaptcha"}
            return redirect("feedback")

        # checking if the email has already been used in the User
        if User.objects.filter(email=request.POST.get("email")):
            request.session["fbk"] = {
                "type": "pupil",
                "email": request.POST.get("email"),
            }
            return redirect("feedback")

        # checking if the email has already been used in the Seeker
        if Seeker.objects.filter(email=request.POST.get("email")):
            request.session["fbk"] = {
                "type": "seeker",
                "email": request.POST.get("email"),
            }
            return redirect("feedback")

        # checking if the email has already been used in the TempRegOfSeeker
        if TempRegOfSeeker.objects.filter(email=request.POST.get("email")):
            request.session["fbk"] = {
                "type": "email",
                "email": request.POST.get("email"),
            }
            return redirect("feedback")

        # populating form with request.POST
        form = TempRegOfSeekerForm(request.POST, request.FILES)

        if form.is_valid():
            # save form data in TempRegOfSeeker table
            form.save()
            # get temp_seeker using email (in form cleaned_data)
            _seeker = TempRegOfSeeker.objects.get(
                email=form.cleaned_data.get("email")
            )
            # send email
            send_email(
                link=reverse("confirm_email", args=[_seeker.id]),
                text="publicwork/insert_yourself/emails/to_confirm.txt",
                html="publicwork/insert_yourself/emails/to_confirm.html",
                _subject="confirmação de email",
                _to=_seeker.email,
                _extras={"name": _seeker.name},
            )

        request.session["fbk"] = {
            "type": "email",
            "email": request.POST.get("email"),
        }
        return redirect("feedback")

    context = {
        "form": TempRegOfSeekerForm(),
        "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
        "form_name": "Seeker",
        "form_path": "publicwork/forms/seeker.html",
        "goback": reverse("seeker_home"),
        "title": "create seeker",
        "to_create": True,
    }
    return render(request, "publicwork/insert_yourself/form.html", context)


def feedback(request):
    context = {"title": "insert yourself as a seeker"}
    return render(
        request, "publicwork/insert_yourself/form_feedback.html", context
    )


def confirm_email(request, token):
    _seeker = get_object_or_404(TempRegOfSeeker, pk=token)
    # get dates
    time_now = datetime.utcnow()
    token_time = _seeker.solicited_on.replace(tzinfo=None) + timedelta(hours=6)

    if time_now < token_time:
        new_seeker = dict(
            name=_seeker.name,
            birth=_seeker.birth,
            gender=_seeker.gender,
            image=_seeker.image,
            city=_seeker.city,
            state=_seeker.state,
            country=_seeker.country,
            phone=_seeker.phone,
            email=_seeker.email,
        )
        Seeker.objects.create(**new_seeker)
        _seeker.delete()
        context = {"feedback": "congratulations"}
    else:
        context = {"feedback": "token_expires"}

    return render(
        request, "publicwork/insert_yourself/pos_email_feedback.html", context
    )

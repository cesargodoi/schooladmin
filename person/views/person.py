from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from schooladmin.common import ASPECTS, STATUS, paginator
from user.models import User

from ..forms import PersonForm, ProfileForm, UserForm
from ..models import Historic, Person


@login_required
@permission_required("person.view_person")
def person_home(request):
    queryset, page = person_search(request)
    object_list = paginator(queryset, page=page)

    context = {
        "object_list": object_list,
        "aspect_list": ASPECTS,
        "status_list": STATUS,
        "title": "person home",
    }

    return render(request, "person/person_home.html", context)


@login_required
@permission_required("person.view_person")
def person_detail(request, id):
    center_persons = [
        person.id
        for person in Person.objects.filter(
            center=request.user.person.center.id
        )
    ]
    if id not in center_persons and not request.user.is_superuser:
        raise Http404
    person = get_object_or_404(Person, id=id)

    context = {
        "object": person,
        "title": "person detail",
        "person": person,  # to header element
    }
    return render(request, "person/person_detail.html", context)


@login_required
@permission_required("person.add_person")
def person_create(request):
    if request.method == "POST":
        # creating a new user
        password = BaseUserManager().make_random_password()
        email = request.POST["email"]
        new_user = User.objects.create_user(
            email=email,
            password=password,
        )
        # updating the user.profile
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=new_user.profile
        )
        if profile_form.is_valid():
            profile_form.save()
        # updating the user.person
        person_form = PersonForm(request.POST, instance=new_user.person)
        if person_form.is_valid():
            person_form.save()
        # add password in observations
        new_user.person.observations += f"\nfirst password: {password}"
        # the center is the same as the center of the logged in user
        new_user.person.center = request.user.person.center
        new_user.person.save()
        message = f"The Person '{request.POST['name']}' has been created!"
        messages.success(request, message)
        return redirect("person_home")

    user_form = UserForm()
    profile_form = ProfileForm()
    person_form = PersonForm(initial={"made_by": request.user})

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "person_form": person_form,
        "title": "create person",
        "to_create": True,
    }
    return render(request, "person/person_form.html", context)


@login_required
@permission_required("person.change_person")
def person_update(request, id):
    center_persons = [
        person.id
        for person in Person.objects.filter(
            center=request.user.person.center.pk
        )
    ]
    if id not in center_persons and not request.user.is_superuser:
        raise Http404

    person = get_object_or_404(Person, id=id)
    if request.method == "POST":
        # updating the user
        user_form = UserForm(request.POST, instance=person.user)
        if user_form.is_valid():
            user_form.save()

        # updating the user.profile
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=person.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()

        # updating the user.person
        person_form = PersonForm(request.POST, instance=person)
        if person_form.is_valid():
            person_form.save()
            message = f"The Person '{request.POST['name']}' has been updated!"
            messages.success(request, message)

        return redirect("person_detail", id=id)

    user_form = UserForm(instance=person.user)
    profile_form = ProfileForm(instance=person.user.profile)
    person_form = PersonForm(
        instance=person, initial={"made_by": request.user}
    )

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "person_form": person_form,
        "title": "update person",
        "id": id,
    }
    return render(request, "person/person_form.html", context)


@login_required
@permission_required("person.delete_person")
def person_delete(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == "POST":
        if person.historic_set.all():
            person.user.is_active = False
            person.user.save()
            person.is_active = False
            person.status = "REM"
            person.save()
            add_historic(person, "REM", request.user)
        else:
            person.user.delete()
        return redirect("person_home")

    context = {"object": person, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


@login_required
@permission_required("person.add_person")
def person_reinsert(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == "POST":
        person.user.is_active = True
        person.user.save()
        person.is_active = True
        person.status = "ACT"
        person.save()
        add_historic(person, "ACT", request.user)
        return redirect("person_home")

    context = {"object": person, "title": "confirm to reinsert"}
    return render(
        request, "person/elements/confirm_to_reinsert_person.html", context
    )


# auxiliar functions
def person_search(request):
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
    if request.GET.get("page"):
        search["page"] = request.GET["page"]
    else:
        search["page"] = 1
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

    return Person.objects.filter(query).order_by("name_sa"), search["page"]


def add_historic(person, occurrence, made_by):
    historic = dict(
        person=person,
        occurrence=occurrence,
        date=timezone.now().date(),
        made_by=made_by,
    )
    Historic.objects.create(**historic)

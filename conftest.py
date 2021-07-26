import pytest
from pytest_factoryboy import register
from django.contrib.auth.models import Group, Permission
from factories import (
    fake,
    UserFactory,
    CenterFactory,
    TempRegOfSeeker,
    SeekerFactory,
)

register(UserFactory)
register(CenterFactory)
register(TempRegOfSeeker)
register(SeekerFactory)


@pytest.fixture
def get_password():
    return "secret"


@pytest.fixture
def create_user(db, django_user_model, get_password):
    def make_user(**kwargs):
        kwargs["email"] = kwargs.get("email") or fake.email()
        kwargs["password"] = kwargs.get("password") or get_password
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, get_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(email=user.email, password=get_password)
        return client, user

    return make_auto_login


#  Groups and Permissions
@pytest.fixture
def get_group(db, get_perms):
    def make_group(name):
        group = Group.objects.create(name=name)
        perms = get_perms[name]
        group.permissions.set(perms)
        group.save()
        return group

    return make_group


@pytest.fixture
def get_perms(db):
    perms = {
        "user": [
            # user and profile
            Permission.objects.get(codename="view_user"),
            Permission.objects.get(codename="change_user"),
            Permission.objects.get(codename="view_profile"),
            Permission.objects.get(codename="change_profile"),
        ],
        "office": [
            # center
            Permission.objects.get(codename="view_center"),
            Permission.objects.get(codename="change_center"),
            # event
            Permission.objects.get(codename="add_event"),
            Permission.objects.get(codename="change_event"),
            Permission.objects.get(codename="delete_event"),
            Permission.objects.get(codename="view_event"),
            # historic
            Permission.objects.get(codename="add_historic"),
            Permission.objects.get(codename="change_historic"),
            Permission.objects.get(codename="delete_historic"),
            Permission.objects.get(codename="view_historic"),
            # person
            Permission.objects.get(codename="add_person"),
            Permission.objects.get(codename="change_person"),
            Permission.objects.get(codename="delete_person"),
            Permission.objects.get(codename="view_person"),
            # membership
            Permission.objects.get(codename="add_membership"),
            Permission.objects.get(codename="change_membership"),
            Permission.objects.get(codename="delete_membership"),
            Permission.objects.get(codename="view_membership"),
            # workgroup
            Permission.objects.get(codename="add_workgroup"),
            Permission.objects.get(codename="change_workgroup"),
            Permission.objects.get(codename="delete_workgroup"),
            Permission.objects.get(codename="view_workgroup"),
        ],
        "treasury": [
            # center
            Permission.objects.get(codename="view_center"),
            # person
            Permission.objects.get(codename="view_person"),
            # order
            Permission.objects.get(codename="add_order"),
            Permission.objects.get(codename="change_order"),
            Permission.objects.get(codename="delete_order"),
            Permission.objects.get(codename="view_order"),
        ],
        "treasury_jr": [
            # center
            Permission.objects.get(codename="view_center"),
            # person
            Permission.objects.get(codename="view_person"),
            # order
            Permission.objects.get(codename="add_order"),
            Permission.objects.get(codename="view_order"),
        ],
    }
    return perms

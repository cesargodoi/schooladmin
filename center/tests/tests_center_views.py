import pytest
from django.urls import reverse


center_home = reverse("center_home")


"""
unlogged person cannot access any page of center app
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    "_type",
    [("home"), ("detail"), ("create"), ("update"), ("delete")],
)
def test_unlogged_person_cannot_view_center_pages(
    center_factory, client, _type
):
    center = center_factory.create()
    page = f"center_{_type}"
    if _type in ("update", "detail", "delete"):
        url = reverse(page, args=[str(center.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


"""
- user cannot access center home
- office, treasury and treasury_jr can
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 200), ("treasury_jr", 200)],
)
def test_access_center_home_by_user_types(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    center_factory.create()
    client, user = auto_login_user()
    group = get_group(user_type)
    user.groups.add(group)
    url = reverse("center_home")
    response = client.get(url)
    assert response.status_code == status_code


"""
- user cannot access center detail
- office, treajury and treasury_jr can 
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 200), ("treasury_jr", 200)],
)
def test_access_center_detail_by_user_types(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    center = center_factory.create()
    client, user = auto_login_user()
    group = get_group(user_type)
    user.groups.add(group)
    url = reverse("center_detail", args=[center.pk])
    response = client.get(url)
    assert response.status_code == status_code


"""
- user, treasury and treasury_jr cannot access center update
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access_center_update_by_user_types(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    center = center_factory.create()
    client, user = auto_login_user()
    group = get_group(user_type)
    user.groups.add(group)
    url = reverse("center_update", args=[center.pk])
    response = client.get(url)
    assert response.status_code == status_code


"""
- office can access center update of only own center
"""


@pytest.mark.django_db
def test_access_center_update_by_offices_own_center(
    center_factory, auto_login_user, get_group
):
    center = center_factory.create()
    client, user = auto_login_user()
    user.person.center = center
    user.groups.add(get_group("office"))
    url = reverse("center_update", args=[center.pk])
    response = client.get(url)
    assert response.status_code == 200


"""
- user, office, treasury and treasury_jr cannot access center update
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 302), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access_center_create_by_user_types(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    center = center_factory.create()
    client, user = auto_login_user()
    group = get_group(user_type)
    user.groups.add(group)
    url = reverse("center_create")
    response = client.get(url)
    assert response.status_code == status_code


"""
- user, office, treasury and treasury_jr cannot access center delete
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 302), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access_center_delete_by_user_types(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    center = center_factory.create()
    client, user = auto_login_user()
    group = get_group(user_type)
    user.groups.add(group)
    url = reverse("center_delete", args=[center.pk])
    response = client.get(url)
    assert response.status_code == status_code


"""
- user cannot search center
- office, treasury and treasury_jr can
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 200), ("treasury_jr", 200)],
)
def test_search_center_home_by_user_types(
    auto_login_user, get_group, user_type, status_code
):
    client, user = auto_login_user()
    group = get_group(user_type)
    user.groups.add(group)
    url = "/center/?term=Group"
    response = client.get(url)
    assert response.status_code == status_code

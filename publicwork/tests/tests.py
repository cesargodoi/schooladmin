import pytest
from center.models import Center


@pytest.mark.django_db
def test_try_to_create_center(center_factory):
    center_factory.create()
    assert Center.objects.count() == 1


@pytest.mark.django_db
def test_verify_if_profile_is_created(center_factory):
    center = center_factory.create()
    secretary = center.secretary
    assert secretary.profile.social_name.startswith("<<")


@pytest.mark.django_db
def test_verify_if_person_is_created(center_factory):
    center = center_factory.create()
    secretary = center.secretary
    assert "REQUIRES ADJUSTMENTS" in secretary.person.name

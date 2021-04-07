from datetime import date
from django.utils import timezone
from django.contrib import auth
from user.models import User
from person.models import (
    Historic,
    Person,
)
from person.tests.dummy import PersonDummy


class TestPerson(PersonDummy):
    def test_list_persons(self):
        self.assertEqual(Person.objects.count(), 8)

    def test_search_person(self):
        person = Person.objects.filter(name__icontains="Office One").first()
        self.assertIn("0001", person.reg)
        

    def test_create_person(self):
        # The Profile and Person classes are linked (one-to-one) to the
        # User class.  When we create a User instance, a Profile and a Person
        # instances are created automatically and linked to the User instance.
        new_user = User.objects.create_user(
            email="new.user@rcad.min",
            password="asdf1234",
        )
        new = dict(
            name="New Úser",
            center=self.center_1,
            reg="0004",
            person_type="WEB",
            made_by=self.office1,
        )
        new_person = Person.objects.get(user=new_user)
        for attr, value in new.items():
            setattr(new_person, attr, value)
        new_person.save()
        self.assertEqual(Person.objects.count(), 9)
        # 'name_sa' is equal to the 'name' field without graphic accents
        # (ÁáÔôÃã ...).  This field is automatically calculated when the
        # Person instance is saved
        self.assertEqual("new user", new_person.name_sa)
        self.assertEqual("0004", new_person.reg)

    def test_update_person_type(self):
        # we have 8 person and 1 was updated for "web" type.
        person = Person.objects.get(name="Office One")
        person.person_type = "WEB"
        person.save()
        self.assertEqual(Person.objects.filter(person_type="PUP").count(), 7)

    def test_update_person_name(self):
        new_user = User.objects.create_user(
            email="new.user@rcad.min",
            password="asdf1234",
        )
        self.assertEqual(Person.objects.filter(name__icontains="REQUIRES ADJUSTMENTS").count(),1)
        new = dict(
            name="New Úser",
            center=self.center_1,
            reg="0004",
            person_type="WEB",
            made_by=self.office1,
        )
        new_person = Person.objects.get(user=new_user)
        for attr, value in new.items():
            setattr(new_person, attr, value)
        new_person.save()
        self.assertEqual(Person.objects.filter(name__icontains="New").count(),1)
        self.assertEqual(new_person.name_sa, "new user") #metodo save: nome sem acento
        self.assertEqual(new_person.short_name, "Úser") #metodo save: nome curto

    def test_delete_person(self):
        Person.objects.filter(name="Office Two").delete()
        self.assertEqual(Person.objects.count(), 7)

    def test_update_person_is_active_then_update_user_is_active_too(self):
        # vice versa também
        new_user = User.objects.create_user(
            email="new.user@rcad.min",
            password="asdf1234",
        )
        self.assertTrue(new_user.is_active)
        new_person = Person.objects.filter(name__icontains="new.user").first()
        self.assertTrue(new_person.is_active)

        #new_user é desativado então new_person também.
        new_user.is_active = False
        new_user.save()
        new_person = Person.objects.filter(name__icontains="New").first()
        self.assertFalse(new_user.is_active)
        self.assertFalse(new_person.is_active)

        #new_person é ativado então new_user também.
        new_person.is_active = True
        new_person.save()
        new_user = User.objects.get(email__icontains="new")
        self.assertTrue(new_user.is_active)

    # # historics
    def test_list_historics(self):
        self.assertEqual(Historic.objects.count(), 1)

    def test_insert_historic(self):
        new = Historic.objects.create(
            person=self.person_2,
            occurrence="REM",
            date=timezone.now(),
            made_by=self.office1,
        )
        self.assertEqual(Historic.objects.count(), 2)

    def test_update_historic_status_and_person_is_update(self):
        new_status = "LIC" #person stay active
        historic = Historic.objects.get(id=1)
        historic.occurrence = new_status
        historic.save()
        person = Person.objects.get(name="Office One")
        self.assertIn("LIC", str(person.historic_set.first()))


    def test_update_historic_aspects_and_person_is_update(self):
        new_aspect = "A3"
        historic = Historic.objects.get(id=1)
        historic.occurrence = new_aspect
        historic.save()
        person = Person.objects.get(name="Office One")
        self.assertIn("A3", str(person.historic_set.first()))

    def test_update_person_status_and_verify_if_person_is_active(self):
        person = Person.objects.get(name="Office One")
        self.assertTrue(person.is_active)
        person.status = "DIS"
        person.clean()
        person.save()
        self.assertFalse(person.is_active)

    def test_delete_historic(self):
        Historic.objects.get(id=1).delete()
        self.assertEqual(Historic.objects.count(), 0)

from django.contrib import auth
from .dummy import UserDummy
from user.models import User, Profile
from person.models import Person


class TestUser(UserDummy):
    
    def test_user_dont_get_logged_in(self):
        #usuário não existe e quer logar.
        self.client.login(
            email="superuser@rcad.min",
            password="00000000",
        )
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated) 

    def test_user_get_logged_in(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_user_get_logged_out(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        assert user.is_authenticated
        self.client.logout()
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_list_profiles(self):
        self.assertEqual(Profile.objects.count(), 8)


    new_user = dict(
        email="new_user@gmail.com",
        password="$536wen.",
    )
    
    def test_add_new_user(self):
        User.objects.create_user(**self.new_user)
        self.assertEqual(User.objects.count(), 9)

    def test_add_new_user_and_verify_new_profile(self):
        User.objects.create_user(**self.new_user)
        self.assertEqual(Profile.objects.count(), 9)

    def test_add_new_user_and_verify_new_person(self):
        User.objects.create_user(**self.new_user)
        self.assertEqual(Person.objects.count(), 9)
        person = Person.objects.get(name__icontains="new_user")
        self.assertEqual(person.name, "<<new_user>> REQUIRES ADJUSTMENTS")

    def test_edit_user(self):
        User.objects.create_user(**self.new_user)
        user = User.objects.last()
        user.email = "new_user@hotmail.com"
        user.save()
        user_edited = User.objects.last()
        self.assertEqual(user_edited.email, "new_user@hotmail.com")

    def test_delete_user(self):
        User.objects.create_user(**self.new_user)
        self.assertEqual(User.objects.count(), 9)

        user_delete = User.objects.last()
        user_delete.delete()

        self.assertEqual(User.objects.count(), 8)

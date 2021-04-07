from django.test import TestCase
from django.contrib import auth

from user.tests.dummy import UserDummy
from user.models import User, Profile


class TestViews(UserDummy):

    def test_user_logged_in_can_access_profile(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/user/profile/detail/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/profile_detail.html")

    def test_user_logged_in_can_access_edit_profile(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/user/profile/update/")
        self.assertEqual(response.status_code, 200)

    def test_user_logged_in_can_access_user_historic(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/user/profile/historic/")
        self.assertEqual(response.status_code, 200)

    def test_user_logged_in_can_access_user_payments(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/user/profile/payments/")
        self.assertEqual(response.status_code, 200)

    def test_user_logged_in_can_access_user_payments_neworder(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/user/profile/new_order/")
        self.assertEqual(response.status_code, 200)

    def test_user_logged_in_can_access_user_frequencies(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/user/profile/frequencies/")
        self.assertEqual(response.status_code, 200)

    def test_user_logged_in_can_access_user_frequencies_scan_qrcode(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/user/profile/frequencies/scan_qrcode_event/")
        self.assertEqual(response.status_code, 200)

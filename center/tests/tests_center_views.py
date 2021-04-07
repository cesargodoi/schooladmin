from django.contrib import auth
from person.tests.dummy import PersonDummy
from center.models import Center
from django.shortcuts import get_object_or_404


class TestViewsFromDummies(PersonDummy):
    # center_list
    # office, treasury and treasuryjr can view center_list
    # user cannot view center_list
    def test_center_list_with_office_logged_in(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/center/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "center/center_home.html")

    def test_center_list_with_treasury_logged_in(self):
        # treasury can view the centers in center_list
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/center/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "center/center_home.html")

    def test_center_list_with_treasuryjr_logged_in(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/center/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "center/center_home.html")

    def test_center_list_with_user_logged_in(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/center/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/center/")

    # center_detail
    # office, treasury and treasuryjr can view center_detail
    # user cannot view center_detail
    def test_center_detail_logged_out_is_redirect_login_page(self):
            center = get_object_or_404(Center, name__icontains="Aquarius")  ######
            response = self.client.get(f"/center/{center.id}/detail/")  ########
            self.assertEqual(response.status_code, 302)
            self.assertIn("login", response.url)

    def test_center_detail_user_is_logged_in(self):
        self.client.login(
            email="user2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/detail/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/{center.id}/detail/")

    def test_center_detail_office_is_logged_in(self):
        self.client.login(
            email="office2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/detail/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "center/center_detail.html")

    def test_center_detail_treasury_is_logged_in(self):
        self.client.login(
            email="treasury2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/detail/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "center/center_detail.html")

    def test_center_detail_treasuryjr_is_logged_in(self):
        self.client.login(
            email="treasuryjr2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/detail/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "center/center_detail.html")

    # center_update
    # only superuser can edit center.
    def test_center_update_by_user(self):
        # user can not edit centers
        self.client.login(
            email="user2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/update/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/{center.id}/update/")

    def test_center_update_by_office(self):
        # office can not edit centers
        self.client.login(
            email="office2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/update/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/{center.id}/update/")

    def test_center_update_by_treasury(self):
        # office can not edit centers
        self.client.login(
            email="treasury2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/update/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/{center.id}/update/")

    def test_center_update_by_treasuryjr(self):
        # office can not edit centers
        self.client.login(
            email="treasuryjr2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/update/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/{center.id}/update/")

    # center_create
    # only superuser can create center.
    def test_center_create_by_user(self):
        # user can not create centers
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/center/create/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/center/create/")

    def test_center_create_by_office(self):
        # office can not create centers
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/center/create/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/center/create/")

    def test_center_create_by_treasury(self):
        # office can not create centers
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/center/create/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/center/create/")

    def test_center_create_by_treasuryjr(self):
        # office can not create centers
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/center/create/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/center/create/")

    # center_delete
    # only superuser can delete center.
    def test_center_delete_by_user(self):
        # user can not delete centers
        self.client.login(
            email="user2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/delete/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/{center.id}/delete/")

    def test_center_delete_by_office(self):
        # office can not delete centers
        self.client.login(
            email="office2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/delete/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/{center.id}/delete/")

    def test_center_delete_by_treasury(self):
        # office can not delete centers
        self.client.login(
            email="treasury2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/delete/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/{center.id}/delete/")

    def test_center_delete_by_treasuryjr(self):
        # office can not delete centers
        self.client.login(
            email="treasuryjr2@rcad.min",
            password="asdf1234",
        )
        center = get_object_or_404(Center, name__icontains="Campinas")  ######
        response = self.client.get(f"/center/{center.id}/delete/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/{center.id}/delete/")

    # center_search
    # office, treasury and treasuryjr can use center_search
    # user cannot view center_search
    def test_center_is_searchable_for_treasury_group(self):
        self.client.login(
            email="treasury2@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/center/?term=cAMp")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "center/center_home.html")
        self.assertIn("Campinas", response.content.decode())

    def test_center_is_searchable_for_treasuryjr_group(self):
        self.client.login(
            email="treasuryjr2@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/center/?term=cAMp")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "center/center_home.html")
        self.assertIn("Campinas", response.content.decode())

    def test_center_is_searchable_for_office_group(self):
        self.client.login(
            email="office2@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/center/?term=cAMp")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "center/center_home.html")
        self.assertIn("Campinas", response.content.decode())

    def test_center_is_searchable_for_user_group(self):
        self.client.login(
            email="user2@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/center/?term=cAMp")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/center/?term=cAMp")

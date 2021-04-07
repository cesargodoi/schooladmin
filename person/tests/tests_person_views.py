from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib import auth

from person.models import Person
from event.models import Event
from event.tests.dummy import EventDummy


class TestViews(TestCase):
    def test_user_logged_out_cannot_access_person(self):
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        response = self.client.get("/person/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)


class TestViewsFromDummies(EventDummy):
    # person_home
    ## testes de acessos
    def test_office_logged_in_can_access_person_home(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_home.html")
        # self.assertIn("2nd. Aspect", response.content.decode())

    def test_treasury_logged_in_can_access_person_home(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_home.html")
        # self.assertIn("2nd. Aspect", response.content.decode())

    def test_treasuryjr_logged_in_can_access_person_home(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_home.html")
        # self.assertIn("2nd. Aspect", response.content.decode())

    def test_user_logged_in_cannot_access_person_home(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # person_detail
    ## testes de acessos
    def test_office_can_access_persons_detail_from_his_center(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        person = get_object_or_404(Person, name__icontains="User One")  ######
        response = self.client.get(f"/person/{person.id}/detail/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_detail.html")
        # self.assertIn("Super User", response.content.decode())

    def test_office_can_not_access_person_detail_another_center(self):
        """
        If the "office" tries to access a person from another center,
        they will get 404 status code.
        """
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        person = get_object_or_404(Person, name__icontains="User Two")  ######
        response = self.client.get(f"/person/{person.id}/detail/")  ########
        self.assertIn("404", response.content.decode())
    
    def test_treasury_can_access_persons_detail_from_his_center(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        person = get_object_or_404(Person, name__icontains="User One")  ######
        response = self.client.get(f"/person/{person.id}/detail/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_detail.html")
        # self.assertIn("Super User", response.content.decode())

    def test_treasury_can_not_access_person_detail_another_center(self):
        """
        If the "treasury" tries to access a person from another center,
        they will get 404 status code.
        """
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        person = get_object_or_404(Person, name__icontains="User Two")  ######
        response = self.client.get(f"/person/{person.id}/detail/")  ########
        self.assertIn("404", response.content.decode())

    def test_treasuryjr_can_access_persons_detail_from_his_center(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        person = get_object_or_404(Person, name__icontains="User One")  ######
        response = self.client.get(f"/person/{person.id}/detail/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_detail.html")
        # self.assertIn("Super User", response.content.decode())

    def test_treasuryjr_can_not_access_person_detail_another_center(self):
        """
        If the "treasuryjr" tries to access a person from another center,
        they will get 404 status code.
        """
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        person = get_object_or_404(Person, name__icontains="User Two")  ######
        response = self.client.get(f"/person/{person.id}/detail/")  ########
        self.assertIn("404", response.content.decode())

    def test_user_can_not_view_person_detail(self):
        # verificar! User não pode ver nada além de seu profile. Então user não pode ver person_detail!
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/detail/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # person_create
    ## testes de acessos
    ### Only 'superuser' and 'office' can create a new 'person'.
    ### To create a new 'person', we need to create a new 'user'.
    ### When we create an 'user', a new 'profile' and 'person' are
    ### also created. So, we can use the 'user.profile' and 'user.person'
    ### relationship to update the 'profile' and 'person' instances.
    def test_office_is_logged_in_can_access_person_create(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/create/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_form.html")

    def test_treasury_logged_in_can_not_access_person_create(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/create/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_can_not_access_person_create(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/create/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_user_logged_in_can_not_access_person_create(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/create/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # person_update
    ## testes de acessos
    def test_office_logged_in_can_access_person_update(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")  ######
        response = self.client.get(f"/person/{person.id}/update/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_form.html")
    
    def test_treasury_logged_in_can_not_access_person_update(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/update/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_can_not_access_person_update(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/update/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_user_logged_in_can_not_access_person_update(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/update/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # person_delete
    ## testes de acessos
    def test_office_logged_in_can_delete_person(self):
        ## office pode apagar totalmente apenas users que não tem relações com outras tabelas.
        ## essa restrição é tratada por outras views.
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="User One")  ######
        response = self.client.get(f"/person/{person.id}/delete/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/confirm_delete.html")

    def test_treasury_logged_in_cannot_delete_person(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/delete/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_cannot_delete_person(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/delete/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_user_logged_in_cannot_delete_person(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/delete/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # person_search
    ## testes de acessos
    def test_office_can_see_person_for_any_centers_by_search(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/?term=user")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_home.html")
        self.assertIn("User", response.content.decode())

    def test_treasury_can_see_person_for_any_centers_by_search(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/?term=user")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_home.html")
        self.assertIn("User", response.content.decode())

    def test_treasuryjr_can_see_person_for_any_centers_by_search(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/?term=user")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_home.html")
        self.assertIn("User", response.content.decode())

    def test_user_cannot_see_person_for_any_centers_by_search(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/person/?term=office")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # person_reinsert
    ## testes de acessos
    def test_office_logged_in_can_reinsert_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="User One")  ######
        response = self.client.get(f"/person/{person.id}/reinsert/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/elements/confirm_to_reinsert_person.html")

    def test_treasury_logged_in_can_not_reinsert_person(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="User One")  ######
        response = self.client.get(f"/person/{person.id}/reinsert/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_can_not_reinsert_person(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="User One")  ######
        response = self.client.get(f"/person/{person.id}/reinsert/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_user_logged_in_can_not_reinsert_person(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury Junior One")  ######
        response = self.client.get(f"/person/{person.id}/reinsert/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    ###########################################################################
    #historic_view

    def test_office_logged_in_can_access_historic_list_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")  ######
        response = self.client.get(f"/person/{person.id}/historic")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/historic_list.html")
    
    def test_treasury_logged_in_can_not_access_historic_list_in_person(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/historic")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_can_not_access_historic_list_in_person(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/historic")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_office_logged_in_can_access_historic_create_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")  ######
        response = self.client.get(f'/person/{person.id}/historic/create/')  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/historic_form.html")

    def test_office_logged_in_can_access_historic_update_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")  ######
        response = self.client.get(f'/person/{person.id}/historic/1/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/historic_form.html")  

    def test_office_logged_in_can_access_historic_delete_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")  ######
        response = self.client.get(f'/person/{person.id}/historic/1/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/confirm_delete.html")

    ###########################################################################
    #frequency_ps_view

    def test_office_logged_in_can_access_frequency_list_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")  ######
        response = self.client.get(f"/person/{person.id}/frequencies")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/frequency_list.html")
    
    def test_treasury_logged_in_can_not_access_frequency_list_in_person(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/frequencies")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_can_not_access_frequency_list_in_person(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/frequencies")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_office_logged_in_can_access_frequency_create_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")  ######
        response = self.client.get(f'/person/{person.id}/frequency_insert')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/frequency_insert.html")

    def test_office_logged_in_can_access_frequency_delete_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")
        event = get_object_or_404(Event, id=1)
        response = self.client.get(f'/person/{person.id}/frequency/{event.id}/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/elements/confirm_to_delete_freq.html")

    ###########################################################################
    #membership_ps_view

    def test_office_logged_in_can_access_membership_list_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="User One")  ######
        response = self.client.get(f"/person/{person.id}/membership_ps/")  ########
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/membership_ps_list.html")
    
    def test_treasury_logged_in_can_not_access_membership_list_in_person(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/membership_ps/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_can_not_access_membership_list_in_person(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/person/{person.id}/membership_ps/")  ########
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_office_logged_in_can_access_membership_create_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")  ######
        response = self.client.get(f'/person/{person.id}/membership_ps/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/membership_ps_insert.html")

    def test_office_logged_in_can_access_membership_delete_in_person(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        person = get_object_or_404(Person, name__icontains="Treasury One")
        response = self.client.get(f'/person/{person.id}/membership_ps/{self.workgroup_membership_1.id}/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/elements/confirm_to_delete_member.html")

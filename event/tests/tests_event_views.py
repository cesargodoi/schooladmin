from event.models import Activity, Event
from event.tests.dummy import EventDummy
from django.contrib import auth


class ActivityViewTests(EventDummy):
    def test_activity_list(self):
        self.client.login(
            email="superuser@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("conference", response.content.decode())
        self.assertIn("service", response.content.decode())
        self.assertIn("contact", response.content.decode())

    def test_activity_create(self):
        self.client.login(
            email="superuser@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/create")
        self.assertEqual(response.status_code, 200)
        # response = self.client.post(
        #     "/event/activity/create", data={"activity": ""}
        # )
        # self.assertContains(response, "service")

    def test_activity_update(self):
        self.client.login(
            email="superuser@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/1/update")
        self.assertEqual(response.status_code, 200)
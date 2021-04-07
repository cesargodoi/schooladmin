from user.models import User
from center.models import Center
from center.tests.dummy import CenterDummy


class TestCenter(CenterDummy):
    def test_list_center(self):
        self.assertEqual(Center.objects.count(), 2)

    def test_add_new_center(self):
        new_center = dict(
            name="Pedra Angular",
            city="Jarinu",
            country="Brasil",
        )
        Center.objects.create(**new_center)
        self.assertEqual(Center.objects.count(), 3)

    def test_update_center_address_and_UF_format(self):
        center = Center.objects.get(name="Campinas")
        center.state = "ce"
        center.save()
        self.assertEqual(center.state, "CE")

    def test_update_phone_and_phone_format(self):
        center = Center.objects.get(name="Aquarius")
        center.phone_1 = "(11)3208-8682"
        center.phone_2 = "(11)987652143"
        center.save()
        self.assertEqual(center.phone_1, "11 3208.8682")
        self.assertEqual(center.phone_2, "11 98765.2143")

    def test_delete_center(self):
        center = Center.objects.get(name="Campinas")
        center.delete()
        self.assertEqual(Center.objects.count(), 1)

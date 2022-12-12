from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234",
            specialization="chef"
        )
        self.client.force_login(self.admin)
        self.cook = get_user_model().objects.create_user(
            username="user",
            password="user1234",
            specialization="assistant"
        )

    def test_cook_specialization_listed(self):
        url = reverse("admin:kitchen_service_cook_changelist")
        resp = self.client.get(url)

        self.assertContains(resp, self.cook.specialization)

    def test_cook_specialization_detailed(self):
        url = reverse("admin:kitchen_service_cook_change", args=[self.cook.id])
        resp = self.client.get(url)

        self.assertContains(resp, self.cook.specialization)

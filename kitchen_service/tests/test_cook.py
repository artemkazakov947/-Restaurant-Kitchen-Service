from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


COOK_LIST_URL = reverse("kitchen_service:cook-list")


class TestCook(TestCase):
    def setUp(self):
        self.cook = get_user_model().objects.create_user(
            username="cook_test",
            password="cook1234"
        )
        self.client.force_login(self.cook)
        num_cooks = 8
        for num in range(num_cooks):
            form_data = {
                "username": f"username_{num}",
                "password1": f"test12345{num}",
                "password2": f"test12345{num}",
                "first_name": f"First_name{num} test",
                "last_name": f"Last_name{num} test",
                "specialization": "assistant"
            }
            self.client.post(reverse("kitchen_service:cook-create"), data=form_data)

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get(COOK_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)
        self.assertRedirects(resp, "/accounts/login/?next=/cooks/")

    def test_private_permission(self):
        resp = self.client.get(COOK_LIST_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "kitchen_service/cook_list.html")

    def test_retrieve_cooks_pagination_4(self):
        resp = self.client.get(COOK_LIST_URL)

        self.assertTrue(resp.context["is_paginated"] is True)
        self.assertEqual(len(resp.context["cook_list"]), 4)

    def test_second_page_paginated(self):
        resp = self.client.get(COOK_LIST_URL + "?page=2")

        self.assertEqual(len(resp.context["cook_list"]), 4)

    def test_detail_page(self):
        cook_2 = get_user_model().objects.get(id=2)
        resp = self.client.get(reverse("kitchen_service:cook-detail", kwargs={"pk": cook_2.id}))
        self.assertContains(resp, cook_2.first_name)
        self.assertContains(resp, cook_2.last_name)
        self.assertContains(resp, cook_2.specialization)

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen_service.models import DishType

DISH_TYPE_LIST_URL = reverse("kitchen_service:dish-type-list")


class DishTypeTest(TestCase):

    def setUp(self):
        num_type = 8
        for type_id in range(num_type):
            DishType.objects.create(name=f"Test_{type_id}")

        self.user = get_user_model().objects.create_user(
            username="test_cook",
            password="cook1234"
        )

        self.client.force_login(self.user)

    def test_public_login_required(self):
        self.client.logout()
        resp = self.client.get(DISH_TYPE_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)
        self.assertRedirects(resp, "/accounts/login/?next=/dish-types/")

    def test_retrieve_dish_types_list_pagination_5(self):
        resp = self.client.get(DISH_TYPE_LIST_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "kitchen_service/dish_type_list.html")
        self.assertTrue(resp.context["is_paginated"] is True)
        self.assertTrue(len((resp.context["dish_type_list"])) == 5)

    def test_pagination_second_page(self):
        resp = self.client.get(DISH_TYPE_LIST_URL + "?page=2")

        self.assertEqual(len(resp.context["dish_type_list"]), 3)

    def test_delete_link(self):
        d_type = DishType.objects.get(id=1)
        resp = self.client.get(reverse("kitchen_service:dish-type-delete", kwargs={"pk": d_type.id}))

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "kitchen_service/dish_type_confirm_delete.html")



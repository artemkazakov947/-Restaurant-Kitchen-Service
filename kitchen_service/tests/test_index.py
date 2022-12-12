from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen_service.models import DishType, Dish

INDEX_URL = reverse("kitchen_service:index")


class TestIndexView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cook_driver",
            password="cook1234"
        )
        self.client.force_login(self.user)

    def test_public_permission(self):
        self.client.logout()
        resp = self.client.get(INDEX_URL)

        self.assertNotEqual(resp.status_code, 200)
        self.assertRedirects(resp, "/accounts/login/?next=/")

    def test_private_permission_used_template(self):
        resp = self.client.get(INDEX_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "kitchen_service/index.html")

    def test_driver_cars_manufacturer_count_listed(self):
        dish_type = DishType.objects.create(name="Test_type")
        cook = get_user_model().objects.get(id=1)
        dish = Dish.objects.create(
                name="Test_name",
                description="Test description",
                price=1.00,
                dish_type=dish_type
            )
        dish.cooks.add(cook)
        resp = self.client.get(INDEX_URL)

        self.assertEqual(resp.context["num_cooks"], len(get_user_model().objects.all()))
        self.assertEqual(resp.context["num_dishes"], len(Dish.objects.all()))
        self.assertEqual(resp.context["num_dish_types"], len(DishType.objects.all()))

    def test_num_visit_count(self):
        num_visit = 10
        for visit in range(num_visit):
            resp = self.client.get(INDEX_URL)

        self.assertEqual(resp.context["num_visits"], num_visit)

from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen_service.models import DishType, Dish


class TestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username="test_cook",
                                             password="test12345",
                                             first_name="Bob",
                                             last_name="Smith",
                                             specialization="assistant"
                                             )
        DishType.objects.create(name="Test")

    def test_dish_type_str(self):
        dish_type = DishType.objects.get(id=1)

        self.assertEqual(str(dish_type), "Test")

    def test_dish_str(self):
        dish_type = DishType.objects.get(id=1)
        dish = Dish.objects.create(name="test_name", dish_type=dish_type, price=10.00)

        self.assertEqual(str(dish), f"{dish.name}, (price:{dish.price} dish type: {dish.dish_type})")

    def test_user_str(self):
        cook = get_user_model().objects.get(id=1)

        self.assertEqual(str(cook), f"Cook {cook.first_name} {cook.last_name} with {cook.specialization} specialization.")

    def test_create_user_with_specialization(self):
        username = "test_cook2"
        specialization = "prep cook"
        password = "user123456"
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            specialization=specialization
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.specialization, specialization)

    def test_get_absolute_url(self):
        cook = get_user_model().objects.get(id=1)

        self.assertEqual(cook.get_absolute_url(), "/cooks/1/")


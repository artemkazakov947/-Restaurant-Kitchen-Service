from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from kitchen_service.models import DishType, Dish, Ingredient, Recipe
from kitchen_service.views import DishListView


class DishTest(TestCase):
    def setUp(self):
        self.cook = get_user_model().objects.create_user(
            username="cook_test",
            password="cook1234"
        )
        self.client.force_login(self.cook)

        dish_type = DishType.objects.create(name="test_type")
        ingredient = Ingredient.objects.create(name="test_ingredient")
        num_dishes = 8
        for num in range(num_dishes):
            Dish.objects.create(
                name=f"name{num}",
                description=f"Description{num}",
                price=num,
                dish_type=dish_type
            )
        dish = Dish.objects.get(id=1)
        recipe = Recipe.objects.create(description="description", dish=dish)
        recipe.ingredients.add(ingredient)

    def test_assigment_cook_on_dish(self):
        """Test checks is the buttons 'I would cook this dish' and 'I wouldn`t cook this dish' works properly"""
        dish = Dish.objects.get(id=1)

        resp = self.client.get(reverse("kitchen_service:toggle_me_to_dish", kwargs={"pk": dish.id}))

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f"/dishes/{dish.id}/")
        self.assertEqual(len(dish.cooks.all()), 1)

        resp = self.client.get(reverse("kitchen_service:toggle_me_to_dish", kwargs={"pk": dish.id}))

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f"/dishes/{dish.id}/")
        self.assertEqual(len(dish.cooks.all()), 0)

    def test_search_queryset_dish(self):
        request = RequestFactory().get("?name=name_1")
        view = DishListView()
        view.request = request
        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, Dish.objects.filter(name__icontains="name_1"))
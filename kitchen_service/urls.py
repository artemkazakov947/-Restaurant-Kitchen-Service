from django.urls import path

from kitchen_service.views import (index,
                                   DishTypeListView,
                                   DishTypeUpdateView,
                                   DishTypeCreateView,
                                   DishTypeDeleteView,
                                   DishListView,
                                   DishDetailView,
                                   DishCreateView,
                                   DishUpdateView,
                                   DishDeleteView,
                                   CookListView,
                                   CookCreateView,
                                   CookDetailView,
                                   CookDeleteView,
                                   RecipeDetailView,
                                   RecipeCreateView,
                                   RecipeUpdateView,
                                   RecipeDeleteView, toggle_me_to_dish, )

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-types/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-types/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("dishes/<int:pk>/toggle_me_to_dish/", toggle_me_to_dish, name="toggle_me_to_dish"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/<int:pk>/delete/", CookDeleteView.as_view(), name="cook-delete"),
    path("recipe/<int:pk>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipe/create/", RecipeCreateView.as_view(), name="recipe-create"),
    path("recipe/<int:pk>/update/", RecipeUpdateView.as_view(), name="recipe-update"),
    path("recipe/<int:pk>/delete/", RecipeDeleteView.as_view(), name="recipe-delete"),
                ]


app_name = "kitchen_service"

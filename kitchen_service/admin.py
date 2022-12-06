from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from kitchen_service.models import (
    DishType,
    Recipe,
    Dish,
    Cook,
    Ingredient,
)

admin.site.register(DishType)
admin.site.register(Recipe)
admin.site.register(Ingredient)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("dish_type",)
    list_display = ["name", "price", "description"]


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("specialization",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("specialization",)}),)
    )

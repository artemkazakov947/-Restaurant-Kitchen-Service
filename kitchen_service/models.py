from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class DishType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    SPEC_CHOICES = [
        ("chef", "chef"),
        ("grill", "grill"),
        ("assistant", "assistant"),
        ("pizzmaker", "pizzmaker"),
        ("sushi maker", "sushi maker"),
        ("prep cook", "prep cook")
    ]
    specialization = models.CharField(
        max_length=63, choices=SPEC_CHOICES, default="assistant"
    )

    def __str__(self):
        return f"Cook {self.first_name} {self.last_name} with {self.specialization} specialization."

    def get_absolute_url(self):
        return reverse_lazy("kitchen_service:cook-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="dishes"
    )
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dishes")

    class Meta:
        verbose_name_plural = "dishes"
        ordering = ("dish_type",)

    def __str__(self):
        return f"{self.name}, (price:{self.price} dish type: {self.dish_type})"


class Recipe(models.Model):
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name="recipe")
    dish = models.OneToOneField(
        Dish, on_delete=models.CASCADE, blank=True, null=True, related_name="recipe"
    )

    def __str__(self):
        return f"Recipe for {self.dish.name}"


class Task(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    cook = models.ForeignKey(Cook, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        ordering = ["is_done", "-created"]

    def __str__(self):
        return f"{self.content} for {self.cook} is done: {self.is_done}"

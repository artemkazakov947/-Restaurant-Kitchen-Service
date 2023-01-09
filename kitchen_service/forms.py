from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from kitchen_service.models import (Dish,
                                    Ingredient,
                                    Cook,
                                    Task,
                                    Recipe,
                                    )


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "specialization", "first_name", "last_name"
        )


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Dish
        fields = "__all__"


class RecipeForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Recipe
        fields = "__all__"
        widgets = {'dish': forms.HiddenInput()}


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search by name..."})
    )


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.SelectDateWidget)

    class Meta:
        model = Task
        fields = "__all__"

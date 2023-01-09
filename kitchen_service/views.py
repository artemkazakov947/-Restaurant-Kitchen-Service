from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from kitchen_service.forms import DishForm, RecipeForm, CookCreationForm, DishSearchForm, TaskForm
from kitchen_service.models import (
    Cook,
    Dish,
    DishType,
    Recipe,
    Task,
)


@login_required
def index(request):
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_type = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_type,
        "num_visits": num_visits + 1,
    }

    return render(request, "kitchen_service/index.html", context=context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen_service/dish_type_list.html"
    context_object_name = "dish_type_list"
    queryset = DishType.objects.all()
    paginate_by = 5


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen_service/dish_type_form.html"
    success_url = reverse_lazy("kitchen_service:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen_service/dish_type_form.html"
    success_url = reverse_lazy("kitchen_service:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen_service/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen_service:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    queryset = Dish.objects.all().select_related("dish_type")
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = DishSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(Q(name__icontains=form.cleaned_data["name"]) | Q(description__icontains=form.cleaned_data["name"]))
        return self.queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm

    def get_success_url(self):
        return reverse_lazy("kitchen_service:dish-list") + f"{self.object.id}/"


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("kitchen_service:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen_service:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")
    paginate_by = 4


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen_service:cook-list")


def toggle_me_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)
    if Dish.objects.get(pk=pk) in cook.dishes.all():
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("kitchen_service:dish-detail", args=[pk]))


class RecipeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Recipe
    queryset = Recipe.objects.all().prefetch_related("ingredients")


class RecipeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Recipe
    form_class = RecipeForm

    def get_success_url(self):
        return reverse_lazy("kitchen_service:dish-detail", args=[self.request.GET.get("dish")])

    def get_initial(self):
        initial = super(RecipeCreateView, self).get_initial()
        initial["dish"] = self.request.GET.get("dish")
        return initial


class RecipeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm
    success_url = reverse_lazy("kitchen_service:dish-list")


class RecipeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Recipe
    success_url = reverse_lazy("kitchen_service:dish-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.all()
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_staff is True:
            return self.queryset
        return self.queryset.filter(cook=self.request.user)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("kitchen_service:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("kitchen_service:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("kitchen_service:task-list")


def mark_complete_or_undo(request, pk):
    task = Task.objects.get(id=pk)
    if task.is_done is False:
        task.is_done = True
    else:
        task.is_done = False
    task.save()
    return HttpResponseRedirect(reverse_lazy("kitchen_service:task-list"))

from django.db.models import Q
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, View
from manager.models import Ingredient, Unit, Recipe
from .forms import IngredientForm


class IngredientList(ListView):
    model = Ingredient
    queryset = Ingredient.objects.all()
    paginate_by = 10
    template_name = 'ingredient/show_ingredients.html'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            context['ingredients'] = self.get_queryset().filter(
                Q(article_number=query) | Q(name__contains=query)
            )
        else:
            context['ingredients'] = self.get_queryset()
        return context


class IngredientAdd(CreateView):
    model = Ingredient
    template_name = 'ingredient/form_ingredients.html'
    form_class = IngredientForm

    def get_success_url(self):
        return reverse('ingredient-show-all')


class IngredientEdit(UpdateView):
    model = Ingredient
    template_name = 'ingredient/form_ingredients.html'
    form_class = IngredientForm

    def get_object(self, **kwargs):
        return Ingredient.objects.get(id=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('ingredient-show-all')


class RecipeList(ListView):
    model = Recipe
    template_name = 'recipe/show_recipes.html'
    queryset = Recipe.objects.all()
    paginate_by = 10

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = self.get_queryset()
        return context


class RecipeAdd(CreateView):
    model = Ingredient
    template_name = 'ingredient/form_ingredients.html'
    form_class = IngredientForm

    def get_success_url(self):
        return reverse('ingredient-show-all')


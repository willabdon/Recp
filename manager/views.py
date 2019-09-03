from django.db import transaction
from django.db.models import Q, Sum
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from manager.models import Ingredient, Recipe, IngredientAmount
from .forms import IngredientForm, RecipeForm, RecipeFormSet


class IngredientList(ListView):
    model = Ingredient
    queryset = Ingredient.objects.all()
    paginate_by = 10
    template_name = 'ingredient/show_ingredients.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'mine' in self.request.path:
            self.queryset = self.get_queryset().filter(created_by=self.request.user)
            self.template_name = 'ingredient/show_my_ingredients.html'
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
        if self.request.POST.get('_save'):
            return reverse('ingredient-show-mine')
        if self.request.POST.get('_another'):
            return reverse('ingredient-add')

    def form_valid(self, form):
        response = super(IngredientAdd, self).form_valid(form)
        self.object.created_by = self.request.user
        self.object.save()
        return response


class IngredientEdit(UpdateView):
    model = Ingredient
    template_name = 'ingredient/form_ingredients.html'
    form_class = IngredientForm

    def get_object(self, **kwargs):
        return Ingredient.objects.get(id=self.kwargs.get('id'))

    def get_success_url(self):
        if self.request.POST.get('_save'):
            return reverse('ingredient-show-mine')
        if self.request.POST.get('_another'):
            return reverse('ingredient-add')


class RecipeList(ListView):
    model = Recipe
    template_name = 'recipe/show_recipes.html'
    queryset = Recipe.objects.all()
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            context['recipes'] = self.get_queryset().filter(name__icontains=query)
        else:
            context['recipes'] = self.get_queryset().filter(ingredients__isnull=False).distinct()
        return context


class RecipeAdd(CreateView):
    model = Recipe
    template_name = 'recipe/form_recipe.html'
    form_class = RecipeForm

    def get_success_url(self):
        return reverse('recipe-show-all')

    def get_context_data(self, **kwargs):
        context = super(RecipeAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = RecipeFormSet(self.request.POST)
        else:
            context['formset'] = RecipeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredients = context['formset']
        with transaction.atomic():
            self.object = form.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
            else:
                context['form'] = form
                context['formset'] = ingredients
                return render(request=self.request, template_name=self.template_name, context=context)
        response = super(RecipeAdd, self).form_valid(form)
        self.object.created_by = self.request.user
        self.object.save()
        return response


class RecipeEdit(RecipeAdd, UpdateView):

    def get_object(self, **kwargs):
        return Recipe.objects.get(id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super(RecipeEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = RecipeFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = RecipeFormSet(instance=self.object)
        return context


class RecipeShow(DetailView):
    model = Recipe
    template_name = 'recipe/show_recipe.html'

    def get_object(self, **kwargs):
        return Recipe.objects.get(id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super(RecipeShow, self).get_context_data(**kwargs)
        context['ingredients'] = IngredientAmount.objects.filter(recipe=self.object)
        context['total'] = context['ingredients'].aggregate(Sum('total'))['total__sum']
        return context


def get_available_units(request, ingredient):
    if request.method == "GET" and request.is_ajax():
        ingredient = Ingredient.objects.get(id=ingredient)
        available_units = {x.id: x.get_id_display() for x in ingredient.unit.available_units()}
        return JsonResponse(available_units)
    else:
        return HttpResponseBadRequest()

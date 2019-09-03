from django.contrib import admin
from django.urls import path
from .views import IngredientList, IngredientAdd, IngredientEdit, RecipeList, RecipeAdd, RecipeEdit, RecipeShow
from .views import get_available_units

urlpatterns = [
    path('ingredient/all', IngredientList.as_view(), name='ingredient-show-all'),
    path('ingredient/mine', IngredientList.as_view(), name='ingredient-show-mine'),
    path('ingredient/add', IngredientAdd.as_view(), name='ingredient-add'),
    path('ingredient/edit/<int:id>/', IngredientEdit.as_view(), name='ingredient-edit'),
    path('ingredient/<int:ingredient>/unit/available', get_available_units, name='unit-available'),
    path('recipe/all', RecipeList.as_view(), name='recipe-show-all'),
    path('recipe/add', RecipeAdd.as_view(), name='recipe-add'),
    path('recipe/edit/<int:id>/', RecipeEdit.as_view(), name='recipe-edit'),
    path('recipe/show/<int:id>/', RecipeShow.as_view(), name='recipe-show'),
]

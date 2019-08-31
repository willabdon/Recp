from django.contrib import admin
from django.urls import path
from .views import IngredientList, IngredientAdd, IngredientEdit, RecipeList

urlpatterns = [
    path('ingredient/all', IngredientList.as_view(), name='ingredient-show-all'),
    path('ingredient/add', IngredientAdd.as_view(), name='ingredient-add'),
    path('ingredient/edit/<int:id>/', IngredientEdit.as_view(), name='ingredient-edit'),
    path('recipe/all', RecipeList.as_view(), name='recipe-show-all'),
]
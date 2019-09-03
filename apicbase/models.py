from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    recipe_favorited = models.ManyToManyField('manager.Recipe')

    def my_recipes_quantity(self):
        return self.created_recipes.count()

    def my_ingredients_quantity(self):
        return self.created_ingredients.count()

    def my_favorites_quantity(self):
        return self.recipe_favorited.count()

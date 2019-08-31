from django.contrib.auth.models import User
from django.db import models


class Unit(models.Model):
    KILOGRAM = 1
    GRAM = 2
    LITER = 3
    CENTILITER = 4
    UNIT_CHOICES = (
        (KILOGRAM, 'kg'),
        (GRAM, 'g'),
        (LITER, 'l'),
        (CENTILITER, 'cl'),
    )

    id = models.PositiveSmallIntegerField(choices=UNIT_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    article_number = models.CharField(max_length=200, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="created_ingredients", blank=True, null=True,
                                   on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_cost(self):
        return '{:.2f}{} per {:.2f}€'.format(self.amount, self.unit, self.value)


class Recipe(models.Model):
    name = models.CharField(max_length=300)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientAmount')


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

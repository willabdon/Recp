from django.contrib.auth.models import User
from django.db import models

from apicbase.models import CustomUser
from manager.utils import calc_total_ingredient


class Unit(models.Model):

    KILOGRAM = 1
    GRAM = 2
    LITER = 3
    CENTILITER = 4

    SOLID_CHOICES = (KILOGRAM, GRAM)
    LIQUID_CHOICES = (LITER, CENTILITER)

    UNIT_CHOICES = (
        (KILOGRAM, 'kg'),
        (GRAM, 'g'),
        (LITER, 'l'),
        (CENTILITER, 'cl'),
    )

    id = models.PositiveSmallIntegerField(choices=UNIT_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()

    @staticmethod
    def kg_to_g(value):
        return value * 1000

    @staticmethod
    def g_to_kg(value):
        return value / 1000

    @staticmethod
    def l_to_cl(value):
        return value * 100

    @staticmethod
    def cl_to_l(value):
        return value / 100

    def available_units(self):
        if self.id in self.SOLID_CHOICES:
            return Unit.objects.filter(id__in=self.SOLID_CHOICES)
        elif self.id in self.LIQUID_CHOICES:
            return Unit.objects.filter(id__in=self.LIQUID_CHOICES)
        else:
            return []


class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    article_number = models.IntegerField(unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, related_name="created_ingredients", blank=True, null=True,
                                   on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ('article_number', )

    def __str__(self):
        return self.name

    def get_cost(self):
        return '{:.2f}€ each {:.2f}{}'.format(self.value, self.amount, self.unit)


class Recipe(models.Model):
    name = models.CharField(max_length=300)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientAmount')
    created_by = models.ForeignKey(CustomUser, related_name="created_recipes", blank=True, null=True,
                                   on_delete=models.SET_NULL)
    instructions = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ('name', )


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.total = calc_total_ingredient(self)
        super(IngredientAmount, self).save(*args, **kwargs)

    def get_formated_amount(self):
        return '{}{}'.format(self.amount, self.unit)

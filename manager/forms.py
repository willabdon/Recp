from django import forms
from django.forms import widgets

from manager.models import Ingredient, Unit


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ('name', 'article_number', 'value', 'amount', 'unit')
        attrs = {
            'class': 'form-control'
        }
        widgets = {
            'name': forms.TextInput(attrs=attrs),
            'article_number': forms.TextInput(attrs=attrs),
            'value': forms.NumberInput(attrs=attrs),
            'amount': forms.NumberInput(attrs=attrs),
            'unit': widgets.Select(attrs=attrs, choices=Unit.objects.all())
        }


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ('name', 'article_number', 'value', 'amount', 'unit')
        attrs = {
            'class': 'form-control'
        }
        widgets = {
            'name': forms.TextInput(attrs=attrs),
            'article_number': forms.TextInput(attrs=attrs),
            'value': forms.NumberInput(attrs=attrs),
            'amount': forms.NumberInput(attrs=attrs),
            'unit': widgets.Select(attrs=attrs, choices=Unit.objects.all())
        }



from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets, inlineformset_factory
from manager.models import Ingredient, Unit, Recipe, IngredientAmount
from django.utils.translation import ugettext_lazy as _

from manager.utils import get_choices


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'article_number', 'value', 'amount', 'unit')
        attrs = {
            'class': 'form-control'
        }
        widgets = {
            'name': forms.TextInput(attrs=attrs),
            'article_number': forms.NumberInput(attrs=attrs),
            'value': forms.NumberInput(attrs=attrs),
            'amount': forms.NumberInput(attrs=attrs),
            'unit': widgets.Select(attrs=attrs, choices=Unit.objects.all())
        }


class IngredientAmountForm(forms.ModelForm):
    attrs = {
        'class': 'form-control',
        'required': True
    }

    error_attrs = {
        'class': 'form-control error-input',
        'required': True,
    }

    class Meta:
        model = IngredientAmount
        fields = ('ingredient', 'amount', 'unit',)

    def __init__(self, *args, **kwargs):
        super(IngredientAmountForm, self).__init__(*args, **kwargs)
        ingredient_choices = Ingredient.objects.all()

        self.fields['ingredient'].widget = widgets.Select(attrs={
            'class': 'form-control ingredient_input',
            'required': True
        }, choices=get_choices(ingredient_choices))
        self.fields['amount'].widget = forms.NumberInput(attrs=self.attrs)
        self.fields['unit'].widget = widgets.Select(attrs=self.attrs, choices=get_choices(Unit.objects.all()))

    def clean(self):
        cleaned_data = self.cleaned_data
        self.handle_errors()
        if 'unit' in cleaned_data:
            if cleaned_data['unit'] not in cleaned_data['ingredient'].unit.available_units():
                raise ValidationError({'unit': "This unit it's not valid for this type of ingredient"})

        super(IngredientAmountForm, self).clean()

    def handle_errors(self):
        for f in self.errors:
            self.fields[f].widget.attrs.update({'class': self.fields[f].widget.attrs.get('class', '') + ' error-input'})


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name',)
        attrs = {
            'class': 'form-control'
        }
        widgets = {
            'name': forms.TextInput(attrs=attrs),
        }


RecipeFormSet = inlineformset_factory(Recipe, IngredientAmount, extra=0, can_delete=True, min_num=1,
                                      fields=('ingredient', 'amount', 'unit',), form=IngredientAmountForm)

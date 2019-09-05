from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets, inlineformset_factory
from manager.models import Ingredient, Unit, Recipe, IngredientAmount
from manager.utils import get_choices

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .layout import *


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
        }

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        self.fields['unit'].widget = widgets.Select(attrs={'class': 'form-control'},
                                                    choices=get_choices(Unit.objects.all()))


class IngredientAmountForm(forms.ModelForm):
    class Meta:
        model = IngredientAmount
        fields = ('ingredient', 'amount', 'unit',)
        attrs = {
            'class': 'form-control',
            'required': True
        }
        widgets = {
            'ingredient': autocomplete.ModelSelect2(
                url='ingredient-autocomplete',
                attrs={
                    'class': 'form-control ingredient_input',
                    'required': True
                }
            ),
            'amount': forms.NumberInput(attrs=attrs),
        }

    def __init__(self, *args, **kwargs):
        super(IngredientAmountForm, self).__init__(*args, **kwargs)
        self.fields['unit'].widget = widgets.Select(attrs={'class': 'form-control'},
                                                    choices=get_choices(Unit.objects.all()))
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div(Field('id')),
                Div(Field('ingredient'), css_class='form-group col-md-5'),
                Div(Field('amount'), css_class='form-group col-md-5'),
                Div(Field('unit'), css_class='form-group col-md-2'),
                css_class='form-row'
            ),
        )

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
        fields = ('id', 'name', 'image', 'instructions')
        attrs = {
            'class': 'form-control'
        }
        widgets = {
            'name': forms.TextInput(attrs=attrs),
            'instructions': forms.Textarea(attrs=attrs)
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_show_labels = False
        self.helper.label_class = 'd-block text-center'
        self.helper.layout = Layout(
            Div(
                HTML('<label class="d-block" for="id_image">Image:</label>'),
                Field('image'),
                HTML('<label class="d-block text-center" for="id_name">Tell us your recipe name:</label>'),
                Field('name', ),
                HTML('<label class="d-block text-center my-2" for="id_instructions">Instructions:</label>'),
                Field('instructions'), css_class='form-group'
            ),
            HTML('<h4 class="gray-color">Ingredients</h4><hr>'),
            Fieldset('', Formset('formset')),
            HTML('<button type="submit" class="btn btn-green mr-2">Submit</button>'),
            HTML('<a href="{% url "recipe-show-mine" %}" class="btn btn-green">Cancel</a>')
        )


RecipeFormSet = inlineformset_factory(Recipe, IngredientAmount, extra=0, can_delete=False, min_num=1,
                                      fields=('ingredient', 'amount', 'unit',), form=IngredientAmountForm)

from django import forms
from django.contrib.auth import authenticate, login

from apicbase.models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(max_length=128)
    attrs = {
        'class': 'form-control',
        'required': True
    }
    password_confirm.widget = forms.PasswordInput(attrs=attrs)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password_confirm')
        attrs = {
            'class': 'form-control',
            'required': True
        }
        widgets = {
            'first_name': forms.TextInput(attrs=attrs),
            'last_name': forms.TextInput(attrs=attrs),
            'username': forms.TextInput(attrs=attrs),
            'email': forms.EmailInput(attrs=attrs),
            'password': forms.PasswordInput(attrs=attrs),

        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if cleaned_data['password'] != cleaned_data['password_confirm']:
            raise ValidationError({'password': "Passwords don't match."})
        else:
            cleaned_data['password'] = make_password(cleaned_data['password'])
        return cleaned_data

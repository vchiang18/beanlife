from django import forms
from .models import User

class LoginForm(forms.Form):
    username=forms.CharField(max_length=150)
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )

class SignupForm(forms.Form):
    username=forms.CharField(max_length=150)
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )
    password_confirmation=forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )

class TargetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'servings_fiber',
            'servings_fat',
            'separate_fats',
            'timezone'
        ]

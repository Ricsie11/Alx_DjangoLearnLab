from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Enter your email", max_length=254,
    widget= forms.TextInput(attrs={'placeholder': 'Email'}))

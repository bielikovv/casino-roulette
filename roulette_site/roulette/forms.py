from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']



class RedactInfoUserForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



class RedactInfoProfileForm(forms.ModelForm):
    photo = forms.ImageField(label='Photo', widget=forms.FileInput(attrs={'class': 'form-control form-control-sm'}))
    nickname = forms.CharField(label='Singer nickname', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = Profile
        fields = ['photo', 'nickname']
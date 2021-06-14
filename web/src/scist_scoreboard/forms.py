from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, widgets
from user.models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(
        label = "使用者名稱",
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label = "電子郵件",
        widget = forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label = "密碼",
        widget = forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label = "密碼確認",
        widget = forms.PasswordInput(attrs={'class': 'form-control'})
    )

class LoginForm(forms.Form):
    class Meta:
        fields = ['email', 'password']
    
    email = forms.EmailField(
        label = "電子郵件",
        widget = forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label = "密碼",
        widget = forms.PasswordInput(attrs={'class': 'form-control'})
    )
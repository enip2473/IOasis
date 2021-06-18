from django import forms
from django.forms import fields, widgets
from user.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, widgets

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(
        max_length = 25,
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

class UpdateEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'CF_handle']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateEditForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        label = "新使用者名稱",
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label = "新電子郵件",
        widget = forms.EmailInput(attrs={'class': 'form-control'})
    )
    CF_handle = forms.CharField(
        label = "新 CodeForces Handle",
        widget = forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise forms.ValidationError('Username {} is already in use.'.format(username))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError('Email {} is already in use.'.format(email))
    
    def clean_CF_handle(self):
        CF_handle = self.cleaned_data['CF_handle']
        try:
            user = CustomUser.objects.exclude(pk=self.instance.pk).get(CF_handle=CF_handle)
        except CustomUser.DoesNotExist:
            return CF_handle
        raise forms.ValidationError('CF_handle {} is already in use.'.format(CF_handle))
    
    def save(self, commit=True):
        user = super(UpdateEditForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.CF_handle = self.cleaned_data['CF_handle']
        if commit:
            user.save()
        return user
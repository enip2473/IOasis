from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from user.forms import LoginForm, RegisterForm, UpdateEditForm
from user.models import CustomUser

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
    
        user = auth.authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', locals())

@login_required
def UserEditPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")

    user_id = kwargs.get("user_id")
    user = CustomUser.objects.get(pk=user_id)
    if user.pk != request.user.pk:
        return HttpResponse("You Cannot Edit Someone Elese Procfile!")

    if request.method == 'POST':
        form = UpdateEditForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect("user:edit", user_id=user_id)
        else:
            form = UpdateEditForm(request.POST, instance=request.user,
                initial = {
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email,
                    "CF_handle": user.CF_handle,
                }
            )
    else:
        form = UpdateEditForm(
            initial={
                "id": user.pk,
                "username": user.username,
                "email": user.email,
                "CF_handle": user.CF_handle,
            }
        )

    return render(request, 'UserEdit.html', locals())
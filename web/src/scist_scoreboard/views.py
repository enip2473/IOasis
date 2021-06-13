from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from scist_scoreboard.forms import RegisterForm

def index(request):
    return render(request, 'index.html', locals())

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render(request, 'loging.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = RegisterForm()
        #form  = UserCreationForm()
    return render(request, 'register.html', locals())
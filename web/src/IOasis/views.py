from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', locals())

def handler404(request, *args, **argv):
    return render(request, '404.html', status=404)

# def handler403(request, **args, **argv):
    # return render(request, '403.html', status=403)
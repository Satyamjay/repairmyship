from django.shortcuts import render
from .forms import *
from django.http import HttpResponse
from django.contrib.auth import authenticate
from authentication.models import *
import datetime
from django.contrib import auth
from django.shortcuts import redirect
# Create your views here.


def signup(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        User.objects.create_user(email=request.POST['email'], password=request.POST['password'], age=request.POST['age'], country=request.POST['country'])
        login(request)
    return render(request, 'signup.html', context={'form': form, 'login_or_logout': 'Login'})


def login(request):
    if request.user.is_authenticated:
        return HttpResponse(request.session['username'])
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            user.last_login = datetime.datetime.now()
            request.session['username'] = user.email
            return render(request, 'home.html')
        if user is None:
            return render(request, 'signup.html', {'form': form, 'login_or_logout': 'Login'})
    else:
        return render(request, 'signup.html', {'form': form, 'login_or_logout': 'Login'})
    return render(request, 'signup.html', context={'form': form, 'login_or_logout': 'Login'})


def logout(request):
    auth.logout(request)
    form = LoginForm(None)
    return render(request, 'signup.html', context={'form': form, 'login_or_logout': 'Login'})


def home(request):
    return redirect('/login/')
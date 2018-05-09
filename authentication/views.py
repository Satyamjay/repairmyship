from django.shortcuts import render
from .forms import *
from django.http import HttpResponse
from django.contrib.auth import authenticate
from authentication.models import *
# Create your views here.


def signup(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        age = request.POST['age']
        country = request.POST['country']
        um = UserManager()
        um.create_user(email, password, age, country)
    return render(request, 'signup.html', context={'form': form})


def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = User.objects.get(email=request.POST['email'])
        form_password = request.POST['password']
        hashed_password = bcrypt.hashpw(form_password.encode('utf8'), user.salt.encode('utf8'))
        user = authenticate(username='oj@oj.com', password=hashed_password.decode('ascii'))
        if user is not None:
            return HttpResponse("Hemml")
        if user is None:
            return HttpResponse("Hemmlasdfd")
    return render(request, 'signup.html', context={'form': form})
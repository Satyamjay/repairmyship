from django.shortcuts import render
from .forms import *
from django.http import Http404
from django.contrib.auth import authenticate
from authentication.models import *
import datetime
from django.contrib import auth
from django.shortcuts import redirect
import math
# Create your views here.


def signup(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        User.objects.create_user(email=request.POST['email'], password=request.POST['password'], age=request.POST['age'], country=request.POST['country'])
        login(request)
    return render(request, 'signup.html', context={'form': form, 'login_or_logout': 'Login'})


def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            user.last_login = datetime.datetime.now()
            request.session['username'] = user.username
            return redirect(home)
        if user is None:
            return render(request, 'signup.html', {'form': form, 'valid_login': 'Invalid UserName or Password', 'login_or_logout': 'Login'})
    else:
        return render(request, 'signup.html', {'form': form, 'login_or_logout': 'Login'})
    return render(request, 'signup.html', context={'form': form, 'login_or_logout': 'Login'})


def logout(request):
    auth.logout(request)
    form = LoginForm(None)
    return redirect(login)


def home(request, page_number=1):
    if 'username' in request.session.keys():
        try:
            page_number = int(page_number)
        except ValueError:
            raise Http404()
        max_questions_in_one_page = 2
        if page_number < 1:
            return redirect(home)
        questions = Question.objects.all()[(page_number-1):(page_number+max_questions_in_one_page-1)]
        max_pages = math.ceil((len(Question.objects.all()))/max_questions_in_one_page)
        return render(
            request, 'home.html',
            context={
                    'questions': questions,
                    'login_or_logout': 'Logout',
                    'current_page': range(page_number, page_number+4),
                    'max_pages': max_pages})
    else:
        return redirect(login)
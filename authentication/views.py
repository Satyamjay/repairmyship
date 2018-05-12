from django.shortcuts import render
from .forms import *
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from authentication.models import *
from django.contrib.auth.decorators import login_required
import datetime
from django.http import JsonResponse
from django.shortcuts import redirect
import math
# Create your views here.


def signup(request):
    logout(request)
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        User.objects.create_user(email=request.POST['email'], password=request.POST['password'], age=request.POST['age'], country=request.POST['country'])
        redirect(my_login)
    return render(request, 'signup.html', context={'form': form, 'login_or_logout': 'Login'})


def my_login(request):
    if not request.user.is_authenticated:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = authenticate(username=request.POST['email'], password=request.POST['password'])
            if user is not None:
                user.last_login = datetime.datetime.now()
                login(request, user=user)
                return redirect(home)
            if user is None:
                return render(request, 'signup.html', {'form': form, 'valid_login': 'Invalid UserName or Password', 'login_or_logout': 'Login'})
        else:
            return render(request, 'signup.html', {'form': form, 'login_or_logout': 'Login'})

    elif request.user.is_authenticated:
        return redirect(home)
    else:
        HttpResponse("wow")



def my_logout(request):
    logout(request)
#   return redirect(login, permanent=True)
    return redirect(my_login)

@login_required
def home(request, page_number=1):
    try:
        page_number = int(page_number)
    except ValueError:
        raise Http404()
    max_questions_in_one_page = 2
    questions = Question.objects.all()[(page_number-1):(page_number+max_questions_in_one_page-1)]
    max_pages = math.ceil((len(Question.objects.all()))/max_questions_in_one_page)
    if (page_number < 1) or (page_number > max_pages):
        raise Http404
    return render(
        request, 'home.html',
        context={
                'questions': questions,
                'login_or_logout': 'Logout',
                'current_page': range(page_number, page_number+4),
                'max_pages': max_pages})


@login_required
def answers(request, question_id, page_number=1):
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(its_question=question_id)
    max_answers_in_one_page = 2
    max_pages = math.ceil((len(Answer.objects.all()))/max_answers_in_one_page)
    if (page_number < 1) or (page_number > max_pages):
        raise Http404
    return render(request, 'answer.html',
                  context= {
                    'question':question,
                    'answers':answers,
                    'login_or_logout': 'Logout',
                    'current_page': range(page_number, page_number+4),
                    'max_pages': max_pages,
                    'user': request.session['username']}
                  )

@login_required
def like_question(request, question_id=None):
    user = request.user
    question = Question.objects.get(id = question_id)
    question.like_by.add(user)
    json = {'success':True}
    return JsonResponse(json)

from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate,login, logout
# from BuildMyShip.custom_authentication import MyCustomBackend
from authentication.models import User, Question, Answer
import datetime
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
        # Create an object of LoginForm with either the data from POST or empty
        form = LoginForm(request.POST or None)
        if form.is_valid():
            # Authenticate is a build in method to check the credentials
            user = authenticate(username=request.POST['email'], password=request.POST['password'])
            if user is not None:
                user.last_login = datetime.datetime.now()
                # login is a builtin method to manage sessions
                login(request, user=user)
                return redirect('/home/-when/all/1')
            if user is None:
                return render(request, 'signup.html', {'form': form, 'valid_login': 'Invalid UserName or Password', 'login_or_logout': 'Login'})
        else:
            return render(request, 'signup.html', {'form': form, 'login_or_logout': 'Login'})

    else:
        return HttpResponseRedirect('/home/-when/all/1')




def my_logout(request):
    logout(request)
#   return redirect(login, permanent=True)
    return redirect(my_login)


def home(request, page_number=1, sort_by= '-when', filter_by='all'):
    if request.user.is_authenticated:
        max_questions_in_one_page = 2
        first_question_on_the_page = (page_number*max_questions_in_one_page)-max_questions_in_one_page
        if(filter_by=='all'):
            # Dont apply filter if filter_by is all
            questions = Question.objects.order_by(sort_by)[first_question_on_the_page:first_question_on_the_page+max_questions_in_one_page]
        else:
            # Apply the filter
            questions = Question.objects.filter(type=filter_by).order_by(sort_by)[first_question_on_the_page:first_question_on_the_page+max_questions_in_one_page]
        liked_question = []
        # Get the questions those are liked by the user on the current page
        for question in questions:
            if question.like_by.filter(id = request.user.id):
                liked_question.append(question.id)

        reported_question = []
        # Get the questions those are reported by the user on the current page
        for question in questions:
            if question.reported_by.filter(id = request.user.id):
                reported_question.append(question.id)

        max_pages = math.ceil((len(Question.objects.all()))/max_questions_in_one_page) if filter_by=='all' else math.ceil((len(Question.objects.filter(type=filter_by)))/max_questions_in_one_page)

        if (page_number < 1) or (page_number > max_pages) and (max_pages!=0):
            raise Http404
        return render(
            request, 'home.html',
            context={
                'questions': questions,  # List of questions to be displayed on the current page
                'login_or_logout': 'Logout',
                'current_pages': range(page_number, page_number+4),
                'max_pages': max_pages,
                'liked_questions': liked_question,
                'reported_questions': reported_question,
                'sort_by': sort_by,
                'filter_by': filter_by})
    else:
        return redirect(my_login)

# Almost same as home view
def answers(request, question_id, sort_by= '-when', page_number=1):
    if request.user.is_authenticated:
        question = Question.objects.get(id=question_id)
        max_answers_in_one_page = 2
        first_answer_on_the_page = (page_number*max_answers_in_one_page)-max_answers_in_one_page
        max_pages = math.ceil((len(Answer.objects.all()))/max_answers_in_one_page)
        answers = Answer.objects.filter(its_question=question_id).order_by(sort_by)[first_answer_on_the_page:first_answer_on_the_page+max_answers_in_one_page]
        if (page_number < 1) or (page_number > max_pages) and (max_pages!=0):
            raise Http404

        liked_answer = []
        for answer in answers:
            if answer.like_by.filter(id = request.user.id):
                liked_answer.append(question.id)

        reported_answer = []
        for answer in answers:
            if answer.reported_by.filter(id = request.user.id):
                reported_answer.append(question.id)

        return render(
            request, 'answer.html',
            context={
                'question': question,
                'answers': answers,
                'login_or_logout': 'Logout',
                'current_pages': range(page_number, page_number+4),
                'max_pages': max_pages,
                'liked_answer': liked_answer,
                'reported_answer': reported_answer,
                'sort_by': sort_by,
                'user': request.user.username})

    else:
        return redirect(my_login)


# Like And Report APIs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class LikeQuestion(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = {permissions.IsAuthenticated}

    def get(self, request,question_id=None,format=None):
        user = self.request.user
        if user.is_authenticated:
            question = Question.objects.get(id = question_id)
            # If user has already liked and again clicks the like button this ill remove the like
            if user in question.like_by.all():
                question.like_by.remove(user)
                question.likes -= 1
                question.save()
            else:
                question.like_by.add(user)
                question.likes += 1
                question.save()
            data = {
                'success': True
            }
            return Response(data)


class ReportQuestion(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = {permissions.IsAuthenticated}

    def get(self, request, question_id=None,format=None):
        data = {
            'success': False
        }
        user = self.request.user
        if user.is_authenticated:
            question = Question.objects.get(id = question_id)
            if user in question.reported_by.all():
                question.reported_by.remove(user)
                question.reported_by -= 1
                question.save()
                data['success'] = True
            else:
                question.reported_by.add(user)
                question.reported_by += 1
                question.save()
                data['success'] = True

            return Response(data)


class LikeAnswer(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = {permissions.IsAuthenticated}

    def get(self, request, answer_id=None, format=None):
        user = self.request.user
        if user.is_authenticated:
            answer = Answer.objects.get(id = answer_id)
            if user in answer.like_by.all():
                answer.like_by.remove(user)
                answer.likes -= 1
                answer.save()
            else:
                answer.like_by.add(user)
                answer.likes += 1
                answer.save()
            data = {
                'success': True
            }

            return Response(data)


class ReportAnswer(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = {permissions.IsAuthenticated}

    def get(self, request, answer_id=None, format=None):
        user = self.request.user
        if user.is_authenticated:
            answer = Answer.objects.get(id = answer_id)
            if user in answer.reported_by.all():
                answer.reported_by.remove(user)
                answer.reports -= 1
                answer.save()
            else:
                answer.reported_by.add(user)
                answer.reports += 1
                answer.save()
            data = {
                'success': True
            }

            return Response(data)
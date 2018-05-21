"""BuildMyShip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.my_login),
    path('signup/', views.signup),
    path('login/', views.my_login),
    path('logout/', views.my_logout),
    # Question URL
    path('home/<sort_by>/<filter_by>/<int:page_number>/', views.home),
    # Ask a question
    path('ask_question/', views.ask_question),
    # Answer a question
    path('answer_question/<int:its_question>', views.answer_question),
    # Answer URL
    path('answer/<sort_by>/<int:question_id>/<int:page_number>/', views.answers),
    # API URLS
    path('api/like_question/<int:question_id>/', views.LikeQuestion.as_view()),
    path('api/report_question/<int:question_id>/', views.ReportQuestion.as_view()),
    path('api/like_answer/<int:answer_id>/', views.LikeAnswer.as_view()),
    path('api/report_answer/<int:answer_id>/', views.ReportAnswer.as_view()),


]

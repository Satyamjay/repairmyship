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
from django.urls import path, re_path
from authentication import views
from verified_email_field import views as vefview

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
<<<<<<< HEAD
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

=======
    # List My Questions
    path('my_questions/', views.my_questions),
    # Delete my question
    path('delete_question/<int:question_id>', views.delete_question)
>>>>>>> 85e90b201536cfa583b3978ebfce45aea8f871c5

]

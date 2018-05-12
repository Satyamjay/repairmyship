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
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('home/', views.home),
    url('^home/(?:page-(?P<page_number>\d+)/)?$', views.home),
    path('signup/', views.signup),
    path('login/', views.my_login),
    path('logout/', views.my_logout),
    path('answer/<int:question_id>/<int:page_number>/', views.answers),
    path('api/like_question/<int:question_id>/', views.LikeQuestion.as_view()),
    path('api/report_question/<int:question_id>/', views.ReportAnswer.as_view())

]

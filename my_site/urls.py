from django.contrib import admin
from django.urls import path
from . import views

  
urlpatterns = [
     path("",views.logins, name="l"),
     path("login/",views.logins, name="l"),
     path("register/",views.register, name="r"),
     path("home/",views.home, name="h"),
     path("logouts/",views.logouts, name="logouts"),
     path("feedback/",views.feedback, name="f"),
     path("submit/",views.submit, name="s"),
     path("tech/",views.tech, name="t"),
     path("business/",views.business, name="b"),
     path("enter/",views.enter, name="p"),
     path("science/",views.science, name="s"),

]
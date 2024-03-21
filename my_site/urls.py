from django.contrib import admin
from django.urls import path
from . import views

  
urlpatterns = [
     path("",views.logins, name="l"),
     path("login/",views.logins, name="l"),
     path("register/",views.register, name="r"),
     path("home/",views.home, name="h"),
     path("logouts/",views.logouts, name="logouts"),
]
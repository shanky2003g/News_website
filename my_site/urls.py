from django.contrib import admin
from django.urls import path
from . import views

  
urlpatterns = [
     path("",views.logins, name="l"),
     path("register/",views.register, name="r"),

]
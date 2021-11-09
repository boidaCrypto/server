from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('register/local', views.LocalRegister),
]

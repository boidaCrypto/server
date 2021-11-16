from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('kakao/login', views.kakao_login, name='kakao_login'),
]

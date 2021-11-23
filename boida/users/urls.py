from django.contrib import admin
from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenVerifyView
urlpatterns = [
    path('kakao/login', views.kakao_login, name='kakao_login'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', views.HelloView.as_view(), name="hello"),

]

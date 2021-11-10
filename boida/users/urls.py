from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('register/local', views.LocalRegister),
    path('kakao/login', views.kakao_login, name='kakao_login'),
    path('kakao/callback', views.kakao_callback, name='kakao_callback'),
    # path('kakao/login/finish', views.KakaoLogin.as_view(), name='kakao_login_todjango')
]

from django.contrib import admin
from django.urls import path, include
from exchange import models
from home import views

urlpatterns = [
    path('list', views.List),
    path('check-connected-exchange', views.CheckConnectedExchange),
    path('total-asset', views.TotalAsset)

    ]

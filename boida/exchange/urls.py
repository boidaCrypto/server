from django.contrib import admin
from django.urls import path, include
from exchange import models
from exchange import views

urlpatterns = [
    path('connected-exchange/<int:pk>', views.ConnectedExchangeList),
    path('connecting-exchange', views.ConnectingExchange),
    path('list-exchange/<int:pk>', views.ListExchange),
    ]

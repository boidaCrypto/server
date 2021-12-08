from django.contrib import admin
from django.urls import path, include
from exchange import models
from exchange import views

urlpatterns = [
    path('connected-exchange/<int:pk>', views.ConnectedExchangeList),
    path('connecting-exchange', views.ConnectingExchange),
    path('list-exchange/<int:pk>', views.ListExchange),
    path('delete-exchange', views.DeleteExchange),
    path('list-exchange-description/<int:pk>', views.ListExchangeDescription),
    path('check-exchange-synchronized', views.CheckExchangeSynchronized),
    path('firebase-test', views.FirebaseTest)
    ]

from django.contrib import admin
from django.urls import path, include
from exchange import models
from transaction import views

urlpatterns = [
    path('test', views.Test),
    path('total-transaction-list/<int:page>', views.ToalTransactionList),
]

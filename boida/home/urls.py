from django.contrib import admin
from django.urls import path, include
from exchange import models
from home import views

urlpatterns = [

    path('test', views.Test),
    path('list', views.List),
    path('list2', views.List2),
    path('check-connected-exchange', views.CheckConnectedExchange),
    path('total-asset', views.TotalAsset)

    ]

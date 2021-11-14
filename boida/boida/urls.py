from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('dj_rest_auth.urls')),
    path('users/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('exchange/', include('exchange.urls'))
    ]

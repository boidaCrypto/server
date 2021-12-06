from django.contrib import admin
from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('users/', include('dj_rest_auth.urls')),
    # path('users/', include('allauth.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', include('users.urls')),
    path('exchange/', include('exchange.urls')),
    path('transaction/', include('transaction.urls')),
    path('home/', include('home.urls')),
    ]

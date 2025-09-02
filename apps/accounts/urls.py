from django.urls import path

from apps.accounts.views import (
    RegisterAPIView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
)


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='account-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='account-login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='account-refresh'),
    path('verify/', CustomTokenVerifyView.as_view(), name='account-verify'),
]

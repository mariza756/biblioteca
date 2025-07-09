from django.urls import path
from .views import RegisterView

# Simple JWT views para login (ya vienen listas)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),      # login JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

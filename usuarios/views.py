from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

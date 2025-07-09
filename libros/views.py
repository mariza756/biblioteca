from rest_framework import viewsets
from .models import Autor, Genero, Libro, Calificacion
from .serializers import AutorSerializer, GeneroSerializer, LibroSerializer, CalificacionSerializer
from rest_framework.permissions import IsAuthenticated

class AutorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class GeneroViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class LibroViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

class CalificacionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer

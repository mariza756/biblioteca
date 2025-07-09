from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Autor, Genero, Libro, Calificacion

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class LibroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(read_only=True)
    genero = GeneroSerializer(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(
        queryset=Autor.objects.all(), source='autor', write_only=True)
    genero_id = serializers.PrimaryKeyRelatedField(
        queryset=Genero.objects.all(), source='genero', write_only=True)

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'autor_id', 'genero', 'genero_id', 'fecha_lanzamiento', 'isbn', 'libro_url']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CalificacionSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='usuario', write_only=True)
    libro = LibroSerializer(read_only=True)
    libro_id = serializers.PrimaryKeyRelatedField(
        queryset=Libro.objects.all(), source='libro', write_only=True)

    class Meta:
        model = Calificacion
        fields = ['id', 'libro', 'libro_id', 'usuario', 'usuario_id', 'calificacion']
        # unique_together ya se respeta por el modelo

from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    nombre = models.CharField(max_length=120)
    nacionalidad = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre
    
class Libro(models.Model):
    titulo = models.CharField(max_length=220)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='libros')
    fecha_lanzamiento = models.DateField()
    isbn = models.CharField(max_length=20, unique=True)
    libro_url = models.URLField()

    def __str__(self):
        return self.titulo

class Calificacion(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='calificaciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calificaciones')
    calificacion = models.DecimalField(max_digits=2, decimal_places=1)


    class Meta:
        unique_together = ('libro', 'usuario') 
    def __str__(self):
        return f"{self.usuario.username} - {self.libro.titulo} ({self.puntaje})"

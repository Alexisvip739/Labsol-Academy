from django.db import models
from usuario.models import UsuarioPersonalizado

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    miniatura = models.ImageField(upload_to='icon_etiqueta/')

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=150)
    miniatura = models.ImageField(upload_to='miniaturas/')
    etiquetas = models.ManyToManyField(Categoria)
    instructor = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, null=True)
    archivo_pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class SolicitudCurso(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

class Inscripcion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
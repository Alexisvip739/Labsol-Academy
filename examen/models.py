from django.db import models
from curso.models import Curso
from usuario.models import UsuarioPersonalizado

# Create your models here.
class Examen(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=255, null=True, blank=True)
    curso = models.OneToOneField(Curso, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
    	return self.nombre
    	

class Pregunta(models.Model):
    examen = models.ForeignKey(Examen, related_name='preguntas', on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='respuestas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=100)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

class CalificacionExamen(models.Model):
    calificacion = models.FloatField(max_length=100, null=False, blank=False )
    estudiante = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)

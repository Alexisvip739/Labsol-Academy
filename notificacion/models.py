from django.db import models
from usuario.models import UsuarioPersonalizado
from curso.models import Curso
from django.utils import timezone


class Notificacion(models.Model):
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=250)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    creador = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.asunto


class NotificacionCurso(Notificacion):
    curso = models.ForeignKey(Curso,on_delete=models.CASCADE,null=True)
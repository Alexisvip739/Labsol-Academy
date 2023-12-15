from django.db import models
from usuario.models import UsuarioPersonalizado
# Create your models here.

class Videollamada(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=200)
    enlace = models.CharField(max_length=200)
    fecha_reunion = models.DateField()
    hora = models.TimeField(null=True, blank=True)
    archivo = models.FileField(upload_to='videollamada/', blank=True, null=True)
    video = models.FileField(upload_to='videollamada/', blank=True, null=True)
    instructor = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, null=True)
    miniatura = models.ImageField(upload_to='videollamada/',  blank=True, null=True)

    def __str__(self):
        return self.titulo


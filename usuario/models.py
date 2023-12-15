from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioPersonalizado(AbstractUser):
    profession = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='perfil/', default='perfil/user.png', blank=True, null=True)
    descripcion = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
    	return self.first_name + " " + self.last_name

class Solicitud(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)

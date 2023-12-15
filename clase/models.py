from django.db import models
from curso.models import Curso, Inscripcion
from usuario.models import UsuarioPersonalizado
from django.core.exceptions import ValidationError



class Clase(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    archivo_pdf = models.FileField(upload_to='pdfs/', blank=True, null=True,)
    video = models.FileField(upload_to='videos/')
    curso =  models.ForeignKey(Curso,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    contenido = models.TextField()
    id_autor = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    id_clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    id_respuesta = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True, related_name='respuestas')

class VistaClase(models.Model):
    estudiante = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_ultima_visualizacion = models.DateTimeField(auto_now=True)
 
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Curso)
admin.site.register(Categoria)
admin.site.register(Inscripcion)
admin.site.register(SolicitudCurso)
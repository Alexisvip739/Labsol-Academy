from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Examen)
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(CalificacionExamen)
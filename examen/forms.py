from django import forms

from .models import *


class FormExamen(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['nombre', 'descripcion', 'curso']

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto', 'examen']
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí la pregunta'}),
        }

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['texto', 'es_correcta', 'pregunta']

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = CalificacionExamen
        fields = ['calificacion','estudiante','examen']


    
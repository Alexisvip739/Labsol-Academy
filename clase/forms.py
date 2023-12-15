from django import forms
from .models import *
import fitz
import magic
from django.core.exceptions import ValidationError

class ClaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClaseForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].required = True
        self.fields['descripcion'].required = True
        self.fields['archivo_pdf'].required = False
        self.fields['video'].required = True
        self.fields['curso'].required = True

    def clean_archivo_pdf(self):
        archivo_pdf = self.cleaned_data.get('archivo_pdf')
        if archivo_pdf:
            if not archivo_pdf.name.endswith('.pdf'):
                raise ValidationError("El archivo debe tener extensión PDF.")
            try:
                doc = fitz.open(stream=archivo_pdf.read(), filetype="pdf")
                if len(doc) < 1:
                    raise ValidationError("El archivo PDF está vacío.")
            except Exception:
                raise ValidationError("El archivo no es un PDF válido.")
            finally:
                doc.close()
        return archivo_pdf

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            mime_type = magic.from_buffer(video.read(), mime=True)
            if mime_type != 'video/mp4':
                raise ValidationError("El archivo debe ser un video en formato MP4.")
        return video

    class Meta:
        model = Clase
        fields = ('titulo','descripcion','archivo_pdf','video','curso')

        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo del curso'}),
            'descripcion' : forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Descripción de la clase'}),
            'archivo_pdf' : forms.FileInput(attrs={'class': 'form-control'}),
            'video' : forms.FileInput(attrs={'class': 'form-control'}),
            'curso' : forms.TextInput(attrs={'type': 'hidden'}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido','id_autor','id_clase','id_respuesta']
        widgets = {
            'contenido': forms.Textarea(attrs={'id':'contenido' ,'class':'form-control rounded', 'placeholder':'Agregar un comentario', 'rows':'2', 'cols':'50'}),
            'id_autor': forms.HiddenInput(),
            'id_clase': forms.HiddenInput(),
            'id_respuesta': forms.HiddenInput()
        }

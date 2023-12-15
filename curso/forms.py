from django import forms
from .models import *
import fitz
from django.core.exceptions import ValidationError

class CursoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = UsuarioPersonalizado.objects.filter(user_type='instructor').exclude(solicitud__isnull=False)
        self.fields['nombre'].required = True
        self.fields['descripcion'].required = True
        self.fields['archivo_pdf'].required = False
        self.fields['miniatura'].required = True
        self.fields['instructor'].required = True
        self.fields['etiquetas'].required = True

    def clean_archivo_pdf(self):
        archivo_pdf = self.cleaned_data.get('archivo_pdf')
        if archivo_pdf:
            if not archivo_pdf.name.endswith('.pdf'):
                raise ValidationError("El archivo debe tener extensión PDF.")
            if archivo_pdf.size > 1 * 1024 * 1024:
                raise ValidationError("El Archivo pdf debe ser menor o igual a 1MB.")
            try:
                doc = fitz.open(stream=archivo_pdf.read(), filetype="pdf")
                if len(doc) < 1:
                    raise ValidationError("El archivo PDF está vacío.")
            except Exception:   
                raise ValidationError("El archivo no es un PDF válido.")
            finally:
                doc.close()
        return archivo_pdf
        
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion', 'miniatura', 'instructor', 'etiquetas', 'archivo_pdf']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese el título del curso'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':"3", 'placeholder':'Ingrese una descripción del curso'}),
            'etiquetas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input '}),
            'archivo_pdf': forms.FileInput(attrs={'class': 'form-control'}),
            'miniatura': forms.FileInput(attrs={'class': 'form-control'} ),
            'instructor': forms.Select(attrs={'class': 'form-select'}),
        }


class EtiquetaForm(forms.ModelForm):

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Categoria.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("La categoría ya está registrada, por lo tanto, no se pudo guardar.")
        return nombre

    class Meta:
        model = Categoria
        fields = ('nombre','descripcion','miniatura')


class FormInscripcion(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ('estudiante', 'curso')
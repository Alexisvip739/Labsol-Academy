from django import forms
from .models import Videollamada
from usuario.models import UsuarioPersonalizado

class FormVideollamada(forms.ModelForm):

    class Meta:
        model = Videollamada
        fields = ['titulo', 'descripcion', 'enlace', 'fecha_reunion', 'archivo', 'hora', 'instructor', 'miniatura']
        descripcion = forms.CharField(widget=forms.Textarea)
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título de la conferencia'}),
            'enlace': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la URL'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class':'form-control'}),
            'fecha_reunion':  forms.TextInput(attrs={'class': 'form-control', 'type':'date'}),
            'instructor': forms.Select(attrs={'class': 'form-select'}),
            'descripcion':forms.Textarea(attrs={'rows': 0, 'cols': 10, 'class': 'form-control'}),
            'miniatura': forms.FileInput(attrs={'class': 'form-control'}),
        }

    
    hora = forms.TextInput(attrs={'type': 'time'})
    def __init__(self, *args, **kwargs):
        super(FormVideollamada, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = UsuarioPersonalizado.objects.filter(user_type='instructor').exclude(solicitud__isnull=False)
        self.fields['titulo'].required = True
        self.fields['descripcion'].required = True
        self.fields['enlace'].required = True
        self.fields['fecha_reunion'].required = True
        self.fields['archivo'].required = False
        self.fields['hora'].required = True
        self.fields['instructor'].required = True
        self.fields['miniatura'].required = True
        

class FormVideollamadaEditar(forms.ModelForm):
    class Meta:
        model = Videollamada
        fields = ['titulo', 'descripcion', 'enlace', 'fecha_reunion', 'archivo', 'hora', 'instructor', 'miniatura', 'video']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título de la conferencia'}),
            'enlace': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la URL'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class':'form-control'}),
            'fecha_reunion':  forms.TextInput(attrs={'class': 'form-control', 'type':'date'}),
            'instructor': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'rows': 0, 'cols': 10, 'class': 'form-control'}),
            'miniatura': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'})  # Agregado el widget para el campo 'video'
        }

    def __init__(self, *args, **kwargs):
        super(FormVideollamadaEditar, self).__init__(*args, **kwargs)
        self.fields['video'].required = True
        # Resto del código para configurar campos requeridos u otras personalizaciones específicas para la edición

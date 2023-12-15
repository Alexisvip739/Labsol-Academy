from django import forms
from .models import Notificacion

class NotificacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asunto'].required = True
        self.fields['descripcion'].required = True

        # Define los widgets aquí, en el método __init__
        self.fields['asunto'].widget = forms.TextInput(attrs={'id': 'id_notificacion_asunto',
                                                              'class': 'form-control', 
                                                              'placeholder':'Escribe el asunto de la notificación aquí'})
        
        self.fields['descripcion'].widget = forms.Textarea(attrs={'id':'id_notificacion_descripcion',
                                                                  'rows': 8, 
                                                                  'class': 'form-control', 
                                                                  'placeholder':'Escribe la descripción aquí'})
        
    
    class Meta:
        model = Notificacion
        exclude = ['fecha_creacion']
        fields = ['asunto', 'descripcion', 'creador']
        
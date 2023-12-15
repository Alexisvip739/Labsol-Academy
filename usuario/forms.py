from django import forms
from .models import UsuarioPersonalizado
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
import magic
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import sys
from django.contrib.auth.forms import PasswordResetForm

class FormUsuario(forms.ModelForm):

    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'first_name', 'last_name', 'profession', 'email', 'user_type', 'password', 'profile_picture', 'descripcion']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos completos'}),
            'profession': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nivel académico actual o profesión actual'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'user_type': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Seleccione el tipo de usuario correspondiente'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de usuario'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese una contraseña'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Ingrese una descripción del tú perfil'}),
        }

    TIPOS_USUARIO = (
        (None, 'Seleccione una opción'),
        ('instructor', 'Instructor'),
        ('estudiante', 'Estudiante'),
        ('admin', 'Administracion')
    )
    
    user_type = forms.ChoiceField(choices=TIPOS_USUARIO, label='Tipo de Usuario', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(FormUsuario, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['profession'].required = False
        self.fields['profile_picture'].required = False
        self.fields['email'].required = True
        self.fields['user_type'].required = True
        self.fields['username'].required = True
        self.fields['password'].required = True
        

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password, self.instance)
        return password
    
    def optimized_image(self):
        picture = self.cleaned_data.get('profile_picture')
        img = Image.open(picture)

        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG', optimize=True, quality=15)
        optimized_image = InMemoryUploadedFile(output_buffer, 'ImageField', picture.name, 'image/jpeg', sys.getsizeof(output_buffer), None)

        return optimized_image

    def save(self, commit=True):
        user = super(FormUsuario, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class FormUpdateUsuario(FormUsuario):
    
    def __init__(self, *args, **kwargs):
        super(FormUpdateUsuario, self).__init__(*args, **kwargs)
        del self.fields['password']
        
    def save(self, commit=True, *args, **kwargs):
        return super(FormUsuario, self).save(commit, *args, **kwargs)
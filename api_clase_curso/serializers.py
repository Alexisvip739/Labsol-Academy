from clase.models import Clase, VistaClase
from curso.models import Curso, Inscripcion, SolicitudCurso
from usuario.models import Solicitud
from rest_framework import serializers

from usuario.models import UsuarioPersonalizado

class ClaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'
class CursoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class InscripcionSerializers(serializers.ModelSerializer):
    class Meta:
        model=Inscripcion
        fields = '__all__'

class ClaseVistaSerializers(serializers.ModelSerializer):
    class Meta:
        model=VistaClase
        fields = '__all__'

class UsuarioPersonalizadoSerializers(serializers.ModelSerializer):
    class Meta:
        model=UsuarioPersonalizado
        fields='__all__'
        
class SolicitudSerializers(serializers.ModelSerializer):
    class Meta:
        model = SolicitudCurso
        fields = '__all__'
        
class SolicitudUsuarioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'

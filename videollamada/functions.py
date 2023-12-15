from notificacion.views import  *
from usuario.models import UsuarioPersonalizado
import magic
from django.db.models import Q

def validar_video(video):
    mime = magic.from_buffer(video.read(1024), mime=True)

    if not mime.startswith('video/'):
        return False
    else:
        return True


def enviar_correos_general(datos):
    usuarios = UsuarioPersonalizado.objects.filter(
        Q(user_type='instructor') | Q(user_type='admin') | Q(user_type='estudiante')
        ).exclude(solicitud__isnull=False)
    
    for usuario in usuarios:
        if usuario.email:
            enviar_correo_videollamada(usuario, datos)


def enviar_correos_de_video(datos):
    usuarios = UsuarioPersonalizado.objects.filter(
        Q(user_type='instructor') | Q(user_type='admin') | Q(user_type='estudiante')
        ).exclude(solicitud__isnull=False)
    
    for usuario in usuarios:
        if usuario.email:
            enviar_correo_video(usuario, datos)
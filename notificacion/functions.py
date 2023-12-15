from usuario.models import UsuarioPersonalizado
from django.conf import settings
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def enviar_correo_usuario(usuario, tipo_usuario, notificacion):
    if( usuario.is_superuser and tipo_usuario == 'Todos'):
        registros = UsuarioPersonalizado.objects.exclude(id=usuario.id)
        pass
    elif ( usuario.user_type == 'admin' and tipo_usuario == 'Todos'):
        registros = UsuarioPersonalizado.objects.exclude(user_type='admin')
        pass
    else:
        registros = UsuarioPersonalizado.objects.filter(user_type=tipo_usuario)
        
    for registro in registros:
        enviar_correo(registro, notificacion)
    

def enviar_correo(usuario, datos):
    subject = f'Notificacion para {usuario.first_name} {usuario.last_name}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email]

    # Renderiza el contenido del correo en HTML usando una plantilla
    html_message = render_to_string('notificacion/notificacion_correo.html', {'notificacion': datos})

    # Obtiene el contenido de texto plano a partir del contenido HTML
    text_message = strip_tags(html_message)

    # Crea una instancia de EmailMultiAlternatives para enviar contenido HTML y de texto plano
    email = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")  # Adjunta el contenido HTML

    # Envía el correo
    email.send()
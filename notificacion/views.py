from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.paginator import Paginator

from notificacion.forms import NotificacionForm
from notificacion.functions import enviar_correo_usuario
from notificacion.models import Notificacion

def enviar_correo_videollamada(usuario, datos):
    subject = 'INVITACIÓN A NUEVA CONFERENCIA'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email]

    # Renderiza el contenido del correo en HTML usando una plantilla
    html_message = render_to_string('notificacion/notificacion_videollamada.html', {'videollamada': datos})

    # Obtiene el contenido de texto plano a partir del contenido HTML
    text_message = strip_tags(html_message)

    # Crea una instancia de EmailMultiAlternatives para enviar contenido HTML y de texto plano
    email = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")  # Adjunta el contenido HTML

    # Envía el correo
    email.send()


def enviar_correo_video(usuario, nombre):
    subject = 'Conferencia disponible'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email]

    # Renderiza el contenido del correo en HTML usando una plantilla
    html_message = render_to_string('notificacion/notificacion_video.html', {'videollamada': nombre})

    # Obtiene el contenido de texto plano a partir del contenido HTML
    text_message = strip_tags(html_message)

    # Crea una instancia de EmailMultiAlternatives para enviar contenido HTML y de texto plano
    email = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")  # Adjunta el contenido HTML

    # Envía el correo
    email.send()
    
def lista_notificacion(request):
    
    # Obtenemos el historial de notificaciones del usuario
    if request.user.user_type == 'instructor':
        lista = Notificacion.objects.filter(creador = request.user)
    else:
        lista = Notificacion.objects.all()
    
    form = NotificacionForm()
        
    paginator = Paginator(lista,10)
    numero_de_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numero_de_pagina)
    
    context = {
        'pagination': page_obj,
        'form_notificacion': form
    }
    
    return render(request, 'notificacion/notificacion_general.html', context)

def enviar_notificacion(request):
    if request.method == 'POST':
        form = NotificacionForm(request.POST)
        if form.is_valid():
            notificacion = form.save()
            enviar_correo_usuario(request.user, request.POST.get("tipo_usuario"), notificacion)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors':form.errors})
    else:
        return JsonResponse({'success': False, 'error':'Solicitud rechazada'})
    
    
def detalle_notificacion(request, notificacion_id):
    notificacion = Notificacion.objects.get(id=notificacion_id)
    
    context = {
        'notificacion': notificacion
    }
    return render(request, 'notificacion/detalle_notificacion_general.html', context)
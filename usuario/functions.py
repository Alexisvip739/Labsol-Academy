from django.db.models import Q
from .models import UsuarioPersonalizado, Solicitud
from .forms import FormUsuario
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def procesar_registro_interno(usuario, request, password1):
    enviar_correo_registro(usuario, password1)

    messages.success(request, 'Ha sido agregado satisfactoriamente el usuario.')

    redirect_url = None
    if usuario.user_type == 'estudiante':
        redirect_url = reverse('usuario:lista_estudiantes')

    elif usuario.user_type == 'instructor':
        redirect_url = reverse('usuario:lista_instructores')

    else:
        redirect_url = reverse('usuario:lista_administradores')

    return JsonResponse({'success': True, 'redirectUrl': redirect_url})


def procesar_registro_externo(usuario):
    if usuario.user_type == 'instructor':
        generar_solicitud(usuario)
        mensaje = 'Tú cuenta ha sido registrada correctamente. Recibirás una confirmación por correo electrónico, cuando sea validado tú acceso.'
    else:
        mensaje = 'Tú cuenta ha sido registrada correctamente.'
    return JsonResponse({'success': True, 'message': mensaje})


def enviar_correo_registro(usuario, password1):
    subject = 'Bienvenido a Labsol Academy'
    message = f'Hola {usuario.first_name}. \n\n Un administrador de Labsol Academy te ha dado el acceso al sistema, para que puedas hacer uso de el. \n\n Tús datos son los siguientes: \n\n Usuario: {usuario.username} \n Contraseña: {password1}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email]

    # Renderiza el contenido del correo en HTML usando una plantilla
    html_message = render_to_string('notificacion/notificacion_registro_usuario.html',
                                    {'usuario': usuario, 'password1': password1})

    # Obtiene el contenido de texto plano a partir del contenido HTML
    text_message = strip_tags(html_message)

    # Crea una instancia de EmailMultiAlternatives para enviar contenido HTML y de texto plano
    email = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")  # Adjunta el contenido HTML

    email.send()


def enviar_correo_registros(usuario):
    subject = 'Bienvenido a Labsol Academy'
    message = f'Hola {usuario.first_name}. \n\n Un administrador de Labsol Academy te ha dado el acceso al sistema, para que puedas hacer uso de el. \n\n Tús datos son los siguientes: \n\n Usuario: {usuario.username} \n Contraseña: {usuario.password}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email]

    send_mail(subject, message, from_email, recipient_list)


def enviar_correo_aceptacion(usuario):
    subject = 'Bienvenido a Labsol Academy'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email]

    # Renderiza el contenido del correo en HTML usando una plantilla
    html_message = render_to_string('notificaciones.html', {'usuario': usuario})

    # Obtiene el contenido de texto plano a partir del contenido HTML
    text_message = strip_tags(html_message)

    # Crea una instancia de EmailMultiAlternatives para enviar contenido HTML y de texto plano
    email = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")  # Adjunta el contenido HTML

    # Envía el correo
    email.send()


def enviar_correo_notificacion(nombre_del_curso, recipient_list, asunto, descripcion):
    subject = "Labsol Academy - Notificación del curso " + str(nombre_del_curso)
    from_email = settings.EMAIL_HOST_USER

    # Renderiza el contenido del correo en HTML usando una plantilla
    html_message = render_to_string('notificaciones_curso.html',
                                    {'nombre_del_curso': nombre_del_curso, 'asunto': asunto,
                                     'descripcion': descripcion})

    # Obtiene el contenido de texto plano a partir del contenido HTML
    text_message = strip_tags(html_message)

    # Crea una instancia de EmailMultiAlternatives para enviar contenido HTML y de texto plano
    email = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")  # Adjunta el contenido HTML

    # Envía el correo
    email.send()


def generar_solicitud(usuario):
    solicitud = Solicitud(usuario=usuario)
    solicitud.save()


def get_usuarios(request, user_type):
    tipos_usuarios = {
        'estudiante': {
            'filtro': Q(user_type='estudiante'),
            'titulo': 'estudiantes'
        },
        'instructor': {
            'filtro': Q(user_type='instructor', solicitud__isnull=True),
            'titulo': 'instructores'
        },
        'admin': {
            'filtro': Q(user_type='admin'),
            'titulo': 'administradores'
        }
    }

    tipo = user_type.lower()
    tipo_usuario = tipos_usuarios.get(tipo)

    if not tipo_usuario:
        # Manejar tipo de usuario no válido
        return render(request, 'usuario/lista_usuarios.html')

    usuarios = UsuarioPersonalizado.objects.filter(tipo_usuario['filtro'])
    form = FormUsuario()
    solicitud = Solicitud.objects.all()

    paginator = Paginator(usuarios, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    contexto = {
        'pagination': page_obj,
        'tipo_usuarios': tipo_usuario['titulo'],
        'forms': form,
        'tipo': tipo,
        'direccion_url': 'usuario:registro',
        'actividad': 'Agregar un nuevo usuario',
        'cantidad': solicitud.count() if tipo == 'instructor' else None
    }

    return render(request, 'usuario/lista_usuarios.html', contexto)


def enviar_correo_aceptacion1(usuario):
    subject = 'Bienvenido a Labsol Academy'
    message = f'Hola {usuario.first_name}. \n\n Un administrador de Labsol Academy te ha aceptado tu solicitud de acceso al sistema. \n\n'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email]
    send_mail(subject, message, from_email, recipient_list)


def enviar_correo_rechazado(usuario):
    subject = 'Notificación de Labsol Academy'
    message = f'Hola {usuario.first_name}. \n\n Tu solicitud de acceso al sistema ha sido rechadaza, si tienes alguna duda, comunicate con los administradores del sistema. \n\n'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email]
    send_mail(subject, message, from_email, recipient_list)


def validar_tipo(tipo):
    if tipo == 'administradores':
        return 'admin'
    if tipo == 'estudiantes':
        return 'estudiante'
    if tipo == 'instructores':
        return 'instructor'


def rutas(tipo):
    if tipo == 'estudiante':
        return redirect('usuario:lista_estudiantes')
    elif tipo == 'instructor':
        return redirect('usuario:lista_instructores')
    else:
        return redirect('usuario:lista_administradores')

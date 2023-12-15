from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from curso.models import Categoria, Curso
from .forms import FormUpdateUsuario, FormUsuario
from .functions import *
from .models import UsuarioPersonalizado
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


# Clase que define la ruta del template personalizado del correo electrónico, el cual contiene el enlace para restablecer la contraseña. 
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'usuario/passwordReset/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


def pagina_no_encontrada(request, exception):
    return render(request, '404_template.html', status=404)


class UserLoginView(LoginView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser or self.request.user.user_type in ['admin']:
                return redirect('curso:lista_cursos')
            elif self.request.user.user_type == 'instructor':
                return redirect('curso:lista_cursos_instructor')
            else:
                return redirect('curso:lista_cursos_estudiante')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actividad'] = 'Registro de usuarios'
        context['act'] = 'externo'
        context['cursos'] = Curso.objects.exclude(solicitudcurso__curso__isnull=False)[:15]
        context['etiquetas'] = Categoria.objects.all()[:15]
        context['instructores'] = UsuarioPersonalizado.objects.filter(user_type='instructor', solicitud__isnull=True)[
                                  :4]
        context['forms'] = FormUsuario()
        context['direccion_url'] = 'usuario:registro'

        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            solicitud_instructor = Solicitud.objects.filter(usuario=user).exists()

            if not solicitud_instructor:
                login(request, user)

                if user.is_superuser or user.user_type in ['admin']:
                    return JsonResponse({'success': True, 'redirectUrl': 'curso/cursos'})
                elif user.user_type == 'instructor':
                    return JsonResponse({'success': True, 'redirectUrl': 'curso/cursos_instructor'})
                else:
                    return JsonResponse({'success': True, 'redirectUrl': 'curso/inicio'})
            else:
                return JsonResponse({'success': False, 'errors': [
                    'Esta cuenta no ha sido validada por los administradores del sistema.']})
        else:
            return JsonResponse({'success': False, 'errors': ['Usuario y/o contraseña son incorrectos.']})


def registro(request):
    if request.method == 'POST':
        form = FormUsuario(request.POST)
        if form.is_valid():
            usuario = form.save()
            password1 = request.POST.get('password')
            if request.user.is_authenticated:
                return procesar_registro_interno(usuario, request, password1)
            else:
                return procesar_registro_externo(usuario)
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = FormUsuario()
        return render(request, 'usuario/form_registrar_usuario.html', {'forms': form})


@login_required
@user_passes_test(lambda user: user.user_type == 'admin' or user.is_superuser)
def get_estudiantes(request):
    return get_usuarios(request, 'estudiante')


@login_required
@user_passes_test(lambda user: user.user_type == 'admin' or user.is_superuser)
def get_instructores(request):
    return get_usuarios(request, 'instructor')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_administradores(request):
    return get_usuarios(request, 'admin')


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')


@login_required
@user_passes_test(lambda user: user.user_type == 'admin' or user.is_superuser)
def get_solicitud(request):
    solicitud = Solicitud.objects.all()
    paginator = Paginator(solicitud, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'usuario/solicitud/solicitud_list.html', {"pagination": page_obj})


@login_required
@user_passes_test(lambda user: user.user_type == 'admin' or user.is_superuser)
def procesar_solicitud(request, solicitud_id, argumento):
    solicitud = Solicitud.objects.get(id=solicitud_id)
    usuario = solicitud.usuario
    if argumento == 'aceptar':
        messages.success(request, 'El instructor ha sido aceptado correctamente.')
        enviar_correo_aceptacion(usuario)
    else:
        enviar_correo_rechazado(usuario)
        usuario = UsuarioPersonalizado.objects.get(id=usuario.id).delete()
        messages.success(request, 'La solicitud se ha eliminado correctamente.')
    solicitud.delete()
    return redirect('usuario:lista_solicitud')


@login_required
@user_passes_test(lambda user: user.user_type in ['instructor', 'admin', 'estudiante'])
def perfil(request):
    usuario_actual = request.user
    if request.method == 'POST':
        form = FormUpdateUsuario(request.POST, request.FILES, instance=usuario_actual)
        if form.is_valid():
            if 'profile_picture' in request.FILES:
                usuario_actual.profile_picture = form.optimized_image()
            usuario_actual = form.save()
            update_session_auth_hash(request, usuario_actual)
            messages.success(request, 'Se ha editado correctamente el perfil')
            return redirect('usuario:perfil')
        else:
            messages.error(request, form.errors)
    else:
        form = FormUsuario(instance=usuario_actual)
    contexto = {'forms': form}
    if request.user.user_type != 'estudiante' :
        return render(request, 'usuario/perfil_instructor.html', contexto)
    else:
        return render(request, 'usuario/perfil.html', contexto)


@login_required
@user_passes_test(lambda user: user.user_type == 'admin' or user.is_superuser)
def editar_usuario(request, usuario_id):
    usuario = UsuarioPersonalizado.objects.get(id=usuario_id)
    if request.method == 'POST':
        form = FormUsuario(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'El usuario ha sido editado correctamente.')
            return rutas(usuario.user_type)
        else:
            messages.error(request, form.errors)
    else:
        form = FormUsuario(instance=usuario)
    return render(request, 'usuario/editar-usuario.html', {'forms': form})


def eliminar_usuario(request, usuario_id):
    try:
        usuario = UsuarioPersonalizado.objects.get(id=usuario_id)
        tipo = usuario.user_type
        usuario.delete()
        messages.success(request, 'El usuario ha sido eliminado correctamente.')
        return rutas(tipo)
    except UsuarioPersonalizado.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
    return redirect('usuario:registro')


def politicas_privacidad(request):
    return render(request, 'usuario/politicas.html', {'politicas': False})

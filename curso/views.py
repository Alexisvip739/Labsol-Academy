from django.shortcuts import get_object_or_404, render, redirect
from .models import Curso, SolicitudCurso, Inscripcion
from django.db.models import Q
from django.core.paginator import Paginator
from .functions import *
from usuario.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from examen.models import Examen
from clase.models import Clase, VistaClase
from clase.forms import ClaseForm
from django.db.models import Count

from usuario.functions import enviar_correo_notificacion
from notificacion.forms import NotificacionForm
from notificacion.models import NotificacionCurso
from django.urls import reverse


def pagina_no_encontrada(request, exception):
    return render(request, '404_template.html', status=404)


# Create your views here.
def buscar_curso(request):
    # Obtener la cadena de búsqueda de los parámetros GET
    query = request.GET.get('q')

    if request.user.is_authenticated:
        # Filtrar cursos por titulo o nombre de etiqueta, valida que los cursos solo sean cursos validados por algun admin y además solo muestra cursos a los que no se ha inscrito
        cursos_ya_inscritos_por_usuario = Inscripcion.objects.filter(estudiante=request.user)
        ID_cursos_ya_inscritos_por_usuario = []
        # De los cursos obtengo los IDs
        for c in cursos_ya_inscritos_por_usuario:
            ID_cursos_ya_inscritos_por_usuario.append(c.curso.id)

        print(ID_cursos_ya_inscritos_por_usuario)
        cursos = Curso.objects.filter((Q(nombre__icontains=query) | Q(etiquetas__nombre__icontains=query)) & (
            Q(solicitudcurso__curso__isnull=True))).distinct()
        cursos = cursos.exclude(id__in=ID_cursos_ya_inscritos_por_usuario)
        print(cursos)
    else:
        # Filtrar cursos por titulo o nombre de etiqueta y valida que los cursos mostrados solo sean cursos validados por una admin.
        cursos = Curso.objects.filter((Q(nombre__icontains=query) | Q(etiquetas__nombre__icontains=query)) & Q(
            solicitudcurso__curso__isnull=True)).distinct()

    # Agregamos paginacion a los cursos
    paginator = Paginator(cursos, 10)

    numero_de_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numero_de_pagina)

    # Agrego informacion de contexto
    context = {}
    context['query'] = query
    context['page_obj'] = page_obj
    context['pagination'] = page_obj
    context['actividad'] = 'Registro de usuarios'
    context['act'] = 'externo'
    context['forms'] = FormUsuario()
    context['direccion_url'] = 'usuario:registro'
    return render(request, 'curso/busqueda.html', context)


# @login_required
# @user_passes_test(lambda user: user.user_type == 'administrador' or user.is_superuser)
def lista_cursos(request):
    cursos = Curso.objects.filter(solicitudcurso__isnull=True)
    curso_solicitud = SolicitudCurso.objects.all()
    contexto = get_pagination_context(cursos, request, curso_solicitud)
    return render(request, 'curso/lista-curso.html', contexto)


def get_solicitud_curso(request):
    solicitud = SolicitudCurso.objects.all()
    paginator = Paginator(solicitud, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    usuario = UsuarioPersonalizado.get_or_c
    return render(request, 'curso/solicitud/solicitud_lista.html', {"pagination": page_obj})


def get_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    etiquetas = curso.etiquetas.all()
    examenes = Examen.objects.filter(curso=curso)
    clases = Clase.objects.filter(curso=curso)
    if not request.user.is_authenticated or request.user.user_type == 'estudiante':
        contexto = {
            'curso': curso,
            'clases': clases,
            'etiquetas': etiquetas,
            'num_clases': clases.count(),
            'num_examen': examenes.count(),
            'instructor_fecha_de_inscripcion': curso.instructor.date_joined.date(),
            'cursos_totales_instructor': Curso.objects.filter(instructor=curso.instructor,
                                                              solicitudcurso__isnull=True).count()
        }
        return render(request, 'curso/ver_curso_externo.html', contexto)
    else:
        contexto = {
            'curso': curso,
            'examen': examenes,
            'form': ClaseForm(),
            'clases': clases,
            'etiquetas': etiquetas,
            'num_clases': clases.count(),
            'num_examen': examenes.count(),
            'form_notificacion': NotificacionForm()
        }
        return render(request, 'curso/ver_curso_interno.html', contexto)


def desinscribir_estudiantes(request, curso_id):
    if request.method == 'GET':
        inscripcion_eliminada = Inscripcion.objects.filter(curso=curso_id, estudiante=request.user).first()
        if inscripcion_eliminada:
            inscripcion_eliminada.delete()
            estudiante = request.user  # Fetching the user from the request
            eliminar_ultimo_visto = VistaClase.objects.filter(curso=curso_id, estudiante=estudiante)
            if eliminar_ultimo_visto:
                eliminar_ultimo_visto.delete()

    return redirect('curso:cursos_inscritos')


@login_required
@user_passes_test(lambda user: user.user_type == 'instructor')
def get_curso_instructor(request):
    cursos = Curso.objects.filter(instructor=request.user, solicitudcurso__isnull=True)
    contexto = get_pagination_context(cursos, request)
    return render(request, 'curso/lista-curso.html', contexto)


@login_required
@user_passes_test(lambda user: user.user_type == 'estudiante')
def lista_cursos_estudiante(request):
    cursos_con_inscripcion = Curso.objects.filter(inscripcion__estudiante=request.user)[:3]

    cursos_ya_inscritos_por_estudiante = Inscripcion.objects.filter(estudiante=request.user)
    lista_de_ids = []
    for inscripcion in cursos_ya_inscritos_por_estudiante:
        lista_de_ids.append(inscripcion.curso.id)

    cursos_sin_inscripcion = Curso.objects.exclude(Q(solicitudcurso__curso__isnull=False) | Q(id__in=lista_de_ids))

    etiquetas = Categoria.objects.all()[:15]
    contexto = {
        'cursos_sin_inscripcion': cursos_sin_inscripcion,
        'cursos_con_inscripcion': cursos_con_inscripcion,
        'etiquetas': etiquetas
    }
    return render(request, 'curso/inicio.html', contexto)


# Muestra todos los cursos a los que el alumno se puede inscribir (Disponibles para él)
@login_required
@user_passes_test(lambda user: user.user_type == 'estudiante')
def cursos_disponibles_para_estudiante(request):
    cursos_ya_inscritos_por_estudiante = Inscripcion.objects.filter(estudiante=request.user)
    lista_de_ids = []
    for inscripcion in cursos_ya_inscritos_por_estudiante:
        lista_de_ids.append(inscripcion.curso.id)

    cursos_totales = Curso.objects.exclude(Q(solicitudcurso__curso__isnull=False) | Q(id__in=lista_de_ids))

    paginator = Paginator(cursos_totales, 15)

    numero_de_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numero_de_pagina)

    context = {}
    context['pagination'] = page_obj

    return render(request, 'curso/cursos_disponibles_estudiante.html', context)


@login_required
@user_passes_test(lambda user: user.user_type == 'estudiante')
def inscribir_curso(request, curso_id):
    datos = {'estudiante': request.user.id, 'curso': curso_id}
    form = FormInscripcion(datos)
    if form.is_valid:
        form.save()
        messages.success(request, 'Te has inscrito correctamente al curso')
    else:
        messages.error(request, 'Hubo un error al inscribirse al curso')
    return redirect('curso:lista_cursos_instructor')


@login_required
@user_passes_test(lambda user: user.user_type == 'instructor')
def get_curso_instructor(request):
    cursos = Curso.objects.filter(instructor=request.user, solicitudcurso__isnull=True)
    contexto = get_pagination_context(cursos, request)
    return render(request, 'curso/lista-curso.html', contexto)


# @login_required
# @user_passes_test(lambda user: user.user_type in ['instructor','admin'] or user.is_superuser)
def crear_curso(request):
    if request.method == 'POST':

        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save()

            if request.user.user_type == 'instructor':
                enviar_solicitud_curso(curso)
                messages.success(request,
                                 'El curso ha sido agregado satisfactoriamente, espere que sea aprobado por algún administrador del sistema.')
                return JsonResponse({'success': True})
            else:
                messages.success(request, 'El curso ha sido agregado satisfactoriamente.')
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    if request.user.user_type == 'instructor':
        return redirect('curso:lista_cursos_instructor')
    else:
        return redirect('curso:lista_cursos')


@login_required
@user_passes_test(lambda user: user.user_type in ['instructor', 'admin'] or user.is_superuser)
def editar_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'El curso ha sido editado correctamente.')
            return redirect('curso:lista_cursos')
        else:
            messages.error(request, form.errors)
    else:
        form = CursoForm(instance=curso)
    return render(request, 'curso/editar-curso.html', {'form': form, 'miniatura_url': curso.miniatura.url})


@login_required
@user_passes_test(lambda user: user.user_type == 'admin' or user.is_superuser)
def agregar_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha agregado correctamente la etiqueta.')
        else:
            messages.error(request, form.errors)
    return redirect('curso:lista_cursos')


@login_required
@user_passes_test(lambda user: user.user_type == 'admin' or user.is_superuser)
def get_solicitud_curso(request):
    solicitud = SolicitudCurso.objects.all()
    paginator = Paginator(solicitud, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'curso/solicitud/solicitud_lista.html', {"pagination": page_obj})


@login_required
@user_passes_test(lambda user: user.user_type == 'admin' or user.is_superuser)
def procesar_solicitud_curso(request, solicitud_id, argumento):
    solicitud = SolicitudCurso.objects.get(id=solicitud_id)
    curso = solicitud.curso
    if argumento == 'aceptar':
        # enviar_correo_aceptacion_curso(curso)
        messages.success(request, 'El curso ha sido aceptado correctamente.')
    else:
        # enviar_correo_rechazado(usuario)
        curso = Curso.objects.get(id=curso.id).delete()
        messages.success(request, 'La solicitud se ha eliminado correctamente.')
    solicitud.delete()
    return redirect('curso:lista_solicitud_curso')


@login_required
def grafica_cursos(request):
    cursos_populares, cursos_menos_populares = obtener_cursos_populares_y_menos_populares(request.user)
    grafica_cursos_popular = generar_grafica_cursos(cursos_populares, 'Cursos con mayores inscripciones')
    grafica_cursos_menos_populares = generar_grafica_cursos(cursos_menos_populares, 'Cursos con menores inscripciones')

    contexto = {
        'grafica_base64_populares': grafica_cursos_popular,
        'grafica_base64_menos_populares': grafica_cursos_menos_populares,
        'cursos_populares': cursos_populares,
        'cursos_menos_populares': cursos_menos_populares,
    }
    return render(request, 'curso/grafica_curso.html', contexto)


def tabla_con_cursos(request):
    inscripciones = obtener_avance_estudiantes(request.user)

    datos = {}
    for inscripcion in inscripciones.distinct():
        datos[inscripcion.curso] = len(inscripciones.filter(curso=inscripcion.curso))

    paginator = Paginator(list(datos.items()), 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    contexto = {'pagination': page_obj, }

    return render(request, 'curso/tabla_con_cursos.html', contexto)


@login_required
def mostrar_avance_estudiante(request, curso):
    curso_con_estudiantes = Curso.objects.get(nombre=curso)
    clases = Clase.objects.filter(curso__nombre=curso_con_estudiantes.nombre)
    inscripciones = Inscripcion.objects.filter(curso=curso_con_estudiantes)

    datos = []
    for inscripcion in inscripciones:
        datos.append(avance_estudiante_en_curso(curso_con_estudiantes, clases, inscripcion.estudiante))

    paginator = Paginator(datos, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    contexto = {'pagination': page_obj}
    return render(request, 'curso/mostrar_avance_estudiante.html', contexto)


@login_required
def mostrar_porcentaje(request):
    return render(
        request,
        'curso/mostrar_porcentaje.html',
    )


@login_required
def cursos_inscritos(request):
    cursos_inscritos_estudiante = Curso.objects.filter(inscripcion__estudiante=request.user,
                                                       solicitudcurso__isnull=True)

    paginator = Paginator(cursos_inscritos_estudiante, 9)
    numero_de_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numero_de_pagina)
    # page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_obj.number,on_each_side=1, on_ends=2)
    contexto = {
        'cursos': page_obj,
        'pagination': page_obj
    }

    return render(request, 'curso/cursos_inscritos_de_estudiante.html', contexto)


@login_required
def alumnos_inscritos_curso(request, curso_id):
    inscripciones = Inscripcion.objects.filter(curso=curso_id).order_by('id')
    paginator = Paginator(inscripciones, 10)
    numero_de_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numero_de_pagina)
    contexto = {
        'pagination': page_obj,
        'contador_inscripcion': inscripciones.count()
    }
    return render(request, 'curso/inscripciones.html', contexto)


@login_required
def enviar_notificacion(request, curso_id):
    if request.method == 'POST':

        form = NotificacionForm(request.POST)
        print(request.POST)
        if form.is_valid():  # El asunto y la descripción estan correctos
            curso = get_object_or_404(Curso, pk=curso_id)  # El curso al cual se enviara la notificación existe

            # Valido que la notificación que quiere enviar el instructor sea para un curso del cual el es el dueño
            curso_del_propietario = Curso.objects.filter(Q(id=curso_id) & Q(instructor=request.user))
            if not curso_del_propietario.exists():  # El instructor no es dueño del curso
                return JsonResponse({'success': False, 'error': 'Acción no autorizada.'})

            # Extraigo los correos de los alumnos a los cuales se les enviara la notificación
            inscritos = Inscripcion.objects.filter(curso=curso)
            subject_del_correo = "Labsol - Notificación del curso: " + str(curso.nombre)
            recipient_list = []
            for inscrito in inscritos:
                recipient_list.append(inscrito.estudiante.email)

            # Se envia el correo a todos los inscritos al curso y guardamos en base de datos la notificación
            enviar_correo_notificacion(curso.nombre, recipient_list, request.POST.get('asunto'),
                                       descripcion=request.POST.get('descripcion'))
            nueva_notificacion = NotificacionCurso(asunto=request.POST.get('asunto'),
                                                   descripcion=request.POST.get('descripcion'), curso=curso,
                                                   creador=request.user)
            nueva_notificacion.save()

            URL_destino = reverse('curso:ver_curso', args=[curso_id])
            messages.success(request, 'Se ha enviado correctamente la notificacion')
            return JsonResponse({'success': True, 'redirectUrl': URL_destino})

        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    else:
        return JsonResponse({'success': False, 'error': 'Método no autorizado.'})


# Muestra las notificaciones que ha enviado un instructor en un curso
@login_required
def ver_notificaciones(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)  # El curso al cual se enviara la notificación existe

    # Valido que la notificaciones que quiere ver el instructor sean de un curso del cual el es el creador
    curso_del_propietario = Curso.objects.filter(Q(id=curso_id) & Q(instructor=request.user))

    if not curso_del_propietario.exists():  # El instructor no es dueño del curso
        return pagina_no_encontrada(request, "")

    # Extraigo todas las notificaciones creadas por el profesor ordenadas por fecha de la más reciente a la más antigua
    notificaciones = NotificacionCurso.objects.filter(curso=curso).order_by('-fecha_creacion')
    context = {}
    context['curso'] = curso

    paginator = Paginator(notificaciones, 15)

    numero_de_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numero_de_pagina)

    context = {}
    context['pagination'] = page_obj

    return render(request, 'notificacion/notificaciones_instructor.html', context)

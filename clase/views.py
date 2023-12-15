from examen.models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .forms import ClaseForm, ComentarioForm
from django.contrib import messages
from django.urls import reverse
from .models import Clase, Comentario,Curso
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import os
import datetime
from django.db.models import Q
from .functions import eliminar_archivo,comprimir_video
from django.shortcuts import render
from .models import VistaClase



def pagina_no_encontrada(request, exception):
    return render(request, '404_template.html', status=404)


@login_required
@user_passes_test(lambda user: user.user_type == 'instructor' )    
def crear_clase(request):
    if request.method == 'POST':
        curso_id = int(request.POST['curso']) # Curso al que pertenece la clase que se va a crear 
        curso = get_object_or_404(Curso, pk=curso_id)
        form = ClaseForm(request.POST, request.FILES)

        if form.is_valid():
            # Valido que la clase que quiere agregar el instructor sea para un curso del cual el es el dueño
            curso_del_propietario = Curso.objects.filter( Q(id=curso_id) & Q(instructor=request.user)  )
            if not curso_del_propietario.exists()  : # El instructor no es dueño del curso
                return JsonResponse({'success': False, 'error': 'Acción no autorizada.' })

            if 'video' not in request.FILES: # El campo de video esta vacio
                messages.error(request,'El campo de video está vacío')
                form = ClaseForm(initial={'curso': curso.id})
                return JsonResponse({'success': False, 'error': 'Selecciona un video para continuar.' }) 

            clase = form.save()

            # Creamos un timestamp para identificar de forma unica a cada video
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f_")
            cadena_timestamp = f"{timestamp}"
            video_no_comprimido = clase.video.path

            # Comprimir el video antes de guardarlo
            ruta_del_video_comprimido = comprimir_video(video_no_comprimido,cadena_timestamp)

            # Ocurrió un error durante la compresión de video.
            if ruta_del_video_comprimido == None:
                form = ClaseForm(initial={'curso': curso.id})
                return JsonResponse({'success': False, 'error': 'Se ha producido un error al intentar subir el video. Por favor, inténtalo de nuevo más tarde.' })

            # Guardar el video en la base de datos.
            clase.video = ruta_del_video_comprimido
            clase.save()

            # Eliminar el video no comprimido.
            eliminar_archivo(video_no_comprimido)
            
            # Redirigir hacia la página principal
            messages.success(request, 'La clase ha sido creada exitosamente.')
            curso = request.POST.get('curso')
            url_destino = reverse('curso:ver_curso', args=[curso])
            return JsonResponse({'success': True, 'redirectUrl': url_destino})
        
        else:
            return JsonResponse({'success': False, 'errors':form.errors})


@login_required
@user_passes_test(lambda user: user.user_type in ['instructor','admin'] or user.is_superuser)
def editar_clase(request):
    if request.method == 'POST':
        curso_id = int(request.POST['curso']) # Curso al que pertenece la clase que se va a crear 
        curso = get_object_or_404(Curso, pk=curso_id)
        clase = Clase.objects.get(id=request.POST.get('clase'))
        form = ClaseForm(request.POST, request.FILES, instance=clase)

        if form.is_valid():

            # Valido que la clase que quiere agregar el instructor sea para un curso del cual el es el dueño
            curso_del_propietario = Curso.objects.filter( Q(id=curso_id) & Q(instructor=request.user)  )
            if not curso_del_propietario.exists()  : # El instructor no es dueño del curso
                return JsonResponse({'success': False, 'error': 'Acción no autorizada.' })

            if 'video' in request.FILES: # se va a actualizar el video
                # Guardamos el video y los datos
                video_antiguo_path = os.path.join(settings.MEDIA_ROOT, str(request.POST['video_comp']) )
            
                clase_form = form.save()

                # Creamos un timestamp para identificar de forma unica a cada video
                timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f_")
                cadena_timestamp = f"{timestamp}"
                video_no_comprimido = clase_form.video.path

                # Comprimir el video antes de guardarlo
                ruta_del_video_comprimido = comprimir_video(video_no_comprimido,cadena_timestamp)

                # Ocurrió un error durante la compresión de video.
                if ruta_del_video_comprimido == None:
                    form = ClaseForm(initial={'curso': curso.id})
                    return JsonResponse({'success': False, 'error': 'Se ha producido un error al intentar subir el video. Por favor, inténtalo de nuevo más tarde.' })
                
                # Guardar el video en la base de datos.
                clase_form.video = ruta_del_video_comprimido

                # Eliminar el video no comprimido y el video antiguo.
                eliminar_archivo(video_no_comprimido)
                eliminar_archivo(video_antiguo_path)
            
            clase.save()
            messages.success(request, 'La clase ha sido editada correctamente.')
            url_destino = reverse('clase:ver_clase', args=[clase.id])
            return JsonResponse({'success': True, 'redirectUrl': url_destino})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        clase_id = request.POST.get('clase')
        clase = Clase.objects.get(id=clase_id)
        form = ClaseForm(instance=clase)
        return render(request, 'clase/editar_clase.html', {'form': form})



@login_required
@user_passes_test(lambda user: user.user_type == 'estudiante' )
def get_clase_estudiante(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)  # Obtén el objeto Curso
    clases = Clase.objects.filter(curso=curso)  # Filtra las clases relacionadas con ese curso
    
    if clases:
        paginator = Paginator(clases, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        clase_id = page_obj.object_list[0].id
        comentarios = Comentario.objects.filter(id_clase=clase_id, id_respuesta=None) 
        form = ComentarioForm(initial={'contenido':'', 'id_autor':request.user,'id_clase': clase_id, 'id_respuesta':None})
        
        examen = Examen.objects.filter(curso=curso).first()
        contexto = {
            'clase': page_obj,
            'comentarios': comentarios,
            'form': form,
            'curso': curso,  # Puedes pasar el objeto curso a la plantilla si lo necesitas
            'examen':examen,
        }
        return render(request, 'clase/clases_estudiante.html', contexto)
    
    else:
        return render(request, 'clase/clases_estudiante.html', context={'clase':None})


@login_required
@user_passes_test(lambda user: user.user_type in ['instructor','admin'] or user.is_superuser)
def get_clase(request, clase_id):
    clase = Clase.objects.get(id=clase_id)
    comentarios = Comentario.objects.filter(id_clase=clase_id, id_respuesta=None) 
    form = ClaseForm(instance=clase)
    form_comentario = ComentarioForm(initial={'contenido':'', 'id_autor':request.user,'id_clase': clase_id, 'id_respuesta':None})
    contexto = {
        'clase':clase,
        'comentarios': comentarios,
        'form':form,
        'form_comentario': form_comentario,
        'accion':'Editar'
    }
    return render(request,'clase/ver_clase.html',contexto)


@login_required
@user_passes_test(lambda user: user.user_type in ['instructor','admin'] or user.is_superuser)
def eliminar_clase(request, clase_id):
    clase = Clase.objects.get(id=clase_id)
    clase.archivo_pdf.delete()
    clase.video.delete()
    curso_id = clase.curso.id
    clase.delete()
    messages.success(request,'La clase ha sido borrada exitosamente.')
    url_destino = reverse('curso:ver_curso', args=[curso_id])
    return redirect(url_destino)

@login_required
def agregar_comentario(request):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors':form.errors})

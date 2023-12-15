from django.core.paginator import Paginator
from .models import Videollamada
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .functions import *
from django.urls import reverse
import datetime
from clase.functions import comprimir_video, eliminar_archivo
import os

def pagina_no_encontrada(request, exception):
    return render(request, '404_template.html', status=404)

def videollamadas(request):
    videollamadas = Videollamada.objects.all()

    paginator = Paginator(videollamadas, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    form = FormVideollamada()
    contexto = {
        'pagination': page_obj,
        'forms': form,
        'direccion_url': 'videollamada:crear_videollamada'
    }

    return render(request, 'videollamada/lista_videollamadas.html', contexto)

def get_videollamadas(request):
    videollamadas_con_video = Videollamada.objects.all()
    videos = []
    for i in videollamadas_con_video:
        if i.video:
            videos.append(i)

    paginator = Paginator(videos , 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    contexto = {
        'pagination': page_obj,
    }
    return render(request, 'videollamada/lista_conferencias.html', contexto)


def crear_videollamada(request):
    if request.method == 'POST':
        form = FormVideollamada(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            messages.success(request, 'Se ha agendado la reunión correctamente')
            enviar_correos_general(video)
        else:
            messages.error(request, form.errors)
    return redirect('videollamada:videollamada')


def subir_video(request):
    if request.method == 'POST':
        videollamada_id = request.POST.get('videollamada_llave')
        videollamada = Videollamada.objects.get(id=videollamada_id)
        video = request.FILES.get('video')
        if video and validar_video(video):
            videollamada.video = request.FILES.get('video')
            videollamada.save()
            videollamada = Videollamada.objects.get(id=videollamada_id)

            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f_")
            cadena_timestamp = f"{timestamp}"
            video_no_comprimido = videollamada.video.path

            # Comprimir el video antes de guardarlo
            ruta_del_video_comprimido = comprimir_video(video_no_comprimido,cadena_timestamp)

            # Ocurrió un error durante la compresión de video.
            if ruta_del_video_comprimido == None:
                form = ClaseForm(initial={'curso': curso.id})
                return JsonResponse({'success': False, 'error': 'Se ha producido un error al intentar subir el video. Por favor, inténtalo de nuevo más tarde.' })

            # Guardar el video en la base de datos.
            videollamada.video = ruta_del_video_comprimido
            videollamada.save()

            enviar_correos_de_video(videollamada.titulo)
            messages.success(request, 'Se ha agregado la reunión exitosamente')
        else:
            messages.error(request, 'Hubo un problema al almacenar la reunión, posible error en el archivo de video')
    return redirect('videollamada:videollamada')



def ver_videollamada(request, videollamada_id):
    videollamada = Videollamada.objects.get(id=videollamada_id)
    if request.user.user_type!='estudiante':
        form = FormVideollamadaEditar(instance=videollamada)
        form.fields['fecha_reunion'].input_formats = ['%d/%m/%Y']
        contexto = {
        'videollamada':videollamada,
        'forms':form,
        'direccion_url': 'videollamada:editar_video'
        }
        return render(request, 'videollamada/detalle_videollamada.html', contexto)
    else:
        contexto = {
        'videollamada':videollamada
        }
        return render(request, 'videollamada/detalle_conferencia.html', contexto)

def editar_video(request):
    id_videollamada = request.POST.get('videollamada_id')
    videollamada = Videollamada.objects.get(id=id_videollamada)
    if request.method == 'POST':
        form = FormVideollamadaEditar(request.POST, request.FILES, instance=videollamada)
        if form.is_valid():
            if 'video' in request.FILES:
                print(videollamada.video.url)
                video_antiguo_path = os.path.join(settings.MEDIA_ROOT, str(videollamada.video.url) )
            
                form = form.save()

                # Creamos un timestamp para identificar de forma unica a cada video
                timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f_")
                cadena_timestamp = f"{timestamp}"
                video_no_comprimido = form.video.path

                # Comprimir el video antes de guardarlo
                ruta_del_video_comprimido = comprimir_video(video_no_comprimido,cadena_timestamp)
                # Guardar el video en la base de datos.
                form.video = ruta_del_video_comprimido
                form.save()

                # Eliminar el video no comprimido y el video antiguo.
                eliminar_archivo(video_no_comprimido)
                eliminar_archivo(video_antiguo_path)
            messages.success(request, 'Se ha editado la videollamada correctamente')
        else:
            messages.error(request, form.errors)
    else:
        form = FormVideollamadaEditar(instance=videollamada)
    url = reverse('videollamada:detalle_video', args=[id_videollamada])
    return redirect(url)
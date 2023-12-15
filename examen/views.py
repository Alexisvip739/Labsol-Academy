from django.shortcuts import render, redirect
from django.db import transaction
from .models import *
from .forms import *
from django.contrib import messages
from django.urls import reverse
from .functions import *
import random
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def pagina_no_encontrada(request, exception):
    
    return render(request, '404_template.html', status=404)

def get_examen(request, examen_id):
    examen = Examen.objects.get(id=examen_id)
    preguntas = Pregunta.objects.filter(examen = examen)
    context = {
        'examen': examen,
        'preguntas': preguntas,
    }
    return render(request, 'examen/crear_examen.html', context)


def crear_pregunta(request):
    if request.method == 'POST':
        pregunta = request.POST.get('pregunta')
        examen = request.POST.get('examen')
        form_pregunta = PreguntaForm(data={'texto': pregunta, 'examen': examen})

        if form_pregunta.is_valid:
            pregunta_obj = form_pregunta.save()

            for i in range(1, 5):
                opcion = request.POST.get(f'respuesta{i}')
                es_correcta = request.POST.get(f'respuesta{i}-es_correcta')
                opcion_respuesta = {'texto': opcion, 'es_correcta': es_correcta, 'pregunta': pregunta_obj.id}
                form_respuesta = RespuestaForm(opcion_respuesta)
                if form_respuesta.is_valid :
                    form_respuesta.save()
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
            messages.success(request, 'La pregunta se ha almacenado correctamente.')
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        url = reverse('examen:detalles_examen', args=[examen])
    return redirect(url)


def crear_examen(request):
    if request.method == 'POST':
        form = FormExamen(request.POST)
        if form.is_valid():
            examen = form.save()
            messages.success(request,'Se ha creado el examen con exito, agrega las preguntas que sean necesarias')
            return render(request, 'examen/crear_examen.html', {'examen': examen})
    return redirect('iniciar_sesion')


def examen(request, examen_id):
    examen = Examen.objects.get(id=examen_id)
    preguntas_examen = Pregunta.objects.filter(examen=examen)

    # Check if the student has already completed the exam
    exa_estudiante = CalificacionExamen.objects.filter(estudiante=request.user, examen=examen_id).first()
    if exa_estudiante:
        return render(request, 'examen/examen_realizado.html', {'examen': examen, 'porcentaje': exa_estudiante.calificacion})

    preguntas_respuestas = []
    for pregunta in preguntas_examen:
        respuestas = list(Respuesta.objects.filter(pregunta=pregunta))
        random.shuffle(respuestas)
        preguntas_respuestas.append((pregunta, respuestas))

    if request.method == 'POST':
        puntaje = 0
        for pregunta, respuestas in preguntas_respuestas:
            respuesta_seleccionada = request.POST.get('respuesta-{}'.format(pregunta.id))
            respuesta = Respuesta.objects.get(id=respuesta_seleccionada)
            if respuesta.es_correcta:
                puntaje += 1
        porcentaje = calcular_promedio(puntaje, preguntas_examen.count())
        calificacion = {'calificacion': porcentaje, 'estudiante': request.user.id, 'examen': int(examen.id)}
        CalificacionForm(calificacion).save()
        mensaje(request, porcentaje)
        context = {
            'examen': examen,
            'total_preguntas': len(preguntas_respuestas),
            'puntaje': puntaje,
            'total_incorrecta': len(preguntas_respuestas) - puntaje,
            'porcentaje': porcentaje
        }
        return render(request, 'examen/realizar_examen.html', context)
    else:
        context = {
            'examen': examen,
            'total_preguntas': len(preguntas_respuestas),
            'preguntas_respuestas': preguntas_respuestas
        }
        return render(request, 'examen/realizar_examen.html', context)


def calificacion_examen(request, examen_id):
    calificaciones = CalificacionExamen.objects.filter(examen = examen_id)
    paginator = Paginator(calificaciones, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'examen/calificacion.html', {"pagination": page_obj})


def eliminar_pregunta(request, pregunta_id):
    pregunta = Pregunta.objects.get(id=pregunta_id)
    examen = pregunta.examen.id
    try:
        respuestas = Respuesta.objects.filter(pregunta=pregunta)
        respuestas.delete()
        pregunta.delete()
        messages.success(request,'Se ha eliminado las preguntas con éxito')
    except:
        messages.errors(request,'Hubo un error al eliminar la pregunta')
    url = reverse('examen:detalles_examen', args=[examen])
    return redirect(url)


def editar_pregunta(request, pregunta_id):
    pregunta = Pregunta.objects.get(id=pregunta_id)
    if request.method == 'POST':
        pregunta.texto = request.POST.get('pregunta')
        with transaction.atomic():
            try:
                pregunta.save()
                for i in range(1, 5):
                    id_respuesta = request.POST.get(f'id_respuesta{i}')
                    respuesta = Respuesta.objects.get(id=id_respuesta)
                    respuesta.texto = request.POST.get(f'respuesta{i}')
                    respuesta.es_correcta =  True if request.POST.get(f'respuesta{i}-es_correcta') else False
                    respuesta.save()
                messages.success(request, 'La pregunta se ha almacenado correctamente.')        
            except Exception as e:
                messages.error(request, f'Hubo un error al editar la pregunta: {e}')
                url = reverse('examen:editar_pregunta', args=[pregunta.id])
                return redirect(url)
    else:
        respuestas = Respuesta.objects.filter(pregunta=pregunta)
        contexto = {
            'pregunta': pregunta,
            'respuestas': respuestas
        }
        return render(request, 'examen/editar_pregunta.html', contexto)
    
    url = reverse('examen:detalles_examen', args=[pregunta.examen.id])
    return redirect(url)


def eliminar_examen(request, examen_id):
    examen = get_object_or_404(Examen, pk=examen_id)
    id = examen.curso.id
    try:
        examen.delete()
        messages.success(request,'Se ha eliminado el examen con éxito')
    except:
        messages.errors(request,'Hubo un error al eliminar el examen')
    url = reverse('curso:ver_curso', args=[id])
    return redirect(url)



def obtener_calificaciones(request):
    calificacion = CalificacionExamen.objects.filter(estudiante=request.user)
    paginator = Paginator(calificacion, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'examen/calificacion_estudiante.html', {"pagination": page_obj})

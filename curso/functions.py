from clase.models import Clase, VistaClase
from .models import *
from django.core.paginator import Paginator
from .forms import *
from .models import Curso
import matplotlib.pyplot as plt
from io import BytesIO
import base64

    
def agregar_salto_linea(cadena, longitud_maxima=20):
    palabras = cadena.split()  # Divide la cadena en palabras
    resultado = []
    linea_actual = ""

    for palabra in palabras:
        if len(linea_actual) + len(palabra) <= longitud_maxima:
            # Agrega la palabra a la línea actual si no excede la longitud máxima
            if linea_actual:
                linea_actual += " "  # Agrega un espacio si no es la primera palabra
            linea_actual += palabra
        else:
            # Si agregar la palabra excede la longitud máxima, inicia una nueva línea
            resultado.append(linea_actual)
            linea_actual = palabra

    if linea_actual:
        resultado.append(linea_actual)  # Agrega la última línea

    return "\n".join(resultado)  # Combina las líneas con saltos de línea

def enviar_solicitud_curso(curso):
    curso = SolicitudCurso(curso=curso)
    curso.save()


def get_pagination_context(queryset, request, cursos=None):
    paginator = Paginator(queryset, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    cantidad = cursos.count() if cursos else 0
    contexto = {
        'form': CursoForm(),
        'pagination': page_obj,
        'cantidad': cantidad
    }
    return contexto


def generar_grafica_cursos(cursos, titulo):
    nombres_cursos = []
    for curso in cursos:
        nombres_cursos.append( agregar_salto_linea(curso.nombre) )
    
    inscritos = [curso.num_inscripciones for curso in cursos]

    if inscritos:  # Verificar si la lista de inscritos no está vacía
        min_inscritos = min(inscritos)
        max_inscritos = max(inscritos)
    else:
        min_inscritos = 0
        max_inscritos = 0

    plt.figure(figsize=(10, 6))
    bars = plt.bar(nombres_cursos, inscritos)
    plt.xlabel('Cursos')
    plt.ylabel('Alumnos Inscritos')
    plt.title(titulo)
    plt.xticks(fontsize=10)
    plt.yticks(range(min_inscritos, max_inscritos + 1, 10))

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 1), ha='center', va='bottom', color='black', fontweight='bold')

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close()

    grafica_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return grafica_base64

def obtener_cursos_populares_y_menos_populares(user):
    cursos = Curso.objects.filter(solicitudcurso__isnull=True).annotate(num_inscripciones=models.Count('inscripcion')).order_by('-num_inscripciones')
    if user.user_type == "instructor":
        cursos = cursos.filter(instructor=user)
    
    return cursos[:5], cursos.reverse()[:5]


def obtener_avance_estudiantes(user):
    if user.user_type == 'instructor':
        cursos = Curso.objects.filter(instructor=user)
        inscripciones = Inscripcion.objects.filter(curso__in=cursos)
        return inscripciones
    else:
        return Inscripcion.objects.all()
    
    
def avance_estudiante_en_curso(curso, clases, estudiante):
    clases_vistas = VistaClase.objects.filter(curso=curso.id, estudiante=estudiante).count()
    
    num_clases= clases.count()
    
    datos = {}
    datos['estudiante'] = estudiante
    datos['visto'] = clases_vistas
    datos['total'] = num_clases
    
    if num_clases > 0:
        datos['porcentaje'] = round((clases_vistas * 100) / num_clases)
    else:
        datos['porcentaje'] = 0
    
    return datos
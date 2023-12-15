from .models import Curso

def cursos(request):
    if request.user.is_authenticated:
        cursos = Curso.objects.filter(instructor=request.user, solicitudcurso__isnull=True)[:20]
    else: 
        cursos = {}
    return {'cursos_instructor': cursos}

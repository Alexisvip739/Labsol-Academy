from django.urls import path
from curso import views

app_name = 'curso'
handler404 = 'curso.views.pagina_no_encontrada'
urlpatterns = [
    path('inicio/', views.lista_cursos_estudiante, name='lista_cursos_estudiante'),
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos_instructor/', views.get_curso_instructor, name='lista_cursos_instructor'),
    path('crear_curso/', views.crear_curso, name='crear_curso'),
    path('editar_curso/<int:curso_id>/', views.editar_curso, name='editar_curso'),
    path('ver_curso/<int:curso_id>/', views.get_curso, name='ver_curso'),
    path('agregar_etiqueta/', views.agregar_etiqueta, name='agregar_etiqueta'),
    path('solicitud/', views.get_solicitud_curso, name='lista_solicitud_curso'),
    path('solicitud/<int:solicitud_id>/<str:argumento>/', views.procesar_solicitud_curso, name='procesar_solicitud_curso'),
    path('inscripcion/<int:curso_id>/', views.inscribir_curso, name='inscripcion'),
    path('grafica/', views.grafica_cursos, name='grafica_cursos'),
    path('avance_estudiantes/',views.tabla_con_cursos ,name='tabla_con_cursos'),
    path('avance_estudiantes/<str:curso>/',views.mostrar_avance_estudiante,name='mostrar_avance_estudiante'),
    path('mostrar_avance/',views.mostrar_porcentaje,name='mostrar_avance'),
    path('cursos_inscritos',views.cursos_inscritos,name='cursos_inscritos'),
    path('todos_los_cursos/',views.cursos_disponibles_para_estudiante,name='todos_los_cursos'),
    path('inscrito_curso/<int:curso_id>/', views.alumnos_inscritos_curso, name='inscrito_curso'),
    path('eliminar_suscripcion/<int:curso_id>/',views.desinscribir_estudiantes,name='eliminar_suscripcion'),
    path('enviar_notificacion/curso/<int:curso_id>/',views.enviar_notificacion,name='enviar_notificacion'),
    path('ver_notificaciones/<int:curso_id>',views.ver_notificaciones,name='ver_notificaciones'),
] 
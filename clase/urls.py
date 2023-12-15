from django.urls import path
from clase import views

app_name = 'clase'
urlpatterns = [
    path('crear_clase/', views.crear_clase, name='crear_clase'),
    path('detalle_clase/<int:clase_id>/', views.get_clase, name='ver_clase'),
    path('eliminar/<int:clase_id>/', views.eliminar_clase, name='eliminar'),
    path('editar_clase/', views.editar_clase, name='editar_clase'),
    path('clases_estudiante/<int:curso_id>/', views.get_clase_estudiante, name='clases_estudiante'),
    path('agregar_comentario/', views.agregar_comentario, name='agregar_comentario'),
]

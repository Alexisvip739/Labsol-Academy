from usuario import views
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'usuario'
handler404 = 'usuario.views.pagina_no_encontrada'
urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('estudiantes/', views.get_estudiantes, name='lista_estudiantes'),
    path('instructores/', views.get_instructores, name='lista_instructores'),
    path('administradores/', views.get_administradores, name='lista_administradores'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('solicitud/', views.get_solicitud, name='lista_solicitud'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('solicitud/<int:solicitud_id>/<str:argumento>/', views.procesar_solicitud, name='procesar_solicitud'),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('politicas_privacidad/', views.politicas_privacidad, name='politicas_y_privacidad'),
]

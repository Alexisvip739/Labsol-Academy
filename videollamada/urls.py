from videollamada import views
from django.urls import path

app_name = 'videollamada'
handler404 = 'videollamada.views.pagina_no_encontrada'

urlpatterns = [
	path('videollamada/', views.videollamadas, name='videollamada'),
	path('crear/', views.crear_videollamada, name='crear_videollamada'),
	path('subir_video/', views.subir_video, name='subir_video'),
	path('detalle_video/<int:videollamada_id>/', views.ver_videollamada, name='detalle_video'),
	path('editar_video/', views.editar_video, name='editar_video'),
	path('lista_conferencias/', views.get_videollamadas, name='lista_videollamada'),
]
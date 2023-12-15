from django.urls import path,include
from rest_framework import routers
from api_clase_curso import views

app_name = 'clase_curso_api'
urlpatterns = [
  path('clase_api/',views.Clase_APIView.as_view(),name='clase_api'),
  path('solicitudCursos_api/',views.SolicituCursoVista_APIView.as_view(),name='solicitudCursos_api'),
  path('clase_api/<str:pk>',views.Clase_APIView_Detail.as_view(),name='clase_api_detail'),
  path("curso_api/", views.Curso_APIView.as_view(), name="curso_api"),
  path("inscripcion/", views.Inscripcion_APIView.as_view(),name="inscription_api"),
  path("inscripcion/<str:pk>/", views.Inscripcion_APIView_Detail.as_view(),name="inscripcion_api_detail"),
  path("clases_vistas/",views.ClaseVista_APIView.as_view(),name="clase_vista_api"),
  path("clase_vista/<str:pk>",views.ClaseVista_APIView_Detail.as_view(),name="clase_vista_detail"),
  path('usuarios/',views.UsuarioPersonalizado_APIView_Detail.as_view(), name="usuarios"),
  path('solicitudUsuarios/',views.SolicitudUsuario_APIView.as_view(), name="solicitud_usuario")
]

from examen import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'examen'
handler404 = 'examen.views.pagina_no_encontrada'
urlpatterns = [
    path('detalles_examen/<int:examen_id>',views.get_examen,name='detalles_examen'),
    path('realizar_examen/<int:examen_id>',views.examen,name='realizar_examen'),
    path('calificacion_examen/<int:examen_id>', views.calificacion_examen, name='calificacion_examen'),
    path('crear_examen/',views.crear_examen,name='crear_examen'),
    path('agregar_pregunta/',views.crear_pregunta,name='crear_pregunta'),
    path('eliminar_pregunta/<int:pregunta_id>',views.eliminar_pregunta,name='eliminar_pregunta'),
    path('editar_pregunta/<int:pregunta_id>',views.editar_pregunta,name='editar_pregunta'),
    path('eliminar_examen/<int:examen_id>',views.eliminar_examen,name='eliminar_examen'),
    path('calificacion_estudiante/',views.obtener_calificaciones, name='calificacion_estudiante'),

]

from django.urls import path
from notificacion import views

app_name = 'notificacion'

urlpatterns = [
    path('notificacion/', views.lista_notificacion, name='notificacion'),
    path('enviar_notificacion/', views.enviar_notificacion, name='enviar_notificacion'),
    path('detalle/<int:notificacion_id>/', views.detalle_notificacion, name='detalle_notificacion')
]
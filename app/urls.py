from django.contrib import admin
from django.urls import path
from usuario import views as users
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from curso import views as curso
from clase import views as clase
from examen import views as examen
from usuario import views as usuario
from videollamada import views as videollamada
from notificacion import views as notificacion
from usuario.views import CustomPasswordResetView
from django.contrib.auth.views import (
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

handler404 = 'clase.views.pagina_no_encontrada'
handler404 = 'curso.views.pagina_no_encontrada'
handler404 = 'examen.views.pagina_no_encontrada'
handler404 = 'usuario.views.pagina_no_encontrada'
handler404= 'videollamada.views.pagina_no_encontrada'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users.UserLoginView.as_view(), name='iniciar_sesion'),
    path('usuario/',include('usuario.urls'),name='usuario'),
    path('curso/',include('curso.urls'),name='curso'),
    path('clase/',include('clase.urls'),name='clase'),
    path('notificacion/',include('notificacion.urls'),name='notificacion'),
    path('examen/',include('examen.urls'),name='examen'),
    path('videollamada/',include('videollamada.urls'),name='videollamada'),
    path('buscar/', curso.buscar_curso, name='buscar'),
    path('api/',include('api_clase_curso.urls'),name='api_clase_curso'),

    #URLs para restablecer la contraseña
	path('password-reset/', CustomPasswordResetView.as_view(
        template_name='usuario/passwordReset/password_reset.html'),
        name='password_reset'),
        
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='usuario/passwordReset/reset_password_done.html'),
        name='password_reset_done'),
        
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='usuario/passwordReset/password_reset_confirm.html'),
        name='password_reset_confirm'),
        
    path('password-reset-complete/',PasswordResetCompleteView.as_view(
        template_name='usuario/passwordReset/password_reset_complete.html'),
        name='password_reset_complete'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


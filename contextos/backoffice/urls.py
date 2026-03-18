from django.urls import path, include
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.listado, name='listado_usuarios'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/api/buscar/', views.buscar_usuarios_api, name='buscar_usuarios_api'),
]
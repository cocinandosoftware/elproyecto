from django.urls import path, include
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.listado, name='listado_usuarios'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/api/buscar/', views.buscar_usuarios_api, name='buscar_usuarios_api'),
    path('usuarios/api/obtener/<int:usuario_id>/', views.obtener_usuario_api, name='obtener_usuario_api'),
    path('usuarios/api/crear/', views.crear_usuario_api, name='crear_usuario_api'),
    path('usuarios/api/editar/<int:usuario_id>/', views.editar_usuario_api, name='editar_usuario_api'),
]
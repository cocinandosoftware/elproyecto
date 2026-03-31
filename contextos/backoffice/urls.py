from django.urls import path, include
from . import dashboard_views
from . import usuarios_views
from . import usuarios_api_views

app_name = 'backoffice'

urlpatterns = [
    # Dashboard
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    
    # Usuarios - Vistas de templates
    path('usuarios/', usuarios_views.listado, name='listado_usuarios'),
    
    # Usuarios - APIs
    path('usuarios/api/buscar/', usuarios_api_views.buscar_usuarios_api, name='buscar_usuarios_api'),
    path('usuarios/api/obtener/<int:usuario_id>/', usuarios_api_views.obtener_usuario_api, name='obtener_usuario_api'),
    path('usuarios/api/crear/', usuarios_api_views.crear_usuario_api, name='crear_usuario_api'),
    path('usuarios/api/editar/<int:usuario_id>/', usuarios_api_views.editar_usuario_api, name='editar_usuario_api'),
    path('usuarios/eliminar/<int:usuario_id>/', usuarios_api_views.eliminar_usuario, name='eliminar_usuario'),
]
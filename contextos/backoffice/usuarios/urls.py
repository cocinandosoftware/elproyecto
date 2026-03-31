from django.urls import path
from .views import listado
from .editar_usuario_view import editar_usuario
from .buscar_usuarios_api import buscar_usuarios_api
from .obtener_usuario_api import obtener_usuario_api
from .crear_usuario_api import crear_usuario_api
from .editar_usuario_api import editar_usuario_api
from .eliminar_usuario_api import eliminar_usuario

app_name = 'usuarios'

urlpatterns = [
    # Vistas de templates
    path('', listado, name='listado'),
    path('<int:usuario_id>/editar/', editar_usuario, name='editar'),
    
    # APIs para operaciones CRUD
    path('api/buscar/', buscar_usuarios_api, name='buscar_api'),
    path('api/obtener/<int:usuario_id>/', obtener_usuario_api, name='obtener_api'),
    path('api/crear/', crear_usuario_api, name='crear_api'),
    path('api/editar/<int:usuario_id>/', editar_usuario_api, name='editar_api'),
    path('eliminar/<int:usuario_id>/', eliminar_usuario, name='eliminar'),
]

"""
Módulo de gestión de usuarios del Backoffice

Este módulo contiene todas las vistas y APIs para la gestión de usuarios
desde el área de administración.
"""

from .views import listado
from .editar_usuario_view import editar_usuario
from .buscar_usuarios_api import buscar_usuarios_api
from .obtener_usuario_api import obtener_usuario_api
from .crear_usuario_api import crear_usuario_api
from .editar_usuario_api import editar_usuario_api
from .eliminar_usuario_api import eliminar_usuario

__all__ = [
    'listado',
    'editar_usuario',
    'buscar_usuarios_api',
    'obtener_usuario_api',
    'crear_usuario_api',
    'editar_usuario_api',
    'eliminar_usuario',
]

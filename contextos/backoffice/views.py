"""
Módulo de vistas del Backoffice - Archivo de índice

Este archivo importa todas las vistas de los submódulos especializados
para mantener compatibilidad con imports antiguos.

Estructura:
- dashboard_views.py: Vista del dashboard de administradores
- usuarios_views.py: Vistas de templates para gestión de usuarios
- usuarios_api_views.py: APIs para operaciones CRUD de usuarios
"""

# Dashboard
from .dashboard_views import dashboard

# Usuarios - Vistas de templates
from .usuarios_views import listado

# Usuarios - APIs
from .usuarios_api_views import (
    buscar_usuarios_api,
    obtener_usuario_api,
    crear_usuario_api,
    editar_usuario_api,
    eliminar_usuario
)

# Hacer disponibles para importación desde este módulo
__all__ = [
    'dashboard',
    'listado',
    'buscar_usuarios_api',
    'obtener_usuario_api',
    'crear_usuario_api',
    'editar_usuario_api',
    'eliminar_usuario',
]

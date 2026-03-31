from django.urls import path, include
from . import dashboard_views

app_name = 'backoffice'

urlpatterns = [
    # Dashboard
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    
    # Módulo de Usuarios (incluye vistas y APIs)
    path('usuarios/', include('contextos.backoffice.usuarios.urls')),
]
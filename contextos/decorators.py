"""
Decoradores personalizados para control de acceso
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


def cliente_required(view_func):
    """
    Decorador que requiere que el usuario esté logueado y sea un cliente.
    Si no está logueado, redirige al login.
    Si no es cliente, lo desloguea y redirige al login.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        # Verificar si está logueado
        if not request.user.is_authenticated:
            return redirect('auth:login')
        
        # Verificar si es cliente
        if not request.user.es_cliente():
            messages.error(request, 'No tienes permisos para acceder a esta área.')
            logout(request)
            return redirect('auth:login')
            
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def desarrollador_required(view_func):
    """
    Decorador que requiere que el usuario esté logueado y sea un desarrollador.
    Si no está logueado, redirige al login.
    Si no es desarrollador, lo desloguea y redirige al login.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si está logueado
        if not request.user.is_authenticated:
            return redirect('auth:login')
            
        # Verificar si es desarrollador
        if not request.user.es_desarrollador():
            messages.error(request, 'No tienes permisos para acceder a esta área.')
            logout(request)
            return redirect('auth:login')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    """
    Decorador que requiere que el usuario esté logueado y sea administrador.
    Si no está logueado, redirige al login.
    Si no es admin, redirige al dashboard correspondiente.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si está logueado
        if not request.user.is_authenticated:
            return redirect('auth:login')
            
        # Verificar si es admin
        if not request.user.es_admin():
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('auth:dashboard')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view



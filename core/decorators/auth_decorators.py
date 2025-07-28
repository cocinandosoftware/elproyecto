from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """
    Decorador que valida que el usuario tenga uno de los roles permitidos
    
    Args:
        allowed_roles (list): Lista de roles permitidos
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'No tienes permisos para acceder a esta área.')
                return redirect('web:index')
        return wrapper
    return decorator


def cliente_required(view_func):
    """
    Decorador que requiere que el usuario sea un cliente
    """
    return role_required(['cliente'])(view_func)


def desarrollador_required(view_func):
    """
    Decorador que requiere que el usuario sea un desarrollador
    """
    return role_required(['desarrollador'])(view_func)


def admin_required(view_func):
    """
    Decorador que requiere que el usuario sea un administrador
    """
    return role_required(['admin'])(view_func)


def cliente_or_admin_required(view_func):
    """
    Decorador que permite acceso a clientes y administradores
    """
    return role_required(['cliente', 'admin'])(view_func)


def desarrollador_or_admin_required(view_func):
    """
    Decorador que permite acceso a desarrolladores y administradores
    """
    return role_required(['desarrollador', 'admin'])(view_func)

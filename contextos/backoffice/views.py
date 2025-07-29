from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.usuarios.UsuarioModel import Usuario


@login_required
def dashboard(request):
    """
    Dashboard específico para administradores
    """
    if not request.user.es_admin():
        messages.error(request, 'No tienes permisos para acceder a esta área.')
        return redirect('auth:dashboard')
    
    # Estadísticas para el backoffice
    total_usuarios = Usuario.objects.count()
    usuarios_activos = Usuario.objects.filter(activo=True).count()
    clientes_usuarios = Usuario.objects.filter(tipo_usuario='cliente').count()
    desarrolladores_usuarios = Usuario.objects.filter(tipo_usuario='desarrollador').count()
    
    context = {
        'usuario': request.user,
        'stats': {
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'clientes': clientes_usuarios,
            'desarrolladores': desarrolladores_usuarios,
        }
    }
    
    return render(request, 'dashboard/backoffice.html', context)


@login_required
def listado(request):
    """
    Vista del listado de backoffice - solo para administradores
    """
    # Verificar que el usuario es administrador
    if not request.user.es_admin():
        messages.error(request, 'No tienes permisos para acceder al backoffice.')
        return redirect('auth:dashboard')
    
    return render(request, 'backoffice/listado.html')
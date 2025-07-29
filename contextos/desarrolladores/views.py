from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def dashboard(request):
    """
    Dashboard específico para desarrolladores
    """
    if not request.user.es_desarrollador():
        messages.error(request, 'No tienes permisos para acceder a esta área.')
        return redirect('auth:dashboard')
    
    context = {
        'usuario': request.user,
    }
    
    return render(request, 'dashboard/desarrollador.html', context)


@login_required
def listado(request):
    """
    Vista del listado de desarrolladores - solo para usuarios autenticados
    """
    # Verificar que el usuario tiene permisos (admin o desarrollador)
    if not (request.user.es_admin() or request.user.es_desarrollador()):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('auth:dashboard')
    
    return render(request, 'desarrolladores/listado.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    """
    Vista para el login de usuarios
    """
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.activo:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.first_name or user.username}!')
            return redirect('authentication:dashboard')
        else:
            messages.error(request, 'Credenciales inválidas o usuario inactivo.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """
    Vista para el logout de usuarios
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('web:index')


@login_required
def dashboard_view(request):
    """
    Vista del dashboard que redirige según el rol del usuario
    """
    user = request.user
    
    if user.is_cliente():
        return redirect('clientes:listado')
    elif user.is_desarrollador():
        return redirect('desarrolladores:listado')
    elif user.is_admin_role() or user.is_superuser:
        return redirect('backoffice:dashboard')
    else:
        messages.error(request, 'Tu cuenta no tiene un rol válido asignado.')
        return redirect('web:index')

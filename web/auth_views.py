from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from core.usuarios.UsuarioModel import Usuario


def login_view(request):
    """
    Vista para el login de usuarios
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Intentar autenticar al usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.activo:
                login(request, user)
                # Actualizar último acceso
                user.actualizar_ultimo_acceso()
                
                messages.success(request, f'¡Bienvenido {user.nombre_completo}!')
                
                # Redirigir al dashboard principal (distribuidor)
                return redirect('auth:dashboard')
            else:
                messages.error(request, 'Tu cuenta está desactivada. Contacta con el administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """
    Vista para el logout de usuarios
    """
    if request.user.is_authenticated:
        messages.success(request, f'¡Hasta luego {request.user.nombre_completo}!')
        logout(request)
    
    return redirect('index')


@login_required
def dashboard_view(request):
    """
    Vista del dashboard principal - redirige según el tipo de usuario a su contexto privado
    """
    user = request.user
    
    if user.es_admin():
        return redirect('backoffice:dashboard')
    elif user.es_cliente():
        return redirect('clientes:dashboard')
    elif user.es_desarrollador():
        return redirect('desarrolladores:dashboard')
    else:
        messages.error(request, 'Tipo de usuario no reconocido.')
        return redirect('index')

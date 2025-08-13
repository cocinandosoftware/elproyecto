from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from core.clientes.ClienteModel import Cliente
from core.desarrolladores.DesarrolladorModel import Desarrollador
from core.usuarios.UsuarioModel import Usuario


def login_view(request):
    """
    Vista para el login de usuarios
    """
    if request.user.is_authenticated:
        return redirect('auth:dashboard')
    
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

def register_view(request):
    """
    Vista para el registro de nuevos usuarios (clientes y desarrolladores)
    """
    if request.user.is_authenticated:
        return redirect('auth:login')
    
    if request.method == 'POST':

        print("Datos del formulario:", request.POST)  # Debugging line to check form data
        
        # Obtener datos del formulario
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        username = request.POST.get('username', '').strip().lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        tipo_usuario = request.POST.get('tipo_usuario')
        telefono = request.POST.get('telefono', '').strip()
        
        # Validaciones
        errors = []
        
        if not first_name:
            errors.append('El nombre es obligatorio.')
        elif len(first_name) < 2:
            errors.append('El nombre debe tener al menos 2 caracteres.')
        
        if not last_name:
            errors.append('Los apellidos son obligatorios.')
        elif len(last_name) < 2:
            errors.append('Los apellidos deben tener al menos 2 caracteres.')
        
        if not email:
            errors.append('El email es obligatorio.')
        elif Usuario.objects.filter(email=email).exists():
            errors.append('Ya existe un usuario con este email.')
        elif '@' not in email or '.' not in email:
            errors.append('El formato del email no es válido.')
        
        if not username:
            errors.append('El nombre de usuario es obligatorio.')
        elif len(username) < 3:
            errors.append('El nombre de usuario debe tener al menos 3 caracteres.')
        elif Usuario.objects.filter(username=username).exists():
            errors.append('Ya existe un usuario con este nombre de usuario.')
        elif not username.replace('_', '').replace('-', '').isalnum():
            errors.append('El nombre de usuario solo puede contener letras, números, guiones y guiones bajos.')
        
        if not password1:
            errors.append('La contraseña es obligatoria.')
        elif len(password1) < 8:
            errors.append('La contraseña debe tener al menos 8 caracteres.')
        elif password1.isdigit():
            errors.append('La contraseña no puede ser solo números.')
        elif password1.lower() in [username.lower(), email.lower(), first_name.lower(), last_name.lower()]:
            errors.append('La contraseña no puede ser similar a tu información personal.')
        
        if password1 != password2:
            errors.append('Las contraseñas no coinciden.')
        
        if tipo_usuario not in ['cliente', 'desarrollador']:
            errors.append('Debe seleccionar un tipo de usuario válido.')
        
        # Validar teléfono si se proporciona
        if telefono:
            # Limpiar el teléfono de espacios y caracteres especiales
            telefono_clean = ''.join(filter(str.isdigit, telefono.replace('+', '')))
            if len(telefono_clean) < 9:
                errors.append('El número de teléfono debe tener al menos 9 dígitos.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'auth/register.html', {
                'form_data': request.POST
            })
        
        try:
            with transaction.atomic():


                if tipo_usuario == 'cliente':
                    cliente = Cliente()
                    cliente.nombre = first_name
                    cliente.razon_social = last_name
                    # cliente.nif = ""
                    cliente.contacto_nombre = first_name
                    cliente.contacto_email = email
                    cliente.contacto_telefono = telefono if telefono else None
                    cliente.save()

                elif tipo_usuario == 'desarrollador':
                    desarrollador = Desarrollador()
                    desarrollador.nombre = first_name
                    # desarrollador.perfil = 'desarrollador'
                    desarrollador.save()

                                # Crear el usuario
                user = Usuario()
                user.username = username
                user.email = email
                user.set_password(password1)
                user.first_name = first_name
                user.last_name = last_name
                user.tipo_usuario = tipo_usuario
                
                if tipo_usuario == 'cliente':
                    user.cliente_asociado = cliente
                elif tipo_usuario == 'desarrollador':
                    user.desarrollador_asociado = desarrollador

                user.telefono = telefono if telefono else None
                user.save()

                messages.success(request, f'¡Registro exitoso! Bienvenido {user.nombre_completo}.')
                
                return redirect('auth:login')
                
        except Exception as e:
            messages.error(request, f'Error al crear el usuario: {str(e)}')
    
    return render(request, 'auth/register.html')


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

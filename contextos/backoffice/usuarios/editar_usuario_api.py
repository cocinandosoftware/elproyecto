from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from core.usuarios.UsuarioModel import Usuario
from contextos.decorators import admin_required


@admin_required
def editar_usuario_api(request, usuario_id):
    """
    API para editar un usuario existente con validación manual.
    Si el password está vacío, se mantiene el actual.
    """
    try:
        if request.method != 'POST':
            return JsonResponse({
                'success': False,
                'error': 'Método no permitido',
                'message': 'Use POST para editar usuarios'
            }, status=405)
        
        # Obtener usuario existente
        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        # Obtener datos del request
        import json
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Datos inválidos',
                'message': 'El formato de los datos no es válido'
            }, status=400)
        
        # Extraer campos
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        tipo_usuario = data.get('tipo_usuario', '').strip()
        telefono = data.get('telefono', '').strip()
        activo = data.get('activo', True)
        
        # Validaciones manuales
        errors = {}
        
        # Validar username (si cambió)
        if not username:
            errors['username'] = ['El nombre de usuario es obligatorio']
        elif len(username) < 3:
            errors['username'] = ['El nombre de usuario debe tener al menos 3 caracteres']
        elif username != usuario.username and Usuario.objects.filter(username=username).exists():
            errors['username'] = ['Este nombre de usuario ya está en uso']
        
        # Validar email (si cambió)
        if not email:
            errors['email'] = ['El email es obligatorio']
        elif '@' not in email or '.' not in email:
            errors['email'] = ['El email no tiene un formato válido']
        elif email != usuario.email and Usuario.objects.filter(email=email).exists():
            errors['email'] = ['Este email ya está registrado']
        
        # Validar password (solo si se proporciona uno nuevo)
        if password and len(password) < 8:
            errors['password'] = ['La contraseña debe tener al menos 8 caracteres']
        
        # Validar tipo_usuario
        tipos_validos = ['admin', 'cliente', 'desarrollador']
        if not tipo_usuario:
            errors['tipo_usuario'] = ['El tipo de usuario es obligatorio']
        elif tipo_usuario not in tipos_validos:
            errors['tipo_usuario'] = ['El tipo de usuario no es válido']
        
        # Validar teléfono (opcional)
        if telefono and len(telefono) > 15:
            errors['telefono'] = ['El teléfono no puede tener más de 15 caracteres']
        
        # Si hay errores, devolverlos
        if errors:
            return JsonResponse({
                'success': False,
                'message': 'Errores de validación',
                'errors': errors
            }, status=400)
        
        # Actualizar campos del usuario
        usuario.username = username
        usuario.email = email
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.tipo_usuario = tipo_usuario
        usuario.telefono = telefono if telefono else None
        usuario.activo = activo
        
        # Actualizar contraseña solo si se proporcionó una nueva
        if password:
            usuario.set_password(password)
        
        usuario.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario "{usuario.nombre_completo}" actualizado correctamente',
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email
            }
        })
    
    except ValueError:
        return JsonResponse({
            'success': False,
            'error': 'Usuario no encontrado',
            'message': 'El usuario que intenta editar no existe'
        }, status=404)
    
    except Exception as e:
        print(f"Error al editar usuario {usuario_id}: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor',
            'message': f'Error al editar el usuario: {str(e)}'
        }, status=500)

from django.http import JsonResponse
from core.usuarios.UsuarioModel import Usuario
from contextos.decorators import admin_required


@admin_required
def crear_usuario_api(request):
    """
    API para crear un nuevo usuario con validación manual.
    Recibe datos en formato JSON desde el formulario del modal.
    """
    try:
        if request.method != 'POST':
            return JsonResponse({
                'success': False,
                'error': 'Método no permitido',
                'message': 'Use POST para crear usuarios'
            }, status=405)
        
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
        
        # Validar username
        if not username:
            errors['username'] = ['El nombre de usuario es obligatorio']
        elif len(username) < 3:
            errors['username'] = ['El nombre de usuario debe tener al menos 3 caracteres']
        elif Usuario.objects.filter(username=username).exists():
            errors['username'] = ['Este nombre de usuario ya está en uso']
        
        # Validar email
        if not email:
            errors['email'] = ['El email es obligatorio']
        elif '@' not in email or '.' not in email:
            errors['email'] = ['El email no tiene un formato válido']
        elif Usuario.objects.filter(email=email).exists():
            errors['email'] = ['Este email ya está registrado']
        
        # Validar password
        if not password:
            errors['password'] = ['La contraseña es obligatoria']
        elif len(password) < 8:
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
        
        # Crear el usuario
        usuario = Usuario.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            tipo_usuario=tipo_usuario,
            telefono=telefono if telefono else None,
            activo=activo
        )
        
        # Establecer contraseña hasheada
        usuario.set_password(password)
        usuario.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario "{usuario.nombre_completo}" creado correctamente',
            'redirect_url': f'/backoffice/usuarios/{usuario.id}/editar/',
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email
            }
        })
    
    except Exception as e:
        print(f"Error al crear usuario: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor',
            'message': f'Error al crear el usuario: {str(e)}'
        }, status=500)

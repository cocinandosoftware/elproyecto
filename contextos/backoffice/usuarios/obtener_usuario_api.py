from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from core.usuarios.UsuarioModel import Usuario
from contextos.decorators import admin_required


@admin_required
def obtener_usuario_api(request, usuario_id):
    """
    API para obtener los datos de un usuario específico.
    Usado para pre-rellenar el formulario de edición.
    """
    try:
        if request.method != 'GET':
            return JsonResponse({
                'success': False,
                'error': 'Método no permitido',
                'message': 'Use GET para obtener datos de usuario'
            }, status=405)
        
        # Obtener usuario o devolver 404
        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        # Preparar datos del usuario
        usuario_data = {
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'tipo_usuario': usuario.tipo_usuario,
            'telefono': usuario.telefono or '',
            'activo': usuario.activo,
        }
        
        return JsonResponse({
            'success': True,
            'usuario': usuario_data
        })
    
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'error': 'Usuario no encontrado',
            'message': str(e)
        }, status=404)
    
    except Exception as e:
        print(f"Error al obtener usuario {usuario_id}: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor',
            'message': f'Error al obtener datos del usuario: {str(e)}'
        }, status=500)

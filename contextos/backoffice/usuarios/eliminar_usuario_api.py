from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from core.usuarios.UsuarioModel import Usuario
from contextos.decorators import admin_required


@admin_required
def eliminar_usuario(request, usuario_id):
    """
    API para eliminar un usuario del sistema de forma asíncrona.
    Solo accesible para administradores.
    Devuelve JSON con el resultado de la operación.
    """
    try:
        # Solo procesar si es una petición POST o DELETE
        if request.method not in ['POST', 'DELETE']:
            return JsonResponse({
                'success': False,
                'error': 'Método no permitido',
                'message': 'Use POST o DELETE para eliminar usuarios'
            }, status=405)
        
        # Obtener el usuario a eliminar o devolver 404
        usuario_a_eliminar = get_object_or_404(Usuario, id=usuario_id)
        
        # Verificar que no se esté intentando eliminar a sí mismo
        if usuario_a_eliminar.id == request.user.id:
            return JsonResponse({
                'success': False,
                'error': 'Auto-eliminación no permitida',
                'message': 'No puedes eliminar tu propio usuario'
            }, status=403)
        
        # Guardar datos antes de eliminar
        nombre_usuario = usuario_a_eliminar.nombre_completo
        tipo_usuario = usuario_a_eliminar.tipo_usuario
        
        # Eliminar el usuario
        usuario_a_eliminar.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario "{nombre_usuario}" eliminado correctamente',
            'usuario_eliminado': {
                'id': usuario_id,
                'nombre': nombre_usuario,
                'tipo': tipo_usuario
            }
        })
    
    except Usuario.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Usuario no encontrado',
            'message': 'El usuario que intenta eliminar no existe'
        }, status=404)
    
    except Exception as e:
        print(f"Error al eliminar usuario {usuario_id}: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor',
            'message': f'Error al eliminar el usuario: {str(e)}'
        }, status=500)

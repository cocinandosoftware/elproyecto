from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, time
from core.usuarios.UsuarioModel import Usuario
from contextos.decorators import admin_required


@admin_required
def dashboard(request):
    """
    Dashboard específico para administradores
    """
    # Estadísticas para el backoffice
    total_usuarios = Usuario.objects.count()
    usuarios_activos = Usuario.objects.filter(activo=True).count()
    clientes_usuarios = Usuario.objects.filter(tipo_usuario='cliente').count()
    desarrolladores_usuarios = Usuario.objects.filter(tipo_usuario='desarrollador').count()
    
    context = {
        'contexto_nombre': 'Backoffice',
        'contexto_css': 'main_backoffice',
        'usuario': request.user,
        'stats': {
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'clientes': clientes_usuarios,
            'desarrolladores': desarrolladores_usuarios,
        }
    }
    
    return render(request, 'gestion/backoffice/dashboard.html', context)


@admin_required
def listado(request):
    """
    Vista del listado de usuarios en backoffice - solo para administradores.
    La carga inicial y el filtrado se manejan completamente mediante JavaScript asíncrono.
    """
    datos = {
        'contexto_nombre': 'Backoffice',
        'contexto_css': 'main_backoffice',
        'usuario': request.user,
    }
    
    return render(request, 'gestion/backoffice/usuarios.html', datos)


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


@admin_required
def buscar_usuarios_api(request):
    """
    API para búsqueda asíncrona de usuarios.
    Devuelve resultados en formato JSON para actualizar la tabla sin recargar la página.
    Incluye manejo completo de excepciones.
    """
    try:
        # Simular carga para visualizar el loader (eliminar en producción)
        import time as t
        t.sleep(1)
        
        # Obtener todos los usuarios como base
        usuarios = Usuario.objects.all()
        
        # Aplicar filtros desde request.GET
        busqueda = request.GET.get('filter_busqueda', '').strip()
        tipo_usuario = request.GET.get('filter_tipo_usuario', '').strip()
        fecha_desde = request.GET.get('filter_fecha_desde', '').strip()
        fecha_hasta = request.GET.get('filter_fecha_hasta', '').strip()
        
        # Aplicar filtro de búsqueda general
        if busqueda:
            usuarios = usuarios.filter(
                Q(first_name__icontains=busqueda) |
                Q(last_name__icontains=busqueda) |
                Q(email__icontains=busqueda) |
                Q(telefono__contains=busqueda) |
                Q(username__icontains=busqueda)
            )
        
        # Aplicar filtro por tipo de usuario
        if tipo_usuario:
            usuarios = usuarios.filter(tipo_usuario=tipo_usuario)
        
        # Aplicar filtro por fecha de último acceso (desde)
        if fecha_desde:
            try:
                fecha_desde_obj = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                usuarios = usuarios.filter(fecha_ultimo_acceso__gte=fecha_desde_obj)
            except ValueError as e:
                return JsonResponse({
                    'success': False,
                    'error': 'Formato de fecha inválido (desde)',
                    'message': 'La fecha debe estar en formato YYYY-MM-DD'
                }, status=400)
        
        # Aplicar filtro por fecha de último acceso (hasta)
        if fecha_hasta:
            try:
                fecha_hasta_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                fecha_hasta_completa = datetime.combine(fecha_hasta_obj, time(23, 59, 59))
                usuarios = usuarios.filter(fecha_ultimo_acceso__lte=fecha_hasta_completa)
            except ValueError as e:
                return JsonResponse({
                    'success': False,
                    'error': 'Formato de fecha inválido (hasta)',
                    'message': 'La fecha debe estar en formato YYYY-MM-DD'
                }, status=400)
        
        # Ordenar resultados
        usuarios = usuarios.order_by('-date_joined')
        
        # Calcular KPIs basados en los resultados filtrados
        total_filtrado = usuarios.count()
        kpis = {
            'total': total_filtrado,
            'admins': usuarios.filter(tipo_usuario='admin').count(),
            'clientes': usuarios.filter(tipo_usuario='cliente').count(),
            'desarrolladores': usuarios.filter(tipo_usuario='desarrollador').count(),
        }

        # Preparar datos para JSON
        usuarios_data = []
        for usuario in usuarios:
            try:
                usuarios_data.append({
                    'id': usuario.id,
                    'username': usuario.username,
                    'nombre_completo': usuario.nombre_completo,
                    'email': usuario.email,
                    'tipo_usuario': usuario.tipo_usuario,
                    'tipo_usuario_display': usuario.get_tipo_usuario_display(),
                    'telefono': usuario.telefono or '—',
                    'activo': usuario.activo,
                    'fecha_ultimo_acceso': usuario.fecha_ultimo_acceso.strftime('%d/%m/%Y %H:%M') if usuario.fecha_ultimo_acceso else 'Nunca',
                })
            except Exception as e:
                # Si hay error al procesar un usuario específico, continuar con los demás
                print(f"Error al procesar usuario {usuario.id}: {str(e)}")
                continue
        
        return JsonResponse({
            'success': True,
            'usuarios': usuarios_data,
            'total': len(usuarios_data),
            'kpis': kpis
        })
    
    except Usuario.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'No se encontraron usuarios',
            'message': 'No hay usuarios registrados en el sistema'
        }, status=404)
    
    except Exception as e:
        # Capturar cualquier otro error inesperado
        print(f"Error en buscar_usuarios_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al procesar la búsqueda. Por favor, inténtelo de nuevo.'
        }, status=500)
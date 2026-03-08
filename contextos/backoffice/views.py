from django.shortcuts import render
from django.db.models import Q
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
    Vista del listado de usuarios en backoffice - solo para administradores
    """
    # Obtener todos los usuarios como base
    usuarios = Usuario.objects.all()


    # Aplicar filtro de búsqueda general (nombre, email, teléfono)
    busqueda = request.GET.get('filter_busqueda', '').strip()
    tipo_usuario = request.GET.get('filter_tipo_usuario', '').strip()
    fecha_desde = request.GET.get('filter_fecha_desde', '').strip()
    fecha_hasta = request.GET.get('filter_fecha_hasta', '').strip()

    
    # Aplicar filtro de búsqueda general (nombre, apellido, email, teléfono, username)
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
        except ValueError:
            pass  # Ignorar si la fecha no es válida
    
    # Aplicar filtro por fecha de último acceso (hasta)
    
    if fecha_hasta:
        try:
            fecha_hasta_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
            # Incluir todo el día hasta las 23:59:59
            fecha_hasta_completa = datetime.combine(fecha_hasta_obj, time(23, 59, 59))
            usuarios = usuarios.filter(fecha_ultimo_acceso__lte=fecha_hasta_completa)
        except ValueError:
            pass  # Ignorar si la fecha no es válida
    
    # Ordenar resultados por fecha de registro (más recientes primero)
    usuarios = usuarios.order_by('-date_joined')
    
    datos = {
        'contexto_nombre': 'Backoffice',
        'contexto_css': 'main_backoffice',
        'usuario': request.user,
        'usuarios': usuarios,
    }
    
    return render(request, 'gestion/backoffice/usuarios.html', datos)
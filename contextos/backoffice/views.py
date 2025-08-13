from django.shortcuts import render
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
        'usuario': request.user,
        'stats': {
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'clientes': clientes_usuarios,
            'desarrolladores': desarrolladores_usuarios,
        }
    }
    
    return render(request, 'backoffice/dashboard.html', context)


@admin_required
def listado(request):
    """
    Vista del listado de backoffice - solo para administradores
    """
    return render(request, 'backoffice/listado.html')
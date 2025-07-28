from django.shortcuts import render
from django.contrib.auth import get_user_model
from core.decorators.auth_decorators import admin_required

User = get_user_model()


@admin_required
def dashboard(request):
    """
    Dashboard del backoffice con resumen de clientes y desarrolladores
    """
    # Estadísticas de usuarios
    total_usuarios = User.objects.filter(activo=True).count()
    total_clientes = User.objects.filter(role='cliente', activo=True).count()
    total_desarrolladores = User.objects.filter(role='desarrollador', activo=True).count()
    
    # Usuarios recientes
    usuarios_recientes = User.objects.filter(activo=True).order_by('-fecha_registro')[:5]
    
    context = {
        'total_usuarios': total_usuarios,
        'total_clientes': total_clientes,
        'total_desarrolladores': total_desarrolladores,
        'usuarios_recientes': usuarios_recientes,
    }
    
    return render(request, 'backoffice/dashboard.html', context)


@admin_required
def listado(request):
    return render(request, 'backoffice/listado.html')
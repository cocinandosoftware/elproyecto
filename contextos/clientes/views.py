from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from core.clientes.ClienteModel import Cliente


# Create your views here.

@login_required
def dashboard(request):
    """
    Dashboard específico para clientes
    """
    if not request.user.es_cliente():
        messages.error(request, 'No tienes permisos para acceder a esta área.')
        return redirect('auth:dashboard')
    
    context = {
        'usuario': request.user,
        'cliente': request.user.cliente_asociado,
    }
    
    return render(request, 'dashboard/cliente.html', context)


@login_required
def listado(request):
    """
    Vista del listado de clientes - solo para usuarios autenticados
    """
    # Verificar que el usuario tiene permisos (admin o cliente asociado)
    if not (request.user.es_admin() or request.user.es_cliente()):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('auth:dashboard')
    
    # Si es cliente, solo mostrar su información
    if request.user.es_cliente() and request.user.cliente_asociado:
        clientes = Cliente.objects.filter(id=request.user.cliente_asociado.id)
    else:
        # Si es admin, mostrar todos los clientes
        clientes = Cliente.objects.all()

    # Calcular la facturación total usando aggregate (más eficiente)
    total_facturacion = clientes.aggregate(total=Sum('total_facturacion'))['total'] or 0

    # Calcular promedio
    if clientes.count() > 0:
        facturacion_promedio = total_facturacion / clientes.count()
    else:
        facturacion_promedio = 0

    estadisticas = {
        'total_clientes': clientes.count(),
        'clientes_activos': clientes.filter(activo=True).count(),
        'clientes_inactivos': clientes.filter(activo=False).count(),
        'total_facturacion': total_facturacion,
        'facturacion_promedio': facturacion_promedio,
    }

    return render(request, 'clientes/listado.html', {'clientes': clientes, 'estadisticas': estadisticas})
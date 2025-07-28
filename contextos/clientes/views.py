from django.shortcuts import render
from django.db.models import Sum

from core.clientes.ClienteModel import Cliente
from core.decorators.auth_decorators import cliente_or_admin_required


# Create your views here.

@cliente_or_admin_required
def listado(request):

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
from django.shortcuts import render
from core.decorators.auth_decorators import desarrollador_or_admin_required


@desarrollador_or_admin_required
def listado(request):
    return render(request, 'desarrolladores/listado.html')
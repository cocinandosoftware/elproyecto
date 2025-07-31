from django.shortcuts import render
from contextos.decorators import desarrollador_required

@desarrollador_required
def dashboard(request):
    """
    Dashboard específico para desarrolladores
    """
    context = {
        'usuario': request.user,
    }
    
    return render(request, 'dashboard/desarrollador.html', context)


@desarrollador_required
def listado(request):
    """
    Vista del listado de desarrolladores - solo para usuarios autenticados
    """
    return render(request, 'desarrolladores/listado.html')
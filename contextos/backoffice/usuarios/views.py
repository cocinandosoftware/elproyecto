from django.shortcuts import render
from contextos.decorators import admin_required


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
    
    return render(request, 'gestion/backoffice/usuarios/listado.html', datos)

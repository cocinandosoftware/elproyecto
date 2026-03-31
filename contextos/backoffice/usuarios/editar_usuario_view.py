from django.shortcuts import render, get_object_or_404
from core.usuarios.UsuarioModel import Usuario
from contextos.decorators import admin_required


@admin_required
def editar_usuario(request, usuario_id):
    """
    Página completa de edición de usuario con tabs.
    Incluye datos básicos, tareas, proyectos, historial, etc.
    
    Esta vista renderiza un formulario completo con múltiples tabs para gestionar
    todos los aspectos relacionados con un usuario (datos personales, relaciones, etc.)
    """
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    # TODO: Cargar relaciones cuando existan los modelos
    # tareas = usuario.tareas.select_related('proyecto').order_by('-fecha_creacion')[:50]
    # proyectos = usuario.proyectos.all()
    # historial = usuario.historial.order_by('-fecha')[:100]
    
    # Por ahora, valores placeholder
    total_tareas = 0  # tareas.count()
    total_proyectos = 0  # proyectos.count()
    
    context = {
        'contexto_nombre': 'Backoffice',
        'contexto_css': 'main_backoffice',
        'usuario_actual': request.user,
        'usuario': usuario,
        # 'tareas': tareas,
        # 'proyectos': proyectos,
        # 'historial': historial,
        'total_tareas': total_tareas,
        'total_proyectos': total_proyectos,
    }
    
    return render(request, 'gestion/backoffice/usuarios/editar.html', context)

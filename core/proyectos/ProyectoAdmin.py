
from django.contrib import admin
from core.proyectos.ProyectoModel import Proyecto


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Proyecto.
    Permite gestionar los proyectos asociados a clientes y desarrolladores.
    """

    # Campos que se muestran en la lista
    list_display = (
        'nombre',
        'cliente',
        'desarrollador',
        'invitacion_estado',
        'invitacion_fecha',
        'invitacion_email_destinatario',
        'fecha_alta'
    )

    # Campos por los que se puede filtrar
    list_filter = ('cliente', 'desarrollador', 'invitacion_estado')

    # Campos por los que se puede buscar
    search_fields = ('nombre', 'cliente__nombre', 'desarrollador__nombre')

    # Orden por defecto
    ordering = ('-fecha_alta',) 

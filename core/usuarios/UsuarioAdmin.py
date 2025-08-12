from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.usuarios.UsuarioModel import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del admin para el modelo Usuario personalizado
    """
    
    # Campos que se muestran en la lista
    list_display = (
        'username', 
        'email', 
        'nombre_completo', 
        'tipo_usuario', 
        'cliente_asociado',
        'desarrollador_asociado',
        'activo', 
        'is_staff', 
        'date_joined',
        'fecha_ultimo_acceso'
    )
    
    # Campos por los que se puede filtrar
    list_filter = (
        'tipo_usuario', 
        'activo', 
        'is_staff', 
        'is_superuser', 
        'date_joined'
    )
    
    # Campos por los que se puede buscar
    search_fields = (
        'username', 
        'first_name', 
        'last_name', 
        'email'
    )
    
    # Orden por defecto
    ordering = ('username',)
    
    # Configuración de los fieldsets (cómo se organizan los campos en el formulario)
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': (
                'tipo_usuario', 
                'cliente_asociado',
                'desarrollador_asociado',
                'activo',
            )
        }),
    )
    
    # Campos que se muestran al agregar un nuevo usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': (
                'email',
                'first_name',
                'last_name',
                'tipo_usuario',
                'cliente_asociado',
                'desarrollador_asociado',
            )
        }),
    )
    
    # Campos de solo lectura
    readonly_fields = ('fecha_ultimo_acceso', 'date_joined')
    
    # Número de elementos por página
    list_per_page = 25
    
    def nombre_completo(self, obj):
        """Método para mostrar el nombre completo en la lista"""
        return obj.nombre_completo
    nombre_completo.short_description = 'Nombre Completo'

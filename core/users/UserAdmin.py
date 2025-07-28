from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .UserModel import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Administración personalizada para el modelo User
    """
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('role', 'telefono', 'activo', 'fecha_registro')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('role', 'telefono', 'email')
        }),
    )
    
    list_display = [
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'role', 
        'activo', 
        'fecha_registro'
    ]
    
    list_filter = [
        'role', 
        'activo', 
        'fecha_registro', 
        'is_staff', 
        'is_active'
    ]
    
    search_fields = [
        'username', 
        'email', 
        'first_name', 
        'last_name'
    ]
    
    readonly_fields = ['fecha_registro']
    
    ordering = ['-fecha_registro']

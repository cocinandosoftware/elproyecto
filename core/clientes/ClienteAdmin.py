from django.contrib import admin

from core.clientes.ClienteModel import Cliente

# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'nombre', 'nif', 'contacto_nombre', 'contacto_telefono', 'contacto_email', 'activo', 'total_facturacion')
    search_fields = ('razon_social', 'nombre', 'nif')
    list_filter = ('activo',)
    ordering = ('razon_social',)
    list_per_page = 20
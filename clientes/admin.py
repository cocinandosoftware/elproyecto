from django.contrib import admin

# Register your models here.


from .models import Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'nombre_comercial', 'nif', 'contacto_nombre', 'contacto_telefono', 'contacto_email', 'activo', 'total_facturacion')
    search_fields = ('razon_social', 'nombre_comercial', 'nif')
    list_filter = ('activo',)
    ordering = ('razon_social',)
    list_per_page = 20
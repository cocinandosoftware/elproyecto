from django.contrib import admin

# Register your models here.


from .models import Ciudad
@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais')
    search_fields = ('nombre', 'pais__nombre')
    list_filter = ('pais',)
    ordering = ('nombre',)
    list_per_page = 20
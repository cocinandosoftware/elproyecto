from django.contrib import admin

from core.desarrolladores.DesarrolladorModel import Desarrollador


@admin.register(Desarrollador)
class DesarrolladorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'perfil', 'activo')
    search_fields = ('nombre', 'perfil')
    list_filter = ('activo',)
    ordering = ('nombre',)
    list_per_page = 20

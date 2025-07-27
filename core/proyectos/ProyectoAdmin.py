
from django.contrib import admin
from core.proyectos.ProyectoModel import Proyecto


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('-nombre',)

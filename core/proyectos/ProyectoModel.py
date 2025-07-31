
from django.db import models

class Proyecto(models.Model):
    fecha_alta = models.DateField(auto_now_add=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cliente = models.ForeignKey(
        'core.Usuario',
        on_delete=models.CASCADE,
        related_name='proyectos_cliente',
        blank=True,
        null=True,
        help_text='Cliente asociado a este proyecto',
        limit_choices_to={'tipo_usuario': 'cliente'}
    )

    desarrollador = models.ForeignKey(
        'core.Usuario',
        on_delete=models.CASCADE,
        related_name='proyectos_desarrollador',
        blank=True,
        null=True,
        help_text='Desarrollador asignado a este proyecto',
        limit_choices_to={'tipo_usuario': 'desarrollador'}
    )

    # estados por choices
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='pendiente',
        help_text='Estado de este proyecto'
    )

    ESTADO_INVITACION_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    invitacion_estado = models.CharField(
        max_length=15,
        choices=ESTADO_INVITACION_CHOICES,
        default='pendiente',
        help_text='Estado de la invitación para este proyecto'
    )

    invitacion_fecha = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha de la invitación para este proyecto'
    )

    invitacion_email_destinatario = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        help_text='Email del destinatario de la invitación'
    )

    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"
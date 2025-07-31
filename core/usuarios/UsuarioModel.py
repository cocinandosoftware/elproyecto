from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    Permite asociar un usuario tanto a un cliente como a un desarrollador.
    """
    
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('desarrollador', 'Desarrollador'),
        ('admin', 'Administrador'),
    ]
    
    # Campos adicionales específicos de nuestro sistema
    tipo_usuario = models.CharField(
        max_length=15, 
        choices=TIPO_USUARIO_CHOICES,
        default='cliente',
        help_text='Tipo de usuario en el sistema'
    )
    
    telefono = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text='Número de teléfono del usuario'
    )
    
    fecha_ultimo_acceso = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='Última vez que el usuario accedió al sistema'
    )
    
    activo = models.BooleanField(
        default=True,
        help_text='Usuario activo en el sistema'
    )
    
    # Relaciones con clientes y desarrolladores (opcional, para flexibilidad)
    cliente_asociado = models.ForeignKey(
        'core.Cliente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        help_text='Cliente asociado a este usuario'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} - {self.get_tipo_usuario_display()}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def es_cliente(self):
        """Verifica si el usuario es un cliente"""
        return self.tipo_usuario == 'cliente'
    
    def es_desarrollador(self):
        """Verifica si el usuario es un desarrollador"""
        return self.tipo_usuario == 'desarrollador'
    
    def es_admin(self):
        """Verifica si el usuario es administrador"""
        return self.tipo_usuario == 'admin' or self.is_superuser
    
    def actualizar_ultimo_acceso(self):
        """Actualiza la fecha del último acceso"""
        from django.utils import timezone
        self.fecha_ultimo_acceso = timezone.now()
        self.save(update_fields=['fecha_ultimo_acceso'])

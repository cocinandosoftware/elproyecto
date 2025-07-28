from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser
    para incluir roles específicos de la plataforma
    """
    
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('desarrollador', 'Desarrollador'),
        ('admin', 'Administrador'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='cliente',
        verbose_name='Rol'
    )
    
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_cliente(self):
        return self.role == 'cliente'
    
    def is_desarrollador(self):
        return self.role == 'desarrollador'
    
    def is_admin_role(self):
        return self.role == 'admin'

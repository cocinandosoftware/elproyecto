from django.db import models

class Cliente(models.Model):
    fecha_alta = models.DateField(auto_now_add=True)
    razon_social = models.CharField(max_length=100)
    nombre_comercial = models.CharField(max_length=100)
    nif = models.CharField(max_length=20)
    contacto_nombre = models.CharField(max_length=15, blank=True, null=True)
    contacto_telefono = models.CharField(max_length=15, blank=True, null=True)
    contacto_email = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    total_facturacion = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


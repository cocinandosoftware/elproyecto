from django.db import models

class Desarrollador(models.Model):
    fecha_alta = models.DateField(auto_now_add=True)
    nombre = models.CharField(max_length=100)
    perfil = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)


    def __str__(self):
        return self.nombre


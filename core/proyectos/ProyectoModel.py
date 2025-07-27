
from django.db import models

class Proyecto(models.Model):
    fecha_alta = models.DateField(auto_now_add=True)
    nombre = models.CharField(max_length=100)
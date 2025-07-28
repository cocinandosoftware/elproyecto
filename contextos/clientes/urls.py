from django.urls import path, include
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.listado, name='listado'),
]
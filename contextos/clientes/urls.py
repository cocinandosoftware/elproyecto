from django.urls import path, include
from . import views

app_name = 'clientes'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.listado, name='listado_clientes'),
]
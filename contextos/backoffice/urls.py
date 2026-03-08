from django.urls import path, include
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.listado, name='listado_usuarios'),
]
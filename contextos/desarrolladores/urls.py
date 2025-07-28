from django.urls import path, include
from . import views

app_name = 'desarrolladores'

urlpatterns = [
    path('', views.listado, name='listado'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test-index/', views.test_index, name='test_index'),
    path('test-main/', views.test_main, name='test_main'),
]

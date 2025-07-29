from django.urls import path
from . import auth_views

app_name = 'auth'

urlpatterns = [
    # Autenticación
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Dashboard distribuidor
    path('dashboard/', auth_views.dashboard_view, name='dashboard'),
]

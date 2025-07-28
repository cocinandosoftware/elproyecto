#!/usr/bin/env python
"""
Script para probar las URLs del proyecto
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elproyecto.settings')
django.setup()

from django.urls import reverse, NoReverseMatch

# URLs a probar
urls_to_test = [
    ('web:index', 'Página de inicio'),
    ('authentication:login', 'Login'),
    ('authentication:logout', 'Logout'),
    ('authentication:dashboard', 'Dashboard'),
    ('clientes:listado', 'Listado clientes'),
    ('desarrolladores:listado', 'Listado desarrolladores'),
    ('backoffice:dashboard', 'Dashboard backoffice'),
]

print("🔗 Probando resolución de URLs...")
print("-" * 50)

all_good = True

for url_name, description in urls_to_test:
    try:
        url = reverse(url_name)
        print(f"✅ {description}: {url}")
    except NoReverseMatch as e:
        print(f"❌ {description}: ERROR - {e}")
        all_good = False

print("-" * 50)
if all_good:
    print("🎉 ¡Todas las URLs se resuelven correctamente!")
else:
    print("⚠️  Hay problemas con algunas URLs.")

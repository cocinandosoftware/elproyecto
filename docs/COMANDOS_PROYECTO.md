# 📝 Comandos Ejecutados en Este Proyecto "Hello World"

## 🎯 Resumen de lo que hicimos paso a paso

### 1. Verificación del entorno
```bash
python3 --version
# Resultado: Python 3.9.6
```

### 2. Creación del entorno virtual
```bash
cd /Users/sergigarcia/projects/cocinandosoftware/elproyecto
python3 -m venv venv
```

### 3. Activación del entorno virtual y actualización de pip
```bash
source venv/bin/activate
pip install --upgrade pip
# pip se actualizó de 21.2.4 a 25.1.1
```

### 4. Instalación de Django
```bash
pip install django
# Se instaló Django 4.2.23 junto con sus dependencias:
# - asgiref-3.9.1
# - sqlparse-0.5.3  
# - typing_extensions-4.14.1
```

### 5. Creación del proyecto Django
```bash
django-admin startproject elproyecto .
# El punto (.) hace que se cree en el directorio actual
```

### 6. Creación de la aplicación
```bash
python manage.py startapp hello
```

### 7. Aplicación de migraciones iniciales
```bash
python manage.py migrate
# Se aplicaron 18 migraciones iniciales para:
# - contenttypes
# - auth (sistema de autenticación)
# - admin (panel de administración)
# - sessions (manejo de sesiones)
```

### 8. Ejecución del servidor
```bash
python manage.py runserver
# Servidor ejecutándose en http://127.0.0.1:8000/
```

---

## 📂 Archivos que modificamos manualmente

### 1. `/hello/views.py`
```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_world(request):
    return HttpResponse("¡Hola Mundo! 🌍 Este es tu primer proyecto Django.")
```

### 2. `/hello/urls.py` (archivo nuevo)
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
]
```

### 3. `/elproyecto/settings.py`
```python
# Agregamos 'hello' a INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hello',  # ← Nuestra aplicación
]
```

### 4. `/elproyecto/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hello.urls')),  # ← Incluir URLs de la app hello
]
```

---

## 🏗️ Estructura final del proyecto

```
elproyecto/
├── .git/
├── .gitignore
├── LICENSE
├── venv/                    # Entorno virtual
├── elproyecto/             # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py         # ✏️ Modificado
│   ├── urls.py            # ✏️ Modificado
│   ├── wsgi.py
│   └── asgi.py
├── hello/                  # Nuestra aplicación
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py           # ✏️ Modificado
│   └── urls.py            # 🆕 Creado nuevo
├── manage.py
├── db.sqlite3             # 🆕 Base de datos creada automáticamente
├── COMANDOS_DJANGO.md     # 🆕 Esta guía completa
└── COMANDOS_PROYECTO.md   # 🆕 Comandos específicos del proyecto
```

---

## 🚀 Para ejecutar este proyecto desde cero

Si alguien quiere replicar exactamente lo que hicimos:

```bash
# 1. Clonar o crear el directorio del proyecto
cd /ruta/a/tu/proyecto

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar Django
pip install django

# 4. Los archivos ya están creados, solo necesitas aplicar migraciones
python manage.py migrate

# 5. Ejecutar el servidor
python manage.py runserver

# 6. Abrir en el navegador: http://127.0.0.1:8000/
```

---

## 🔧 Para continuar desarrollando

```bash
# Siempre activar el entorno virtual primero
source venv/bin/activate

# Luego ejecutar el servidor
python manage.py runserver

# Para parar el servidor: Ctrl+C

# Para desactivar el entorno virtual
deactivate
```

---

## 📋 Lista de verificación

- ✅ Python 3.9.6 instalado
- ✅ Entorno virtual creado y activado
- ✅ Django 4.2.23 instalado
- ✅ Proyecto "elproyecto" creado
- ✅ Aplicación "hello" creada
- ✅ Vista hello_world implementada
- ✅ URLs configuradas correctamente
- ✅ Aplicación registrada en settings.py
- ✅ Migraciones aplicadas
- ✅ Servidor funcionando en puerto 8000
- ✅ "¡Hola Mundo!" visible en el navegador

---

## 🎓 Lo que aprendiste

1. **Gestión de entornos virtuales** con `venv`
2. **Instalación de paquetes** con `pip`
3. **Estructura de un proyecto Django**
4. **Diferencia entre proyecto y aplicación**
5. **Sistema de URLs de Django**
6. **Vistas básicas con HttpResponse**
7. **Configuración en settings.py**
8. **Sistema de migraciones de Django**
9. **Servidor de desarrollo**

¡Felicidades! 🎉 Has creado tu primer proyecto Django funcional.

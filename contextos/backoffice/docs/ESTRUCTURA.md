# Estructura del Backoffice

Guía técnica sobre la arquitectura, organización y convenciones del área de administración.

## 📐 Arquitectura General

El backoffice sigue un patrón **modular por funcionalidad**, donde cada módulo:
- Tiene su propia carpeta
- Gestiona sus propias URLs
- Exporta su interfaz pública mediante `__init__.py`
- Se documenta de forma independiente

### Diagrama de Arquitectura

```
backoffice/
│
├── dashboard_views.py         ← Dashboard principal (stats globales)
├── urls.py                    ← URLs raíz que incluyen módulos
│
├── usuarios/                  ← Módulo independiente
│   ├── __init__.py            ← Exporta: listado, buscar_api, crear_api...
│   ├── views.py               ← Vistas de templates
│   ├── api_views.py           ← APIs JSON
│   └── urls.py                ← URLs del módulo
│
└── [futuros módulos]/
    ├── proyectos/
    ├── clientes/
    └── desarrolladores/
```

## 🔗 Sistema de URLs

### Configuración en Cascada

**1. URLs Principales** ([backoffice/urls.py](../urls.py))
```python
urlpatterns = [
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('usuarios/', include('contextos.backoffice.usuarios.urls')),
    # Futuros módulos:
    # path('proyectos/', include('contextos.backoffice.proyectos.urls')),
]
```

**2. URLs del Módulo** ([usuarios/urls.py](../usuarios/urls.py))
```python
app_name = 'usuarios'  # Namespace del módulo

urlpatterns = [
    path('', views.listado, name='listado'),
    path('api/buscar/', api_views.buscar_usuarios_api, name='buscar_api'),
    # ... más URLs del módulo
]
```

### Acceso a URLs en Templates

```django
{# URL del dashboard #}
{% url 'backoffice:dashboard' %}

{# URLs del módulo usuarios #}
{% url 'backoffice:usuarios:listado' %}
{% url 'backoffice:usuarios:buscar_api' %}
```

**Namespace completo**: `backoffice:usuarios:nombre_url`

## 📂 Organización de Módulos

### Estructura Estándar de un Módulo

```
nombre_modulo/
├── __init__.py          # Exporta interfaz pública
├── views.py             # Vistas que renderizan templates
├── api_views.py         # Endpoints API (JSON)
├── urls.py              # Configuración de URLs
└── [otros archivos]     # forms.py, serializers.py, etc. (opcional)
```

### Contenido de los Archivos

#### `__init__.py` - Interfaz Pública
```python
"""
Módulo de [nombre funcionalidad]
"""

from .views import vista1, vista2
from .api_views import api1, api2

__all__ = ['vista1', 'vista2', 'api1', 'api2']
```

#### `views.py` - Vistas de Templates
```python
from django.shortcuts import render
from contextos.decorators import admin_required

@admin_required
def listado(request):
    """
    Vista del listado de [entidad]
    """
    context = {
        'contexto_nombre': 'Backoffice',
        'contexto_css': 'main_backoffice',
        'usuario': request.user,
    }
    return render(request, 'gestion/backoffice/template.html', context)
```

#### `api_views.py` - APIs JSON
```python
from django.http import JsonResponse
from contextos.decorators import admin_required

@admin_required
def buscar_api(request):
    """
    API para búsqueda asíncrona de [entidad]
    """
    try:
        # Lógica de la API
        return JsonResponse({
            'success': True,
            'data': [...]
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
```

#### `urls.py` - Configuración de URLs
```python
from django.urls import path
from . import views, api_views

app_name = 'nombre_modulo'  # ← Importante para namespacing

urlpatterns = [
    path('', views.listado, name='listado'),
    path('api/buscar/', api_views.buscar_api, name='buscar_api'),
]
```

## 🔐 Sistema de Seguridad

### Decorador `@admin_required`

**Ubicación**: `contextos/decorators.py`

**Funcionalidad**:
1. Verifica que el usuario esté autenticado
2. Verifica que `request.user.tipo_usuario == 'admin'`
3. Si no cumple: desloguea y redirige a login con mensaje de error

**Uso obligatorio**: TODAS las vistas del backoffice deben usar este decorador.

```python
from contextos.decorators import admin_required

@admin_required
def mi_vista(request):
    # Ya está protegida automáticamente
    pass
```

## 📋 Convenciones de Código

### Nomenclatura

- **Variables y funciones**: `snake_case` en español
  ```python
  total_usuarios = Usuario.objects.count()
  def obtener_estadisticas():
  ```

- **Clases**: `PascalCase`
  ```python
  class Usuario(models.Model):
  ```

- **Constantes**: `UPPER_SNAKE_CASE`
  ```python
  TIPO_USUARIO_ADMIN = 'admin'
  ```

### Docstrings

Siempre en español, formato claro:
```python
def mi_funcion(request):
    """
    Descripción breve de lo que hace la función.
    
    Args:
        request: HttpRequest de Django
    
    Returns:
        HttpResponse o JsonResponse
    """
```

### Importaciones

Ordenar en 3 bloques:
```python
# 1. Librerías estándar de Python
from datetime import datetime
import json

# 2. Django y librerías de terceros
from django.shortcuts import render
from django.http import JsonResponse

# 3. Imports del proyecto
from core.usuarios.UsuarioModel import Usuario
from contextos.decorators import admin_required
```

## 🎨 Context para Templates

Todas las vistas de templates deben incluir:
```python
context = {
    'contexto_nombre': 'Backoffice',  # Nombre del contexto
    'contexto_css': 'main_backoffice',  # CSS sin extensión
    'usuario': request.user,  # Usuario actual
    # ... datos específicos de la vista
}
```

## 📊 APIs - Formato Estándar

### Respuesta Exitosa
```json
{
  "success": true,
  "message": "Operación completada correctamente",
  "data": {
    // datos específicos
  }
}
```

### Respuesta con Error
```json
{
  "success": false,
  "error": "Tipo de error",
  "message": "Mensaje descriptivo para el usuario"
}
```

### Códigos de Estado HTTP

- **200**: Operación exitosa
- **400**: Error de validación (datos incorrectos)
- **403**: Acceso prohibido (sin permisos)
- **404**: Recurso no encontrado
- **405**: Método HTTP no permitido
- **500**: Error interno del servidor

## 🧪 Testing

### Estructura de Tests

```python
from django.test import TestCase, Client
from django.urls import reverse
from core.usuarios.UsuarioModel import Usuario

class UsuariosModuloTest(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create(
            username='admin_test',
            tipo_usuario='admin'
        )
        self.client.force_login(self.admin)
    
    def test_listado(self):
        url = reverse('backoffice:usuarios:listado')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
```

## ➕ Agregar Nuevos Módulos

### Checklist Completo

- [ ] **1. Crear estructura de carpeta**
  ```bash
  mkdir contextos/backoffice/nuevo_modulo
  cd contextos/backoffice/nuevo_modulo
  ```

- [ ] **2. Crear archivos base**
  ```bash
  touch __init__.py views.py api_views.py urls.py
  ```

- [ ] **3. Implementar `__init__.py`**
  ```python
  from .views import listado
  from .api_views import buscar_api
  __all__ = ['listado', 'buscar_api']
  ```

- [ ] **4. Implementar `views.py`** (vistas de templates)
  - Usar decorador `@admin_required`
  - Preparar context con datos del módulo

- [ ] **5. Implementar `api_views.py`** (endpoints JSON)
  - APIs para CRUD
  - Manejo de errores con try-except
  - Respuestas en formato estándar

- [ ] **6. Configurar `urls.py`**
  ```python
  from django.urls import path
  from . import views, api_views
  
  app_name = 'nuevo_modulo'
  urlpatterns = [...]
  ```

- [ ] **7. Incluir en `backoffice/urls.py`**
  ```python
  path('nuevo-modulo/', include('contextos.backoffice.nuevo_modulo.urls'))
  ```

- [ ] **8. Crear template** en `templates/gestion/backoffice/nuevo_modulo/`

- [ ] **9. Documentar** en `docs/modulos/nuevo_modulo.md`

- [ ] **10. Actualizar** el índice en `docs/README.md`

## 🔍 Debugging

### Verificar URLs
```python
python manage.py show_urls | grep backoffice
```

### Verificar Imports
```python
python manage.py shell
>>> from contextos.backoffice.usuarios import listado
>>> print(listado)
```

### Ver Errores
```bash
python manage.py check
python manage.py runserver  # Ver logs en consola
```

## 📌 Notas Importantes

- **No usar `from .backoffice import views`**: El backoffice no tiene archivo `views.py` central
- **Importar desde módulos**: `from .usuarios import listado`
- **Cada módulo es independiente**: No hay dependencias cruzadas entre módulos
- **Dashboard es especial**: Está en `dashboard_views.py` (no en módulo separado)

---

**Última actualización**: Marzo 2026

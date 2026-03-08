# Instrucciones de Desarrollo para ElProyecto 🚀

## 📋 Resumen del Proyecto

**ElProyecto** es una plataforma Django que conecta clientes y desarrolladores para gestionar proyectos de software de forma estructurada. La aplicación implementa un sistema de roles (cliente, desarrollador, administrador) con dashboards diferenciados y control de acceso granular.

## 🏗️ Arquitectura y Estructura

### Organización del Proyecto

- **`core/`**: Aplicación principal con modelos genéricos y reutilizables
  - Modelos organizados en submódulos: `clientes/`, `desarrolladores/`, `proyectos/`, `usuarios/`
  - Cada módulo tiene su propio `*Model.py` y `*Admin.py`
  - Mantener esta app **genérica** y **reutilizable**

- **`contextos/`**: Lógica específica de negocio y vistas por rol
  - **No es una app Django estándar** - contiene decoradores y vistas organizadas por contexto
  - Submódulos: `backoffice/`, `clientes/`, `desarrolladores/`
  - Contiene los decoradores personalizados en `decorators.py`
  - Contiene archivos SCSS para estilos específicos de cada contexto

- **`web/`**: Aplicación para el sitio público
  - Vistas públicas (landing page)
  - Autenticación (`auth_views.py`, `auth_urls.py`)
  - Archivos SCSS para el sitio público

- **`templates/`**: Plantillas organizadas por contexto
  - `gestion/`: Templates para áreas autenticadas (backoffice, clientes, desarrolladores)
  - `web/`: Templates públicos (index, login, register)

- **`docs/`**: Documentación del proyecto en español
  - Guías técnicas sobre Django (fixtures, comandos, estáticos)
  - Documentación de decisiones de arquitectura (decoradores, autenticación)

### Modelo de Datos

El proyecto usa un **modelo de usuario personalizado** (`core.Usuario`) que extiende `AbstractUser`:

```python
AUTH_USER_MODEL = 'core.Usuario'
```

**Tipos de usuario**:
- `cliente`: Acceso al área de clientes
- `desarrollador`: Acceso al área de desarrolladores
- `admin`: Acceso completo al backoffice

**Métodos de verificación de roles**:
- `user.es_cliente()` → Verifica si es cliente
- `user.es_desarrollador()` → Verifica si es desarrollador
- `user.es_admin()` → Verifica si es administrador

## 🔐 Sistema de Control de Acceso

### Decoradores Personalizados

**SIEMPRE usar los decoradores del proyecto** en lugar de `@login_required` directamente:

```python
from contextos.decorators import cliente_required, desarrollador_required, admin_required
```

**Decoradores disponibles**:
- `@cliente_required`: Login + verificación de rol cliente
- `@desarrollador_required`: Login + verificación de rol desarrollador
- `@admin_required`: Login + verificación de rol admin
- `@cliente_or_admin_required`: Permite acceso a clientes O admins
- `@desarrollador_or_admin_required`: Permite acceso a desarrolladores O admins

**Ubicación**: `contextos/decorators.py` (NO en `core` porque están acoplados a la lógica de negocio)

**Ejemplo de uso correcto**:
```python
from contextos.decorators import cliente_required

@cliente_required
def dashboard(request):
    # La vista ya está protegida automáticamente
    return render(request, 'gestion/clientes/dashboard.html')
```

### Comportamiento de los Decoradores

- **Si no está logueado**: Redirige a `/login/`
- **Si no tiene permisos**: 
  - Clientes/Desarrolladores: Desloguea y redirige a login con mensaje de error
  - Admin: Redirige al dashboard del usuario con mensaje de error
- **Mensajes**: Se usan `messages.error()` o `messages.success()` de Django

## 🎨 Sistema de Estilos

### SCSS y Organización de Estilos

El proyecto usa **SCSS** para los estilos. Cada contexto tiene sus propios archivos SCSS:

**Ubicaciones**:
- `contextos/scss/`: Estilos para áreas autenticadas
  - `main_backoffice.scss` → Estilos del backoffice
  - `main_clientes.scss` → Estilos del área de clientes
  - `main_desarrolladores.scss` → Estilos del área de desarrolladores
- `web/scss/`: Estilos para el sitio público

**Variables de color por rol**:
- **Clientes**: Azul (`#667eea`, `#764ba2`)
- **Desarrolladores**: Verde (`#28a745`, `#20c997`)
- **Administradores**: Rojo (`#dc3545`, `#e74c3c`)

### Anchos y Contenedores

**IMPORTANTE**: Los módulos de listado (tablas, grids de datos, búsquedas) **SIEMPRE deben usar el 100% del ancho disponible** para aprovechar el espacio horizontal.

**Reglas de ancho**:
- **Listados y tablas**: 100% del ancho (sin max-width)
- **Dashboards y formularios**: max-width de 1400px para mejor legibilidad
- **Contenedor `.listado-container`**: Siempre width: 100%

**Implementación en SCSS**:
```scss
.container {
    width: 100%;
    
    // Para contenido normal (dashboards, formularios)
    &:not(:has(.listado-container)) {
        max-width: 1400px;
    }
    
    // Para listados, usar 100% del ancho disponible
    &:has(.listado-container) {
        max-width: 100%;
        padding: 1rem;
    }
}
```

**En templates de listado**:
```django
<div class="container">
    <div class="listado-container">
        <!-- Contenido del listado -->
    </div>
</div>
```

### Archivos Estáticos

**Configuración en templates**:

```python
# En settings.py
STATICFILES_DIRS = [
    BASE_DIR / 'web' / 'static',
    BASE_DIR / 'contextos' / 'static',
]
```

**En templates, siempre usar**:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/main.css' %}">
```

**Estructura de static**:
```
contextos/static/css/
├── main_backoffice.css
├── main_clientes.css
└── main_desarrolladores.css

web/static/css/
└── main.css
```

**Context variables para templates**:
```python
context = {
    'contexto_nombre': 'Backoffice',  # Nombre del contexto
    'contexto_css': 'main_backoffice',  # CSS sin extensión
    'usuario': request.user,
}
```

## 📝 Convenciones de Código

### Nomenclatura

**Variables, funciones y métodos**: Español, snake_case
```python
def obtener_proyectos_activos(cliente_id):
    proyectos_activos = Proyecto.objects.filter(activo=True)
    return proyectos_activos
```

**Clases y modelos**: PascalCase
```python
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
```

**Constantes**: UPPER_SNAKE_CASE
```python
TIPO_USUARIO_CHOICES = [
    ('cliente', 'Cliente'),
    ('desarrollador', 'Desarrollador'),
]
```

### Comentarios y Docstrings

**SIEMPRE en español**, descriptivos y claros:

```python
def dashboard(request):
    """
    Dashboard específico para administradores.
    Muestra estadísticas generales del sistema.
    """
    # Calcular estadísticas
    total_usuarios = Usuario.objects.count()
    
    return render(request, 'gestion/backoffice/dashboard.html', context)
```

### Organización de Imports

```python
# 1. Librerías estándar de Python
from datetime import datetime
from functools import wraps

# 2. Librerías de terceros (Django)
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# 3. Imports del proyecto
from core.usuarios.UsuarioModel import Usuario
from contextos.decorators import admin_required
```

## 🗄️ Modelos Django

### Estructura de Modelos

Los modelos están **organizados en submódulos** dentro de `core/`:

```
core/
├── clientes/
│   ├── ClienteModel.py
│   └── ClienteAdmin.py
├── desarrolladores/
│   ├── DesarrolladorModel.py
│   └── DesarrolladorAdmin.py
├── proyectos/
│   ├── ProyectoModel.py
│   └── ProyectoAdmin.py
└── usuarios/
    ├── UsuarioModel.py
    └── UsuarioAdmin.py
```

### Buenas Prácticas para Modelos

1. **Campos comunes**:
   ```python
   fecha_alta = models.DateField(auto_now_add=True)
   activo = models.BooleanField(default=True)
   ```

2. **Método `__str__`**: Siempre implementarlo
   ```python
   def __str__(self):
       return f"{self.contacto_nombre} ({self.nombre})"
   ```

3. **Help text**: Documentar campos importantes
   ```python
   tipo_usuario = models.CharField(
       max_length=15,
       choices=TIPO_USUARIO_CHOICES,
       help_text='Tipo de usuario en el sistema'
   )
   ```

4. **Related names**: Usar nombres descriptivos
   ```python
   cliente_asociado = models.ForeignKey(
       'core.Cliente',
       on_delete=models.SET_NULL,
       related_name='usuarios',  # Acceso desde Cliente: cliente.usuarios.all()
   )
   ```

## 🖼️ Templates Django

### Estructura de Templates

```
templates/
├── gestion/
│   ├── base.html  # Template base para áreas autenticadas
│   ├── backoffice/
│   │   ├── header.html
│   │   ├── dashboard.html
│   │   └── usuarios.html
│   ├── clientes/
│   │   ├── dashboard.html
│   │   └── listado.html
│   └── desarrolladores/
│       ├── dashboard.html
│       └── listado.html
└── web/
    ├── index.html  # Página principal pública
    └── auth/
        ├── login.html
        └── register.html
```

### Convenciones de Templates

1. **Extender de base.html**:
   ```django
   {% extends 'gestion/base.html' %}
   ```

2. **Cargar static al inicio**:
   ```django
   {% load static %}
   ```

3. **Usar variables de contexto**:
   ```django
   <link rel="stylesheet" href="{% static 'css/' %}{{ contexto_css }}.css">
   ```

4. **Mensajes de Django**:
   ```django
   {% if messages %}
       {% for message in messages %}
           <div class="alert alert-{{ message.tags }}">
               {{ message }}
           </div>
       {% endfor %}
   {% endif %}
   ```

## 🔄 Vistas Django

### Estructura de Vistas

Las vistas están **organizadas por contexto** en `contextos/`:

```
contextos/
├── backoffice/
│   └── views.py
├── clientes/
│   └── views.py
└── desarrolladores/
    └── views.py
```

### Patrón de Vista Típico

```python
from django.shortcuts import render
from django.db.models import Q
from contextos.decorators import cliente_required
from core.proyectos.ProyectoModel import Proyecto

@cliente_required
def dashboard(request):
    """
    Dashboard para clientes con sus proyectos activos
    """
    # Obtener datos específicos del usuario
    proyectos = Proyecto.objects.filter(
        cliente=request.user.cliente_asociado,
        activo=True
    )
    
    # Preparar contexto
    context = {
        'contexto_nombre': 'Clientes',
        'contexto_css': 'main_clientes',
        'usuario': request.user,
        'proyectos': proyectos,
    }
    
    return render(request, 'gestion/clientes/dashboard.html', context)
```

### Filtros y Búsquedas

Usar **Q objects** para búsquedas complejas:

```python
from django.db.models import Q

# Filtro de búsqueda general
busqueda = request.GET.get('filter_busqueda', '').strip()
if busqueda:
    usuarios = usuarios.filter(
        Q(first_name__icontains=busqueda) |
        Q(last_name__icontains=busqueda) |
        Q(email__icontains=busqueda)
    )
```

## 🛠️ URLs y Enrutamiento

### Estructura de URLs

```
elproyecto/urls.py  # URLs principales
├── web/urls.py  # URLs públicas
├── web/auth_urls.py  # URLs de autenticación
├── contextos/backoffice/urls.py  # URLs del backoffice
├── contextos/clientes/urls.py  # URLs del área de clientes
└── contextos/desarrolladores/urls.py  # URLs del área de desarrolladores
```

### Patrón de URLs

```python
# En urls.py de cada módulo
from django.urls import path
from . import views

app_name = 'clientes'  # Namespace de la app

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('proyectos/', views.listado, name='listado'),
]
```

**Uso en templates**:
```django
<a href="{% url 'clientes:dashboard' %}">Dashboard</a>
```

## 🔧 Comandos de Gestión Django

El proyecto tiene **comandos personalizados** en `core/management/commands/`:

- `crear_semilla`: Crea datos de prueba
- `copy_data`: Copia datos entre bases de datos

**Uso**:
```bash
python manage.py crear_semilla
python manage.py copy_data
```

## 📦 Base de Datos

- **Desarrollo**: SQLite (`db.sqlite3`)
- **Producción**: PostgreSQL (recomendado)

**Migraciones**:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Datos de Prueba

Usar el comando personalizado para crear datos de semilla:

```bash
python manage.py crear_semilla
```

Consultar `docs/DATOS_SEMILLA.md` para más información.

## 📚 Documentación

El proyecto tiene **documentación técnica extensa** en la carpeta `docs/`:

- `ARCHIVOS_ESTATICOS.md`: Guía completa de archivos estáticos
- `COMANDOS_DJANGO.md`: Comandos Django útiles
- `COMANDOS_PROYECTO.md`: Comandos específicos del proyecto
- `DATOS_SEMILLA.md`: Información sobre datos de prueba
- `DECORADORES_PERMISOS.md`: Sistema de decoradores
- `FIXTURES_DJANGO.md`: Uso de fixtures
- `SISTEMA_AUTENTICACION.md`: Sistema de autenticación completo

**SIEMPRE consultar la documentación** antes de implementar funcionalidades similares.

## ✅ Checklist para Nuevas Funcionalidades

### Al crear una nueva vista:
- [ ] Usar el decorador de permisos apropiado (`@cliente_required`, etc.)
- [ ] Incluir docstring en español
- [ ] Preparar context con `contexto_nombre` y `contexto_css`
- [ ] Manejar errores con `messages.error()` o `messages.success()`
- [ ] Crear/actualizar template correspondiente
- [ ] Registrar URL con namespace apropiado

### Al crear un nuevo modelo:
- [ ] Organizar en submódulo dentro de `core/`
- [ ] Incluir `__str__()` method
- [ ] Agregar campos `fecha_alta` y `activo` si aplica
- [ ] Documentar con `help_text` en campos importantes
- [ ] Crear archivo `*Admin.py` correspondiente
- [ ] Hacer migraciones: `makemigrations` y `migrate`
- [ ] Testear en el admin de Django

### Al crear estilos:
- [ ] Usar SCSS en la carpeta apropiada
- [ ] Seguir la convención de colores por rol
- [ ] Compilar SCSS a CSS (en `static/css/`)
- [ ] Usar variables del proyecto en `variables.scss`

## 🎯 Principios de Desarrollo

1. **Consistencia**: Seguir los patrones existentes del proyecto
2. **Documentación**: Todo en español, clara y concisa
3. **Seguridad**: Siempre usar los decoradores de permisos
4. **Modularidad**: Mantener `core/` genérico, `contextos/` específico
5. **Responsabilidad**: Cada módulo tiene una responsabilidad clara
6. **DRY**: No repetir código, usar los decoradores y utilidades del proyecto
7. **Nombres descriptivos**: Variables y funciones que expliquen su propósito
8. **Separación de responsabilidades**: Modelos en `core/`, vistas en `contextos/`, templates en `templates/`

## 🚀 Entorno de Desarrollo

**Entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

**Instalar dependencias**:
```bash
pip install -r requirements.txt
```

**Servidor de desarrollo**:
```bash
python manage.py runserver
```

**Acceder**:
- Sitio público: `http://localhost:8000/`
- Admin Django: `http://localhost:8000/admin/`

## 🔍 Debugging

- Usar `print()` o `breakpoint()` para debugging
- Revisar logs de Django en la consola
- Usar Django Debug Toolbar en desarrollo (si está instalado)
- Verificar errores de permisos revisando los decoradores

## 📌 Notas Finales

- **Todo el código y comentarios en ESPAÑOL**
- **Seguir la estructura modular existente**
- **Usar los decoradores personalizados del proyecto**
- **Consultar la documentación en `docs/` antes de implementar**
- **Mantener consistencia con los patrones existentes**
- **Documentar decisiones importantes en `docs/`**

---

**Última actualización**: Marzo 2026
**Versión Django**: 4.2.23
**Versión Python**: 3.8+

# Documentación del Backoffice

Documentación completa del área de administración de ElProyecto.

## 📚 Índice de Documentación

### 📖 Arquitectura
- [**ESTRUCTURA.md**](ESTRUCTURA.md) - Organización de archivos, URLs y convenciones del backoffice

### 📦 Módulos Disponibles
- [**Gestión de Usuarios**](modulos/usuarios.md) - CRUD completo, APIs, búsqueda con filtros y paginación

## 🗂️ Estructura de Archivos

```
backoffice/
├── __init__.py
├── urls.py                    # URLs principales del backoffice
├── dashboard_views.py         # Vista del dashboard de administradores
├── docs/                      # 📂 Documentación centralizada
│   ├── README.md              # Este archivo (índice)
│   ├── ESTRUCTURA.md          # Arquitectura y convenciones
│   └── modulos/               # Documentación por módulo
│       └── usuarios.md        # Módulo de usuarios
└── usuarios/                  # 📂 Módulo de gestión de usuarios
    ├── __init__.py            # Exporta funciones del módulo
    ├── views.py               # Vistas de templates
    ├── api_views.py           # APIs CRUD
    └── urls.py                # URLs del módulo
```

## 🎯 Guías Rápidas

### Acceder a Vistas de un Módulo

```python
# Opción 1: Importar desde el módulo (recomendado)
from contextos.backoffice.usuarios import listado, crear_usuario_api

# Opción 2: Importar desde archivos específicos
from contextos.backoffice.usuarios.views import listado
from contextos.backoffice.usuarios.api_views import crear_usuario_api

# Dashboard
from contextos.backoffice.dashboard_views import dashboard
```

### Crear un Nuevo Módulo

Ver guía completa en [ESTRUCTURA.md](ESTRUCTURA.md#-agregar-nuevos-módulos)

**Pasos resumidos**:
1. Crear carpeta: `backoffice/nuevo_modulo/`
2. Crear archivos: `__init__.py`, `views.py`, `api_views.py`, `urls.py`
3. Incluir en `backoffice/urls.py`
4. Documentar en `docs/modulos/nuevo_modulo.md`

### Proteger Vistas

```python
from contextos.decorators import admin_required

@admin_required  # ← Obligatorio en todas las vistas del backoffice
def mi_vista(request):
    # El decorador verifica autenticación y rol admin
    return render(request, 'template.html')
```

## 🔗 Enlaces Útiles

### Documentación del Proyecto
- [Instrucciones Generales](../../../.github/copilot-instructions.md)
- [Sistema de Autenticación](../../../docs/SISTEMA_AUTENTICACION.md)
- [Decoradores de Permisos](../../../docs/DECORADORES_PERMISOS.md)
- [Archivos Estáticos](../../../docs/ARCHIVOS_ESTATICOS.md)

### Código del Backoffice
- [Dashboard](../dashboard_views.py)
- [URLs Principales](../urls.py)
- [Módulo Usuarios](../usuarios/)

## 📝 Convenciones Generales

### Código
- **Idioma**: Todo en español (código, comentarios, docstrings)
- **Nomenclatura**: `snake_case` para funciones y variables
- **Decoradores**: Siempre `@admin_required` en vistas del backoffice

### APIs
- **Formato de respuesta**: JSON estándar
  ```json
  {
    "success": true/false,
    "message": "Mensaje descriptivo",
    "data": {...}
  }
  ```
- **Códigos HTTP**: Usar correctamente (200, 400, 403, 404, 500)
- **Manejo de errores**: Try-except con mensajes claros

### Archivos
- **views.py**: Vistas que renderizan templates
- **api_views.py**: Endpoints API (JSON)
- **urls.py**: Configuración de URLs del módulo
- **__init__.py**: Exporta la interfaz pública del módulo

## 🚀 Próximos Módulos

Módulos planificados para el backoffice:
- [ ] **Proyectos**: Gestión de proyectos del sistema
- [ ] **Clientes**: Administración de clientes
- [ ] **Desarrolladores**: Gestión de desarrolladores
- [ ] **Reportes**: Generación de informes y estadísticas
- [ ] **Configuración**: Parámetros del sistema

---

**Última actualización**: Marzo 2026

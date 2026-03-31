# Módulo de Usuarios - Backoffice

Módulo completo para la gestión de usuarios desde el área de administración.

## 📁 Estructura

```
usuarios/
├── __init__.py      # Exportaciones del módulo
├── views.py         # Vistas de templates
├── api_views.py     # APIs para CRUD de usuarios
├── urls.py          # Configuración de URLs
└── README.md        # Este archivo
```

## 🎯 Funcionalidades

### Vistas de Templates (`views.py`)

#### `listado(request)`
Vista principal del listado de usuarios. Renderiza el template con carga asíncrona.
- **URL**: `/backoffice/usuarios/`
- **Template**: `gestion/backoffice/usuarios.html`
- **Permisos**: `@admin_required`

### APIs (`api_views.py`)

#### `buscar_usuarios_api(request)`
Búsqueda asíncrona con soporte completo de filtros, ordenación y paginación.

**Método**: `GET`  
**URL**: `/backoffice/usuarios/api/buscar/`  
**Parámetros GET**:
- `filter_busqueda`: Búsqueda por nombre, email, teléfono, username
- `filter_tipo_usuario`: Filtrar por tipo (admin/cliente/desarrollador)
- `filter_fecha_desde`: Fecha de último acceso desde
- `filter_fecha_hasta`: Fecha de último acceso hasta
- `order_by`: Campo de ordenación (id, username, nombre_completo, email, etc.)
- `order_dir`: Dirección (asc/desc)
- `page`: Número de página
- `page_size`: Elementos por página (max 100)

**Respuesta**:
```json
{
  "success": true,
  "usuarios": [...],
  "kpis": {
    "total": 15,
    "admins": 2,
    "clientes": 8,
    "desarrolladores": 5
  },
  "pagination": {
    "current_page": 1,
    "total_pages": 2,
    "page_size": 10,
    "total_items": 15,
    "has_next": true,
    "has_previous": false
  },
  "ordering": {
    "order_by": "id",
    "order_dir": "asc"
  }
}
```

#### `obtener_usuario_api(request, usuario_id)`
Obtiene los datos de un usuario específico para edición.

**Método**: `GET`  
**URL**: `/backoffice/usuarios/api/obtener/<usuario_id>/`  
**Respuesta**:
```json
{
  "success": true,
  "usuario": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "Sistema",
    "tipo_usuario": "admin",
    "telefono": "",
    "activo": true
  }
}
```

#### `crear_usuario_api(request)`
Crea un nuevo usuario con validación completa.

**Método**: `POST`  
**URL**: `/backoffice/usuarios/api/crear/`  
**Body (JSON)**:
```json
{
  "username": "nuevousuario",
  "email": "nuevo@example.com",
  "password": "Password123",
  "first_name": "Nombre",
  "last_name": "Apellido",
  "tipo_usuario": "cliente",
  "telefono": "123456789",
  "activo": true
}
```

**Validaciones**:
- Username: Mínimo 3 caracteres, único
- Email: Formato válido, único
- Password: Mínimo 8 caracteres
- Tipo usuario: admin/cliente/desarrollador
- Teléfono: Máximo 15 caracteres (opcional)

#### `editar_usuario_api(request, usuario_id)`
Edita un usuario existente. El password es opcional (si está vacío, se mantiene el actual).

**Método**: `POST`  
**URL**: `/backoffice/usuarios/api/editar/<usuario_id>/`  
**Body**: Misma estructura que crear, pero password es opcional

#### `eliminar_usuario(request, usuario_id)`
Elimina un usuario del sistema.

**Método**: `POST` o `DELETE`  
**URL**: `/backoffice/usuarios/eliminar/<usuario_id>/`  
**Restricciones**:
- No se puede auto-eliminar
- Devuelve los datos del usuario eliminado

## 🔗 Integración de URLs

Las URLs de este módulo se incluyen en el archivo principal del backoffice:

```python
# En backoffice/urls.py
path('usuarios/', include('contextos.backoffice.usuarios.urls'))
```

Esto hace que todas las URLs del módulo estén disponibles bajo el prefijo `/backoffice/usuarios/`.

## 🔐 Seguridad

- Todas las vistas requieren autenticación (`@admin_required`)
- Validación de permisos de administrador
- Validación exhaustiva de datos en APIs
- Contraseñas hasheadas automáticamente
- Prevención de auto-eliminación

## 📊 Flujo de Trabajo

1. Admin accede a `/backoffice/usuarios/`
2. JavaScript llama a `/api/buscar/` para cargar datos
3. Admin puede:
   - Filtrar y ordenar usuarios
   - Ver detalles con `/api/obtener/<id>/`
   - Crear con `/api/crear/`
   - Editar con `/api/editar/<id>/`
   - Eliminar con `/eliminar/<id>/`

## 🧪 Testing

Para testear este módulo:
```python
from django.test import TestCase
from contextos.backoffice.usuarios import views, api_views
```

## 📝 Notas

- Los KPIs se calculan ANTES de paginar para reflejar resultados filtrados
- La ordenación se aplica en el backend (no en JavaScript)
- Paginación configurable con límite máximo de 100 items por página
- Manejo robusto de errores con códigos HTTP apropiados

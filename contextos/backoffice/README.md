# Backoffice - Organización de Vistas

Este módulo contiene las vistas del área de backoffice (administración) del proyecto.

## 📁 Estructura de Archivos

```
backoffice/
├── __init__.py
├── urls.py                    # Configuración de URLs del backoffice
├── views.py                   # Índice que importa todas las vistas
├── dashboard_views.py         # Vista del dashboard de administradores
├── usuarios_views.py          # Vistas de templates para usuarios
└── usuarios_api_views.py      # APIs para operaciones CRUD de usuarios
```

## 📄 Descripción de Archivos

### `dashboard_views.py`
- **Propósito**: Vista principal del dashboard de administradores
- **Vistas**: 
  - `dashboard`: Muestra estadísticas generales del sistema

### `usuarios_views.py`
- **Propósito**: Vistas que renderizan templates de la gestión de usuarios
- **Vistas**:
  - `listado`: Vista del listado de usuarios (carga asíncrona con JS)

### `usuarios_api_views.py`
- **Propósito**: Endpoints API para operaciones CRUD de usuarios
- **Vistas**:
  - `buscar_usuarios_api`: Búsqueda asíncrona con filtros, ordenación y paginación
  - `obtener_usuario_api`: Obtener datos de un usuario específico
  - `crear_usuario_api`: Crear un nuevo usuario
  - `editar_usuario_api`: Editar un usuario existente
  - `eliminar_usuario`: Eliminar un usuario

### `views.py`
- **Propósito**: Archivo índice que importa todas las vistas de los submódulos
- **Uso**: Mantiene compatibilidad con imports antiguos

### `urls.py`
- **Propósito**: Configuración de URLs del backoffice
- **Imports**: Importa desde los módulos especializados organizados por comentarios

## 🔐 Seguridad

Todas las vistas están protegidas con el decorador `@admin_required` que verifica:
- Usuario autenticado
- Usuario con rol de administrador (`tipo_usuario='admin'`)

## 📝 Convenciones

- **Idioma**: Todo el código y comentarios en español
- **Formato de respuesta API**: JSON con estructura estándar
  ```python
  {
      'success': True/False,
      'message': 'Mensaje descriptivo',
      'data': {...}  # Datos específicos de la operación
  }
  ```
- **Manejo de errores**: Try-except con mensajes descriptivos y status codes apropiados

## 🔄 Flujo de Trabajo

1. **Usuario accede al dashboard**: `dashboard_views.dashboard()`
2. **Usuario accede al listado**: `usuarios_views.listado()` → Renderiza template
3. **JavaScript carga datos**: Llama a `usuarios_api_views.buscar_usuarios_api()`
4. **CRUD de usuarios**: Se usan las APIs correspondientes en `usuarios_api_views.py`

## ✅ Ventajas de esta Organización

- **Separación de responsabilidades**: Cada archivo tiene un propósito claro
- **Mantenibilidad**: Fácil encontrar y modificar código específico
- **Escalabilidad**: Fácil agregar nuevas funcionalidades en archivos dedicados
- **Testing**: Más fácil escribir tests unitarios por módulo
- **Legibilidad**: Archivos más pequeños y enfocados en una tarea

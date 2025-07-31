# Sistema de Decoradores de Permisos

Este documento explica el sistema de decoradores implementado para el control de acceso en la aplicación.

## 🎯 Objetivo

Simplificar la validación de permisos en las vistas con un solo decorador que maneja tanto la autenticación como la autorización, eliminando código repetitivo y centralizando toda la lógica de control de acceso.

## 📂 Ubicación

Los decoradores están definidos en: `contextos/decorators.py`

## 🏗️ Arquitectura

Los decoradores están ubicados en el módulo `contextos` porque:
- Están **acoplados a la lógica de negocio** específica (roles cliente, desarrollador, admin)
- El módulo `core` debe ser **genérico** y reutilizable
- Los `contextos` contienen la lógica específica de cada área de la aplicación
- Facilita el **mantenimiento** y la **organización** del código

## 🛠️ Decoradores Disponibles

### Decoradores de Rol Único

#### `@cliente_required`
- **Funcionalidad**: Verifica login + requiere que el usuario sea cliente
- **Si no está logueado**: Redirige a login
- **Si no es cliente**: Desloguea y redirige a login con mensaje de error
- **Mensaje**: "No tienes permisos para acceder a esta área."

#### `@desarrollador_required`
- **Funcionalidad**: Verifica login + requiere que el usuario sea desarrollador
- **Si no está logueado**: Redirige a login
- **Si no es desarrollador**: Desloguea y redirige a login con mensaje de error
- **Mensaje**: "No tienes permisos para acceder a esta área."

#### `@admin_required`
- **Funcionalidad**: Verifica login + requiere que el usuario sea administrador
- **Si no está logueado**: Redirige a login
- **Si no es admin**: Redirige al dashboard del usuario con mensaje de error
- **Mensaje**: "No tienes permisos para acceder a esta sección."

### Decoradores de Múltiples Roles

#### `@cliente_or_admin_required`
- **Funcionalidad**: Verifica login + permite acceso a clientes O administradores
- **Si no está logueado**: Redirige a login
- **Si no es cliente ni admin**: Redirige al dashboard del usuario

#### `@desarrollador_or_admin_required`
- **Funcionalidad**: Verifica login + permite acceso a desarrolladores O administradores
- **Si no está logueado**: Redirige a login
- **Si no es desarrollador ni admin**: Redirige al dashboard del usuario

## 📝 Ejemplos de Uso

### Antes (Con dos decoradores)
```python
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def dashboard_cliente(request):
    if not request.user.es_cliente():
        messages.error(request, 'No tienes permisos para acceder a esta área.')
        logout(request)
        return redirect('auth:login')
    
    # Lógica de la vista...
    return render(request, 'dashboard/cliente.html')
```

### Después (Con un solo decorador)
```python
from contextos.decorators import cliente_required

@cliente_required
def dashboard_cliente(request):
    # Lógica de la vista...
    return render(request, 'dashboard/cliente.html')
```

## 🎯 Casos de Uso por Contexto

### Contexto Clientes
```python
from contextos.decorators import cliente_required, cliente_or_admin_required

@cliente_required
def dashboard(request):
    # Solo clientes pueden acceder (verifica login automáticamente)
    pass

@cliente_or_admin_required
def listado_clientes(request):
    # Clientes ven sus datos, admins ven todos (verifica login automáticamente)
    pass
```

### Contexto Desarrolladores
```python
from contextos.decorators import desarrollador_required, desarrollador_or_admin_required

@desarrollador_required
def dashboard(request):
    # Solo desarrolladores pueden acceder (verifica login automáticamente)
    pass

@desarrollador_or_admin_required
def listado_desarrolladores(request):
    # Desarrolladores y admins pueden acceder (verifica login automáticamente)
    pass
```

### Contexto Backoffice
```python
from contextos.decorators import admin_required

@admin_required
def dashboard(request):
    # Solo administradores pueden acceder (verifica login automáticamente)
    pass
```

## ✅ Ventajas del Sistema

1. **Un solo decorador**: No necesitas `@login_required` + nuestro decorador
2. **Más limpio**: Menos imports y menos decoradores por vista
3. **Consistente**: Toda la lógica de autenticación/autorización en un lugar
4. **Menos errores**: Imposible olvidar agregar `@login_required`
5. **Mejor rendimiento**: Una sola verificación en lugar de dos decoradores anidados
6. **Más legible**: Un decorador indica claramente qué permisos se requieren
7. **Reutilizable**: Se puede usar en cualquier vista

## � Lógica Interna

Cada decorador sigue este flujo:

1. **Verificar autenticación**: `request.user.is_authenticated`
   - Si no está logueado → redirige a login
2. **Verificar autorización**: roles específicos (`es_cliente()`, etc.)
   - Si no tiene permisos → maneja según el tipo de error

## 🧪 Testing

Los decoradores son fáciles de testear porque:
- Cada uno tiene una responsabilidad clara
- Toda la lógica está centralizada
- Se pueden mockear fácilmente en tests unitarios
- Un solo punto de entrada por decorador

## 🚀 Extensiones Futuras

El sistema se puede extender fácilmente para:
- Permisos específicos por proyecto
- Roles más granulares
- Validaciones basadas en ownership de recursos
- Cache de permisos para mejor rendimiento
- Integración con grupos de Django

## 💡 Migración desde el Sistema Anterior

Si tenías:
```python
@login_required
@cliente_required
def vista(request):
    pass
```

Cambia a:
```python
@cliente_required
def vista(request):
    pass
```

¡Y elimina el import de `login_required`!

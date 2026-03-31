# 📚 Librería JavaScript Modular - ElProyecto

## ✨ Características

- ✅ **JavaScript Vanilla** - No requiere compilación ni bundlers
- ✅ **ES6 Modules** - Importación nativa del navegador (`import/export`)
- ✅ **Orientado a Objetos** - Clases, herencia, encapsulación
- ✅ **Reutilizable** - Componentes y clases base para todos los listados
- ✅ **Modular** - Código organizado en archivos separados

## 📂 Estructura de Archivos

```
contextos/static/js/
├── core/                          # Clases base reutilizables
│   ├── Utils.js                   # Utilidades (CSRF, mensajes, debounce)
│   ├── ApiClient.js               # Cliente HTTP con fetch
│   ├── Modal.js                   # Sistema de modales genérico
│   └── DataTable.js               # Clase base para tablas (patrón Template Method)
│
├── components/                    # Componentes UI reutilizables
│   ├── KPISection.js             # Indicadores clave con animación
│   ├── Pagination.js             # Paginación standalone
│   └── SearchFilters.js          # Búsqueda y filtros dinámicos
│
└── modules/                       # Módulos específicos
    └── usuarios/
        ├── UsuariosTable.js      # Implementación específica (extiende DataTable)
        └── usuarios-init.js      # Punto de entrada
```

## 🚀 Uso en Templates

### 1. HTML Básico

```django
{% extends 'gestion/base.html' %}
{% load static %}

{% block content %}
<div class="listado-container">
    <div class="kpis-section"></div>
    
    <div class="search-section">
        <div class="search-filters">
            <input type="text" id="filter_busqueda" placeholder="Buscar...">
        </div>
    </div>
    
    <div class="table-section">
        <table class="data-table">
            <thead>
                <tr>
                    <th class="sortable" data-field="nombre">Nombre</th>
                    <th class="sortable" data-field="email">Email</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
        <div class="pagination"></div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script type="module" src="{% static 'js/modules/usuarios/usuarios-init.js' %}"></script>
{% endblock %}
```

### 2. Crear Nueva Tabla (ej: Clientes)

```javascript
// contextos/static/js/modules/clientes/ClientesTable.js
import { DataTable } from '../../core/DataTable.js';
import { Modal } from '../../core/Modal.js';
import { Utils } from '../../core/Utils.js';

export class ClientesTable extends DataTable {
    constructor() {
        super({
            apiUrl: '/backoffice/api/clientes/',
            tableSelector: '.data-table',
            paginationSelector: '.pagination',
            searchInputSelector: '#filter_busqueda'
        });
    }

    // Método abstracto OBLIGATORIO
    buildRow(cliente) {
        return `
            <td>${cliente.id}</td>
            <td>${cliente.nombre}</td>
            <td>${cliente.email}</td>
            <td class="actions">
                <button class="btn btn-sm btn-edit" data-id="${cliente.id}">✏️</button>
                <button class="btn btn-sm btn-delete" data-id="${cliente.id}">🗑️</button>
            </td>
        `;
    }

    // Método abstracto OPCIONAL
    getFilters() {
        return {
            busqueda: document.getElementById('filter_busqueda')?.value || '',
            activo: document.getElementById('filter_activo')?.value || ''
        };
    }

    // Métodos propios
    attachRowEventListeners() {
        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', () => this.handleDelete(btn.dataset.id));
        });
    }
}

export { ClientesTable };
```

```javascript
// contextos/static/js/modules/clientes/clientes-init.js
import { ClientesTable } from './ClientesTable.js';

document.addEventListener('DOMContentLoaded', () => {
    const clientesTable = new ClientesTable();
    clientesTable.init();
    
    window.clientesTable = clientesTable; // Para debugging
});
```

## 🔧 API Requirements

Las tablas esperan una API en el backend que devuelva:

```json
{
    "success": true,
    "items": [
        {"id": 1, "nombre": "Juan", "email": "juan@example.com"},
        {"id": 2, "nombre": "Ana", "email": "ana@example.com"}
    ],
    "pagination": {
        "current_page": 1,
        "total_pages": 5,
        "total_items": 100,
        "page_size": 20,
        "has_next": true,
        "has_previous": false
    },
    "kpis": {
        "total": 100,
        "activos": 80,
        "inactivos": 20
    }
}
```

## 🎯 Clase DataTable (Base)

### Métodos Abstractos (OBLIGATORIOS)

```javascript
buildRow(item)      // Genera HTML de una fila
getFilters()        // Retorna objeto con filtros activos
```

### Métodos Heredados (YA IMPLEMENTADOS)

```javascript
init()                      // Inicializa la tabla
loadData()                  // Carga datos desde la API
updateTable(items)          // Actualiza el tbody
updatePagination(data)      // Actualiza controles de paginación
handleSort(field)           // Maneja ordenación
handleSearch()              // Maneja búsqueda
goToPage(page)             // Navega a página
setLoading(loading)         // Muestra/oculta loader
refresh()                   // Recarga datos
reset()                     // Limpia filtros y recarga
```

### Métodos Hook (OPCIONALES)

```javascript
setupCustomListeners()      // Listeners adicionales
attachRowEventListeners()   // Event listeners en filas de tabla
updateKPIs(kpis)           // Actualiza KPIs
```

## 🐛 Debugging

### 1. Agregar script de diagnóstico al template:

```django
{% block extra_js %}
<script src="{% static 'js/diagnostico.js' %}"></script>
<script type="module" src="{% static 'js/modules/usuarios/usuarios-init.js' %}"></script>
{% endblock %}
```

### 2. Verificar en la consola del navegador:

- ✅ Mensajes de inicialización
- ✅ Elementos del DOM encontrados
- ❌ Errores 404 en módulos JS
- ❌ Errores de sintaxis

### 3. Problemas Comunes

#### Error 404 al cargar módulos
```
❌ GET http://localhost:8000/static/js/modules/usuarios/usuarios-init.js 404
```

**Solución**: Verificar `STATICFILES_DIRS` en `settings.py`:
```python
STATICFILES_DIRS = [
    BASE_DIR / 'contextos' / 'static',
]
```

#### Módulo no se carga
```
❌ Failed to load module script: Expected a JavaScript module script
```

**Solución**: Verificar que el script tag tenga `type="module"`:
```html
<script type="module" src="..."></script>
```

#### Errores de import
```
❌ Uncaught SyntaxError: The requested module does not provide an export named 'Utils'
```

**Solución**: Verificar que los exports sean **named exports**:
```javascript
// ✅ CORRECTO
export { Utils };

// ❌ INCORRECTO
export default Utils;
```

#### CORS o CSRF errors en API
```
❌ Forbidden (CSRF token missing or incorrect)
```

**Solución**: Verificar que `ApiClient` incluya el token CSRF:
```javascript
headers: {
    'X-CSRFToken': Utils.getCsrfToken()
}
```

## 📝 Convenciones

### Nombre de Archivos
- **PascalCase** para clases: `DataTable.js`, `UsuariosTable.js`
- **kebab-case** para scripts: `usuarios-init.js`, `diagnostico.js`

### Exports/Imports
- **Named exports** siempre: `export { ClassName }`
- **Named imports**: `import { ClassName } from './file.js'`

### Rutas Relativas
- Desde `core/` a `core/`: `./Utils.js`
- Desde `modules/usuarios/` a `core/`: `../../core/Utils.js`
- Desde `components/` a `core/`: `../core/Utils.js`

## 🔄 Workflow de Desarrollo

1. **Backend**: Crear endpoint API en Django
2. **Modelo**: Crear clase que extienda DataTable
3. **Init**: Crear archivo init.js
4. **Template**: Agregar HTML y script tag
5. **Test**: Verificar en navegador
6. **Debug**: Usar `diagnostico.js` si hay problemas

## 📦 Sin Compilación Necesaria

Esta librería usa **JavaScript nativo del navegador** (ES6 Modules):

- ✅ No necesita Webpack, Rollup, Parcel, etc.
- ✅ No necesita npm build
- ✅ No necesita transpilación con Babel
- ✅ Funciona directamente en navegadores modernos (Chrome 61+, Firefox 60+, Safari 11+)

**Limitación**: No funciona en Internet Explorer 11 (pero nadie usa IE11 en 2026 😉)

## 📚 Recursos

- [MDN: JavaScript Modules](https://developer.mozilla.org/es/docs/Web/JavaScript/Guide/Modules)
- [MDN: Fetch API](https://developer.mozilla.org/es/docs/Web/API/Fetch_API)
- [MDN: Classes](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Classes)

---

**Última actualización**: Marzo 2026
**Versión**: 1.0.0
**Autor**: ElProyecto Dev Team

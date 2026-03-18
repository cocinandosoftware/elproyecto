# Library - Utilidades y Scripts de ElProyecto

Esta carpeta contiene scripts y utilidades auxiliares para el proyecto.

## 📂 Contenido

### `generar_usuarios.py`

Script para generar usuarios masivos (clientes y desarrolladores) con datos realistas para testing y desarrollo.

## 🚀 Uso

### Opción 1: Desde Django Shell

```bash
python manage.py shell
```

```python
from library.generar_usuarios import generar_usuarios_masivos

# Generar 80 clientes y 70 desarrolladores (150 usuarios totales)
resultado = generar_usuarios_masivos(num_clientes=80, num_desarrolladores=70)

# Generar cantidades personalizadas
resultado = generar_usuarios_masivos(num_clientes=100, num_desarrolladores=50)
```

### Opción 2: Ejecución Directa

```bash
# Generar 80 clientes y 70 desarrolladores (por defecto)
python library/generar_usuarios.py

# Generar cantidades personalizadas
python library/generar_usuarios.py 100 50  # 100 clientes, 50 desarrolladores
```

### Opción 3: Comando Django (Recomendado)

```bash
# Generar usuarios con cantidades por defecto
python manage.py generar_usuarios

# Generar cantidades personalizadas
python manage.py generar_usuarios --clientes 100 --desarrolladores 50

# Ver ayuda
python manage.py generar_usuarios --help
```

## 📊 Datos Generados

### Clientes
- **Username**: Variaciones de nombre y apellido + número único
- **Email**: Basado en nombre y apellido con dominios realistas
- **Password**: `cliente123` (todos los clientes)
- **Empresa**: Nombre de empresa realista generado automáticamente
- **NIF**: Generado aleatoriamente
- **Teléfono**: Número español realista (móvil o fijo)
- **Facturación**: Entre 1.000€ y 50.000€

### Desarrolladores
- **Username**: Variaciones de nombre y apellido + número único
- **Email**: Basado en nombre y apellido con dominios realistas
- **Password**: `dev123` (todos los desarrolladores)
- **Perfil**: Frontend, Backend, Full Stack, DevOps, QA, Mobile, etc.
- **Teléfono**: Número español realista

## 🔒 Contraseñas por Defecto

- **Clientes**: `cliente123`
- **Desarrolladores**: `dev123`

## 🧹 Limpieza

Para eliminar los usuarios generados masivamente:

```bash
python library/generar_usuarios.py limpiar
```

O desde el shell:

```python
from library.generar_usuarios import limpiar_usuarios_generados
limpiar_usuarios_generados()
```

⚠️ **ADVERTENCIA**: Esta operación es irreversible. Solo elimina usuarios con usernames que contengan números >= 1000.

## 📝 Ejemplos de Uso

### Generar 150 usuarios para testing

```python
from library.generar_usuarios import generar_usuarios_masivos

resultado = generar_usuarios_masivos(
    num_clientes=80, 
    num_desarrolladores=70,
    verbose=True  # Mostrar información detallada
)

print(f"Total usuarios creados: {resultado['total']}")
print(f"Tiempo de ejecución: {resultado['duracion']:.2f} segundos")
```

### Generar solo clientes

```python
resultado = generar_usuarios_masivos(num_clientes=100, num_desarrolladores=0)
```

### Generar solo desarrolladores

```python
resultado = generar_usuarios_masivos(num_clientes=0, num_desarrolladores=100)
```

## ✅ Características

- ✨ Datos realistas (nombres españoles, empresas, NIFs, teléfonos)
- 🔐 Validación de unicidad (usernames y emails únicos)
- 🎯 Transacciones atómicas (rollback automático en caso de error)
- 📊 Progress bar durante la generación
- 🚀 Alto rendimiento (genera ~150 usuarios en pocos segundos)
- 🔄 Asociación automática (Cliente/Desarrollador ↔ Usuario)
- 📝 Logs detallados del proceso

## 🛠️ Estructura de Datos

El script genera:

1. **Cliente** → Tabla `core_cliente`
   - Empresa con nombre realista
   - Datos de contacto completos
   - NIF y facturación simulada

2. **Desarrollador** → Tabla `core_desarrollador`
   - Perfil profesional asignado
   - Datos personales completos

3. **Usuario** → Tabla `core_usuario`
   - Asociado a Cliente o Desarrollador
   - Credenciales de acceso
   - Tipo de usuario configurado

## 📦 Dependencias

No requiere dependencias adicionales. Usa solo la biblioteca estándar de Python y Django.

## 🎯 Casos de Uso

- Testing de paginación con volumen de datos
- Pruebas de rendimiento de listados
- Desarrollo de funcionalidades de búsqueda y filtrado
- Demostración del sistema con datos realistas
- Pruebas de carga y stress testing

## 💡 Tips

1. **Primera ejecución**: Genera al menos 150 usuarios para tener un volumen representativo
2. **Entornos**: Solo usar en desarrollo, NUNCA en producción
3. **Limpieza periódica**: Usa la función de limpieza después de las pruebas
4. **Combinación**: Puedes ejecutar el script múltiples veces para acumular más usuarios
5. **Variación**: Los datos son aleatorios, cada ejecución genera usuarios diferentes

## 🐛 Troubleshooting

### Error: "module not found"
Asegúrate de estar en el directorio raíz del proyecto y que el entorno virtual esté activado.

### Error: "username already exists"
El script maneja automáticamente esto incrementando el número. Si persiste, ajusta los números de inicio en el código.

### Usuarios no aparecen en el admin
Verifica que:
- Las migraciones estén aplicadas: `python manage.py migrate`
- Los modelos estén registrados en admin.py
- El usuario admin tenga permisos para ver los registros


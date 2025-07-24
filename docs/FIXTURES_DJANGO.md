# 📊 Guía Completa: Fixtures en Django - Datos Iniciales

## 📋 Índice
1. [¿Qué son las Fixtures?](#qué-son-las-fixtures)
2. [Estructura de un Archivo Fixture](#estructura-de-un-archivo-fixture)
3. [Creando Fixtures](#creando-fixtures)
4. [Cargando Datos](#cargando-datos)
5. [Exportando Datos](#exportando-datos)
6. [Comandos Esenciales](#comandos-esenciales)
7. [Ejemplo Práctico Completo](#ejemplo-práctico-completo)

---

## 🤔 ¿Qué son las Fixtures?

Las **fixtures** son archivos que contienen datos serializados para poblar la base de datos con información inicial. Son muy útiles para:

### 🎯 Casos de Uso
- **Datos de prueba**: Para desarrollo y testing
- **Datos iniciales**: Usuarios admin, categorías básicas, configuraciones
- **Datos de demostración**: Para mostrar la aplicación funcionando
- **Migración de datos**: Transferir datos entre entornos
- **Backup de datos**: Respaldo de información crítica

### ✅ Ventajas
- **Reproducibles**: Mismos datos en todos los entornos
- **Versionables**: Se pueden versionar con Git
- **Automatizables**: Se pueden cargar en scripts de despliegue
- **Portables**: Funcionan en cualquier base de datos compatible

---

## 📄 Estructura de un Archivo Fixture

### Formato JSON (Recomendado)
```json
[
  {
    "model": "nombre_app.modelo",
    "pk": 1,
    "fields": {
      "campo1": "valor1",
      "campo2": "valor2"
    }
  }
]
```

### Anatomía de una Fixture
- **model**: `app_name.modelo` (nombre de la aplicación + modelo)
- **pk**: Clave primaria (primary key) - ID único
- **fields**: Diccionario con los campos del modelo y sus valores

### Otros Formatos Soportados
- **XML**: Menos común pero soportado
- **YAML**: Más legible pero requiere PyYAML

---

## 🔧 Creando Fixtures

### 1. Estructura de Directorios
```
mi_app/
├── fixtures/              # Directorio para fixtures
│   ├── datos_iniciales.json
│   ├── usuarios_prueba.json
│   └── configuracion.json
├── models.py
└── ...
```

### 2. Ubicaciones donde Django busca fixtures:
1. `mi_app/fixtures/`
2. `mi_app/`
3. Directorios especificados en `FIXTURE_DIRS` en settings.py

### 3. Ejemplo: Modelo Ciudad
```python
# models.py
class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre}, {self.pais}"
```

### 4. Fixture para el Modelo Ciudad
```json
[
  {
    "model": "web.ciudad",
    "pk": 1,
    "fields": {
      "nombre": "Madrid",
      "pais": "España"
    }
  },
  {
    "model": "web.ciudad",
    "pk": 2,
    "fields": {
      "nombre": "Barcelona",
      "pais": "España"
    }
  }
]
```

---

## 📥 Cargando Datos

### Comando Principal
```bash
python manage.py loaddata nombre_fixture
```

### Ejemplos Específicos
```bash
# Cargar fixture específica
python manage.py loaddata ciudades_iniciales

# Cargar múltiples fixtures
python manage.py loaddata ciudades usuarios configuracion

# Cargar con ruta específica
python manage.py loaddata mi_app/fixtures/datos.json

# Cargar con verbose (más información)
python manage.py loaddata ciudades_iniciales --verbosity=2
```

### ¿Qué hace loaddata?
1. **Busca** el archivo en los directorios de fixtures
2. **Lee** el archivo (JSON, XML, YAML)
3. **Crea** los objetos en la base de datos
4. **Reporta** cuántos objetos se instalaron

### Salida típica:
```bash
$ python manage.py loaddata ciudades_iniciales
Installed 20 object(s) from 1 fixture(s)
```

---

## 📤 Exportando Datos

### Comando dumpdata
```bash
python manage.py dumpdata app_name.modelo > archivo.json
```

### Ejemplos de Exportación
```bash
# Exportar todas las ciudades
python manage.py dumpdata web.ciudad > ciudades_backup.json

# Exportar con formato legible
python manage.py dumpdata web.ciudad --indent 2 > ciudades_formato.json

# Exportar toda una aplicación
python manage.py dumpdata web > web_completa.json

# Exportar excluyendo ciertos modelos
python manage.py dumpdata --exclude auth.permission > datos_sin_permisos.json

# Exportar solo campos específicos
python manage.py dumpdata web.ciudad --fields nombre,pais > ciudades_simple.json
```

---

## 🛠️ Comandos Esenciales

### Cargar Datos
```bash
# Básico
python manage.py loaddata mi_fixture

# Con información detallada
python manage.py loaddata mi_fixture --verbosity=2

# Ignorar errores de clave primaria duplicada
python manage.py loaddata mi_fixture --ignore-duplication

# Cargar en una base de datos específica
python manage.py loaddata mi_fixture --database=mi_db
```

### Exportar Datos
```bash
# Exportar modelo específico
python manage.py dumpdata app.modelo > backup.json

# Con formato bonito
python manage.py dumpdata app.modelo --indent 2 > backup_formato.json

# Sin tipos de contenido y permisos (más limpio)
python manage.py dumpdata --exclude contenttypes --exclude auth.permission > datos_limpios.json

# Datos naturales (usa campos naturales como identificadores)
python manage.py dumpdata --natural-foreign --natural-primary > datos_naturales.json
```

### Verificar Datos
```bash
# Usar shell para verificar
python manage.py shell -c "from mi_app.models import MiModelo; print(MiModelo.objects.count())"

# Listar algunos objetos
python manage.py shell -c "from mi_app.models import MiModelo; [print(obj) for obj in MiModelo.objects.all()[:5]]"
```

---

## 💻 Ejemplo Práctico Completo

### 1. El Modelo
```python
# web/models.py
from django.db import models

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    poblacion = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre}, {self.pais}"
    
    class Meta:
        verbose_name_plural = "Ciudades"
```

### 2. Crear el Directorio
```bash
mkdir -p web/fixtures
```

### 3. Crear la Fixture
```json
# web/fixtures/ciudades_iniciales.json
[
  {
    "model": "web.ciudad",
    "pk": 1,
    "fields": {
      "nombre": "Madrid",
      "pais": "España",
      "poblacion": 3223000
    }
  },
  {
    "model": "web.ciudad",
    "pk": 2,
    "fields": {
      "nombre": "Barcelona",
      "pais": "España",
      "poblacion": 1620000
    }
  },
  {
    "model": "web.ciudad",
    "pk": 3,
    "fields": {
      "nombre": "París",
      "pais": "Francia",
      "poblacion": 2140000
    }
  }
]
```

### 4. Hacer las Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Cargar los Datos
```bash
python manage.py loaddata ciudades_iniciales
```
**Resultado esperado:**
```
Installed 3 object(s) from 1 fixture(s)
```

### 6. Verificar los Datos
```bash
python manage.py shell
```
```python
>>> from web.models import Ciudad
>>> Ciudad.objects.count()
3
>>> for ciudad in Ciudad.objects.all():
...     print(ciudad)
Madrid, España
Barcelona, España
París, Francia
```

### 7. Agregar Más Datos y Exportar
```bash
# Después de agregar más ciudades manualmente...
python manage.py dumpdata web.ciudad --indent 2 > web/fixtures/ciudades_completas.json
```

---

## 🔄 Flujo de Trabajo con Fixtures

### Desarrollo Local
1. **Crear modelos** y hacer migraciones
2. **Agregar datos** manualmente o por admin
3. **Exportar fixtures** con `dumpdata`
4. **Versionar** las fixtures en Git

### Testing
1. **Cargar fixtures** en tests automáticos
2. **Tener datos** consistentes para pruebas
3. **Limpiar datos** entre tests

### Despliegue
1. **Subir código** nuevo
2. **Hacer migraciones**
3. **Cargar fixtures** de datos iniciales
4. **Verificar** que todo funcione

---

## ⚠️ Buenas Prácticas

### ✅ Qué Hacer
- **Usar nombres descriptivos** para las fixtures
- **Mantener fixtures pequeñas** y específicas
- **Versionar fixtures** en control de versiones
- **Documentar** qué hace cada fixture
- **Usar claves primarias** explícitas
- **Testear fixtures** regularmente

### ❌ Qué Evitar
- **No hardcodear IDs** que cambien entre entornos
- **No incluir datos sensibles** (contraseñas, tokens)
- **No hacer fixtures gigantes** (divide en archivos)
- **No depender de fixtures** para datos críticos de producción

### 🔒 Datos Sensibles
```python
# En lugar de hardcodear contraseñas:
{
  "model": "auth.user",
  "fields": {
    "username": "admin",
    "password": "pbkdf2_sha256$..."  # Hash, no texto plano
  }
}

# Mejor usar management commands para crear usuarios:
# python manage.py createsuperuser
```

---

## 🐛 Debugging de Fixtures

### Errores Comunes

#### Error: "No such file or directory"
```bash
# Django no encuentra la fixture
# Solución: Verificar nombre y ubicación
python manage.py loaddata ciudades_iniciales --verbosity=2
```

#### Error: "IntegrityError"
```bash
# Clave primaria duplicada
# Solución: Verificar que los IDs no existan ya
python manage.py loaddata ciudades --ignore-duplication
```

#### Error: "DoesNotExist"
```bash
# Referencia a objeto que no existe (ForeignKey)
# Solución: Cargar las dependencias primero
python manage.py loaddata categorias
python manage.py loaddata productos  # Depende de categorias
```

### Verificación Manual
```bash
# Ver qué fixtures encuentra Django
python manage.py loaddata --help

# Ver estructura de la base de datos
python manage.py dbshell
.tables
.schema web_ciudad
```

---

## 📚 Fixtures Avanzadas

### Relaciones ForeignKey
```json
[
  {
    "model": "web.pais",
    "pk": 1,
    "fields": {
      "nombre": "España",
      "codigo": "ES"
    }
  },
  {
    "model": "web.ciudad",
    "pk": 1,
    "fields": {
      "nombre": "Madrid",
      "pais": 1  # Referencia al país con pk=1
    }
  }
]
```

### Fechas y Timestamps
```json
{
  "model": "web.evento",
  "pk": 1,
  "fields": {
    "nombre": "Conferencia Django",
    "fecha": "2025-07-24T10:00:00Z",  # Formato ISO
    "fecha_creacion": "2025-01-01T00:00:00Z"
  }
}
```

### Usando Natural Keys
```python
# En el modelo
class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=3, unique=True)
    
    def natural_key(self):
        return (self.codigo,)
```

```json
{
  "model": "web.ciudad",
  "fields": {
    "nombre": "Madrid",
    "pais": ["ES"]  # Usa natural key en lugar de pk
  }
}
```

---

## 🎯 Resumen de Comandos Clave

```bash
# Crear fixtures
python manage.py dumpdata app.modelo --indent 2 > fixtures/datos.json

# Cargar fixtures
python manage.py loaddata datos

# Verificar datos
python manage.py shell -c "from app.models import Modelo; print(Modelo.objects.count())"

# Exportar toda la app
python manage.py dumpdata app > backup_app.json

# Cargar con información detallada
python manage.py loaddata datos --verbosity=2
```

---

*✨ ¡Con esta guía dominarás las fixtures en Django! Recuerda que son fundamentales para tener datos consistentes en todos tus entornos.*

# 🐍 Guía Completa: Comandos Django desde Cero

## 📋 Índice
1. [Preparación del Entorno](#preparación-del-entorno)
2. [Instalación de Django](#instalación-de-django)
3. [Creación del Proyecto](#creación-del-proyecto)
4. [Configuración Inicial](#configuración-inicial)
5. [Ejecución del Servidor](#ejecución-del-servidor)
6. [Comandos Adicionales Útiles](#comandos-adicionales-útiles)

---

## 🚀 Preparación del Entorno

### 1. Verificar Python
```bash
python3 --version
```
**¿Qué hace?** Verifica que Python 3 esté instalado en tu sistema.
**¿Por qué lo necesita Django?** Django está construido en Python y requiere Python 3.8 o superior.

### 2. Crear entorno virtual
```bash
python3 -m venv venv
```
**¿Qué hace?** Crea un entorno virtual llamado "venv" en tu directorio actual.
**¿Por qué es importante?** 
- Aísla las dependencias del proyecto
- Evita conflictos entre diferentes versiones de paquetes
- Mantiene tu sistema Python limpio
- Permite tener diferentes versiones de Django para diferentes proyectos

### 3. Activar entorno virtual
```bash
source venv/bin/activate
```
**¿Qué hace?** Activa el entorno virtual creado anteriormente.
**¿Cómo sabes que está activo?** Verás `(venv)` al inicio de tu línea de comandos.
**¿Por qué activarlo?** Para que todas las instalaciones y comandos se ejecuten dentro del entorno aislado.

### 3.1. Desactivar entorno virtual
```bash
deactivate
```

### 4. Actualizar pip
```bash
pip install --upgrade pip
```
**¿Qué hace?** Actualiza pip (el gestor de paquetes de Python) a la última versión.
**¿Por qué?** Versiones más recientes de pip son más rápidas y seguras para instalar paquetes.

---

## 📦 Instalación de Django

### 5. Instalar Django
```bash
pip install django
```
**¿Qué hace?** Instala la última versión estable de Django (en nuestro caso 4.2.23).
**¿Qué se instala junto con Django?**
- `asgiref`: Para manejo de aplicaciones asíncronas
- `sqlparse`: Para análisis de consultas SQL
- `typing_extensions`: Para mejor tipado en Python

---

## 🏗️ Creación del Proyecto

### 6. Crear proyecto Django
```bash
django-admin startproject elproyecto .
```
**¿Qué hace?** Crea un nuevo proyecto Django llamado "elproyecto" en el directorio actual (el punto final).
**¿Qué archivos crea?**
- `manage.py`: Script principal para administrar el proyecto
- `elproyecto/settings.py`: Configuraciones del proyecto
- `elproyecto/urls.py`: Configuración de URLs principales
- `elproyecto/wsgi.py`: Para despliegue en servidores WSGI
- `elproyecto/asgi.py`: Para despliegue en servidores ASGI

### 7. Crear aplicación Django
```bash
python manage.py startapp hello
```
**¿Qué hace?** Crea una nueva aplicación llamada "hello" dentro del proyecto.
**¿Diferencia entre proyecto y aplicación?**
- **Proyecto**: El sitio web completo con todas sus configuraciones
- **Aplicación**: Una parte específica del sitio (blog, tienda, usuarios, etc.)

**¿Qué archivos crea para la app?**
- `views.py`: Lógica de las vistas (controladores)
- `models.py`: Modelos de datos (base de datos)
- `admin.py`: Configuración del panel de administración
- `apps.py`: Configuración de la aplicación
- `tests.py`: Pruebas unitarias
- `migrations/`: Carpeta para migraciones de base de datos

---

## ⚙️ Configuración Inicial

### 8. Aplicar migraciones iniciales
```bash
python manage.py migrate
```
**¿Qué hace?** Aplica las migraciones iniciales de Django a la base de datos.
**¿Qué migraciones aplica?**
- Tablas para el sistema de autenticación (`auth`)
- Tablas para el panel de administración (`admin`)
- Tablas para tipos de contenido (`contenttypes`)
- Tablas para sesiones de usuario (`sessions`)

**¿Por qué es necesario?** Django necesita estas tablas básicas para funcionar correctamente.

---

## 🌐 Ejecución del Servidor

### 9. Ejecutar servidor de desarrollo
```bash
python manage.py runserver 8001
```
**¿Qué hace?** Inicia el servidor de desarrollo de Django en `http://127.0.0.1:8000/`
**¿Es para producción?** ¡NO! Solo para desarrollo. Para producción se usan servidores como Gunicorn, uWSGI, etc.

### 10. Ejecutar en puerto específico
```bash
python manage.py runserver 8080
```
**¿Qué hace?** Ejecuta el servidor en el puerto 8080 en lugar del 8000 por defecto.

---

## 🛠️ Comandos Adicionales Útiles

### Gestión de Archivos Estáticos

#### Recopilar archivos estáticos
```bash
python manage.py collectstatic
```
**¿Qué hace?** Recopila todos los archivos estáticos (CSS, JS, imágenes) de todas las aplicaciones y los coloca en un solo directorio.
**¿Cuándo usarlo?** 
- Antes de desplegar en producción
- Cuando quieres servir archivos estáticos desde un servidor web (nginx, Apache)
- Para optimizar la entrega de archivos estáticos

#### Recopilar sin confirmación
```bash
python manage.py collectstatic --noinput
```
**¿Qué hace?** Igual que el anterior pero sin preguntar confirmación para sobrescribir archivos.

#### Limpiar archivos estáticos
```bash
python manage.py collectstatic --clear --noinput
```
**¿Qué hace?** Elimina todos los archivos del directorio STATIC_ROOT antes de copiar los nuevos.

### Gestión de la Base de Datos

#### Crear migraciones
```bash
python manage.py makemigrations
```
**¿Cuándo usarlo?** Después de modificar los modelos en `models.py`
**¿Qué hace?** Crea archivos de migración basados en los cambios en tus modelos.

#### Ver migraciones pendientes
```bash
python manage.py showmigrations
```
**¿Qué hace?** Muestra qué migraciones están aplicadas y cuáles están pendientes.

#### Migración específica
```bash
python manage.py migrate nombre_app numero_migracion
```
**¿Cuándo usarlo?** Para aplicar o revertir a una migración específica.

### Gestión de Usuarios

#### Crear superusuario
```bash
python manage.py createsuperuser
```
**¿Qué hace?** Crea un usuario administrador para acceder al panel de admin en `/admin/`

### Herramientas de Desarrollo

#### Shell interactivo de Django
```bash
python manage.py shell
```
**¿Qué hace?** Abre un shell de Python con el contexto de Django cargado.
**¿Para qué sirve?** Probar modelos, consultas, y código Django interactivamente.

#### Recopilar archivos estáticos
```bash
python manage.py collectstatic
```
**¿Cuándo usarlo?** Antes de desplegar en producción para reunir todos los CSS, JS, imágenes.

#### Verificar el proyecto
```bash
python manage.py check
```
**¿Qué hace?** Verifica si hay problemas en la configuración del proyecto.

---

## 📁 Estructura de Archivos Creada

```
elproyecto/
├── venv/                 # Entorno virtual
├── elproyecto/          # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py      # Configuraciones principales
│   ├── urls.py          # URLs principales
│   ├── wsgi.py          # Para servidores WSGI
│   └── asgi.py          # Para servidores ASGI
├── hello/               # Aplicación Django
│   ├── migrations/      # Migraciones de la app
│   ├── __init__.py
│   ├── admin.py         # Configuración del admin
│   ├── apps.py          # Configuración de la app
│   ├── models.py        # Modelos de datos
│   ├── tests.py         # Pruebas
│   ├── views.py         # Vistas (lógica)
│   └── urls.py          # URLs de la app (creado manualmente)
├── manage.py            # Script de administración
└── db.sqlite3           # Base de datos SQLite (se crea automáticamente)
```

---

## 🔄 Flujo de Trabajo Típico

1. **Activar entorno virtual**: `source venv/bin/activate`
2. **Hacer cambios en el código**
3. **Crear migraciones** (si cambias modelos): `python manage.py makemigrations`
4. **Aplicar migraciones**: `python manage.py migrate`
5. **Ejecutar servidor**: `python manage.py runserver`
6. **Probar en el navegador**: `http://127.0.0.1:8000/`

---

## ⚠️ Comandos de Emergencia

### Resetear base de datos
```bash
rm db.sqlite3
python manage.py migrate
```
**¿Cuándo usarlo?** Si la base de datos se corrompe o quieres empezar de cero.

### Desactivar entorno virtual
```bash
deactivate
```
**¿Qué hace?** Desactiva el entorno virtual actual.

### Ver versión de Django
```bash
python -m django --version
```
**¿Qué hace?** Muestra la versión de Django instalada.

---

## 📚 Recursos Adicionales

- **Documentación oficial**: https://docs.djangoproject.com/
- **Tutorial oficial**: https://docs.djangoproject.com/en/4.2/intro/tutorial01/
- **Django Girls Tutorial**: https://tutorial.djangogirls.org/

---

## 💡 Consejos Importantes

1. **Siempre activa el entorno virtual** antes de trabajar
2. **Nunca hagas `pip install` sin el entorno virtual activo**
3. **Guarda tu `requirements.txt`**: `pip freeze > requirements.txt`
4. **El servidor de desarrollo se reinicia automáticamente** cuando cambias código
5. **Para salir del servidor** presiona `Ctrl+C`

---

*✨ ¡Recuerda: La práctica hace al maestro! Prueba estos comandos y experimenta con Django.*



# ElProyecto 🚀

**Cocinando Software** - El entorno para que clientes y desarrolladores cocinen sus proyectos

[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📝 Descripción

ElProyecto es una plataforma web que actúa como intermediaria entre clientes y desarrolladores, eliminando las ineficiencias de comunicación que surgen durante el desarrollo de software. Proporciona un entorno común donde ambas partes pueden estructurar proyectos, hacer seguimiento de su evolución y garantizar una comunicación fluida basada en una metodología clara.

### 🎯 El Problema que Resolvemos

- **Clientes** que no saben cómo pedir lo que necesitan
- **Desarrolladores** que reciben proyectos mal definidos o sin contexto
- Pérdida de tiempo y dinero en malentendidos y desarrollos ineficaces
- Falta de seguimiento claro de tareas, fases, entregables y decisiones
- Dificultad para generar confianza mutua entre cliente y proveedor

### 🎯 Nuestra Solución

Una plataforma que permite hablar el mismo idioma a ambos lados del desarrollo. Los proyectos se definen con claridad, los roles y responsables están identificados, y las decisiones y tareas quedan documentadas.

## 👥 Audiencia Objetivo

### Clientes
- Empresas que contratan desarrolladores freelance o equipos externos
- Personas no técnicas que necesitan desarrollar software sin saber cómo gestionarlo

### Desarrolladores
- Freelance que trabajan para varios clientes
- Equipos de desarrollo que quieren estandarizar la toma de requisitos y la relación con clientes

## 🛠️ Tecnologías

- **Backend**: Django (Python)
- **Frontend**: JavaScript Vanilla
- **Base de Datos**: SQLite (desarrollo) → PostgreSQL (producción)
- **Autenticación**: Sistema de roles integrado

## ✨ Características Principales

### 👨‍💻 Área de Desarrolladores
- **Gestión de Proyectos**: Listado completo con estados y fichas detalladas
- **Gestión de Clientes**: Listado de clientes y proyectos vinculados
- **Historias de Usuario**: Categorización y seguimiento completo
- **Gestión de Tareas**: Control de implementación con fechas límite y responsables

### 👤 Área de Clientes
- **Gestión de Proyectos**: Vista completa de proyectos y su progreso
- **Gestión de Proveedores**: Listado de desarrolladores y proyectos asociados
- **Historias de Usuario**: Creación con descripciones, imágenes y criterios de aceptación
- **Seguimiento de Tareas**: Visibilidad completa del progreso de desarrollo

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- GitHub (Control de versiones)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/cocinandosoftware/elproyecto.git
   cd elproyecto
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**
   ```bash
   python manage.py migrate
   ```

5. **Crear datos de prueba (opcional)**
   ```bash
   python manage.py crear_semilla
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

8. **Acceder a la aplicación**
   - Aplicación: http://127.0.0.1:8000/
   - Panel de administración: http://127.0.0.1:8000/admin/


## 📁 Estructura del Proyecto

```
elproyecto/
├── contextos/              # Contextos de la aplicación
│   ├── backoffice/        # Área administrativa
│   ├── clientes/          # Gestión de clientes
│   └── desarrolladores/   # Gestión de desarrolladores
├── core/                  # Modelos y lógica central
│   ├── clientes/         # Modelos de cliente
│   ├── proyectos/        # Modelos de proyecto
│   ├── usuarios/         # Modelos de usuario
│   └── management/       # Comandos personalizados
├── templates/            # Plantillas HTML
│   ├── auth/            # Autenticación
│   ├── backoffice/      # Panel administrativo
│   ├── clientes/        # Vistas de cliente
│   ├── desarrolladores/ # Vistas de desarrollador
│   └── dashboard/       # Dashboards por rol
├── web/                 # Aplicación web principal
├── docs/                # Documentación del proyecto
└── manage.py           # Script de gestión de Django
```

## 🗺️ Roadmap de Desarrollo

### ✅ Fase 1: Fundamentos (Completado)
- [x] Estructura base del proyecto Django
- [x] Sistema de autenticación y roles
- [x] Modelos básicos (Usuario, Cliente, Proyecto)
- [x] Panel de administración Django
- [x] Plantillas base y navegación

### 🚧 Fase 2: Funcionalidades Core (En Desarrollo)
- [ ] Creacion de un Readme.md inicial
- [ ] Control de acceso a los contextos haciendo uso de decoradores
- [ ] Diagrama inicial de nuestra base de datos para seguimiento futuro
- [ ] Sistema CRM con listados y filtros
- [ ] Gestión completa de proyectos
- [ ] Dashboard diferenciado por roles
- [ ] Sistema de invitaciones entre usuarios
- [ ] Gestión de historias de usuario

### 📋 Fase 3: Colaboración Avanzada (Planificado)
- [ ] Sistema de tareas y seguimiento
- [ ] Notificaciones en tiempo real
- [ ] Sistema de comentarios y comunicación
- [ ] Gestión de archivos y documentos
- [ ] Reportes y métricas de proyecto

### 🚀 Fase 4: Producción (Futuro)
- [ ] Optimización para móviles
- [ ] Integración continua (CI/CD)
- [ ] Despliegue en servidor dedicado
- [ ] Sistema de backups
- [ ] Monitorización y logging

## 📚 Documentación

Para más información detallada, consulta:

### 📋 Documentación del Proyecto
- [Comandos Django](docs/COMANDOS_DJANGO.md)
- [Comandos del Proyecto](docs/COMANDOS_PROYECTO.md)
- [Datos Semilla](docs/DATOS_SEMILLA.md)
- [Sistema de Autenticación](docs/SISTEMA_AUTENTICACION.md)
- [Archivos Estáticos](docs/ARCHIVOS_ESTATICOS.md)
- [Login en areas privadas] (dev_lucia / dev123 - cliente_laura / cliente123)

### 🎥 Contenido Educativo
- **Canal YouTube**: @CocinandoSoftware
- **Commits**: Cada sesión tiene commits detallados con explicaciones
- **Tags Git**: Navegación fácil entre sesiones (`v1.1`, `v1.2`, etc.)

## 🎥 Siguiendo el Desarrollo en Vivo

Este proyecto se desarrolla de forma **pública y documentada** a través del canal **@CocinandoSoftware** con sesiones de 45 minutos grabadas y publicadas en YouTube.

### 📺 Cómo Seguir el Curso

1. **YouTube**: Sesiones completas de desarrollo en tiempo real
2. **GitHub**: Código fuente actualizado después de cada sesión
3. **Tags de Git**: Cada sesión tiene su tag correspondiente (`v1.1`, `v1.2`, etc.)

### 🏷️ Navegación por Sesiones

Para ver el código en un momento específico del curso:

```bash
# Ver todas las sesiones disponibles
git tag

# Cambiar al código de una sesión específica
git checkout v1.5  # Ejemplo: Sesión 5

# Volver a la versión más reciente
git checkout main

# Ver los cambios de una sesión específica
git log --oneline v1.4..v1.5
```


### 📚 Sesiones Realizadas

- **Sesión 1**: Idea y definición del proyecto → `v1.1` | [📺 Ver en YouTube](#)
- **Sesión 2**: Experimentando con la IA → `v1.2` | [📺 Ver en YouTube](#)
- **Sesión 3**: Primer HelloWorld → `v1.3` | [📺 Ver en YouTube](#)
- **Sesión 4**: HelloWorld otra vez + render y DB → `v1.4` | [📺 Ver en YouTube](#)
- **Sesión 5**: Nuestro primer módulo funcional - Clientes → `v1.5` | [📺 Ver en YouTube](#)
- **Sesión 6**: Contextos + Core → `v1.6` | [📺 Ver en YouTube](#)
- **Sesión 7**: Autenticación y acceso a los contextos (desastre IA) → `v1.7` | [📺 Ver en YouTube](#)
- **Sesión 8**: Autenticación y acceso a los contextos (final) → `v1.8` | [📺 Ver en YouTube](#)

> 💡 **Tip**: Usa `git log --oneline v1.X..v1.Y` para ver los commits entre sesiones específicas.

## 🤝 Metodología de Desarrollo

Esta metodología educativa permite que:
- Otros desarrolladores aprendan del proceso real de desarrollo
- Los clientes entiendan cómo se construye software de calidad desde cero
- La comunidad pueda hacer aportaciones y sugerencias
- Se documente cada decisión técnica tomada

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres colaborar:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

**Cocinando Software**
- Canal: @CocinandoSoftware
- Proyecto: [ElProyecto](https://github.com/cocinandosoftware/elproyecto)

---

⭐ Si este proyecto te resulta útil, ¡no olvides darle una estrella!


## Uso de SCSS 
- Configuración en package.json
```bash
npm run sass:watch
```
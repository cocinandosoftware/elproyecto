# 🌱 Datos de Semilla - Sistema de Autenticación

## 📊 Datos Creados

El sistema ahora tiene datos de prueba completos para testear todas las funcionalidades:

### 🏢 **5 Empresas Cliente**
- **TechInno** (Tecnologías Innovadoras S.L.)
- **WebPro** (Desarrollo Web Profesional S.A.)
- **DigitalStart** (Startup Digital Solutions)
- **EcomGlobal** (E-Commerce Global S.L.)
- **FintechInn** (Fintech Innovations S.A.)

### 👥 **5 Usuarios Cliente**
Cada usuario está asociado a una empresa:

| Usuario | Nombre | Email | Empresa | Password |
|---------|--------|-------|---------|----------|
| `cliente_maria` | María García | maria.garcia@techinno.es | TechInno | `cliente123` |
| `cliente_carlos` | Carlos Rodríguez | carlos.rodriguez@webpro.es | WebPro | `cliente123` |
| `cliente_ana` | Ana Martínez | ana.martinez@digitalstart.es | DigitalStart | `cliente123` |
| `cliente_pedro` | Pedro López | pedro.lopez@ecomglobal.es | EcomGlobal | `cliente123` |
| `cliente_laura` | Laura Sánchez | laura.sanchez@fintechinn.es | FintechInn | `cliente123` |

### 💻 **6 Usuarios Desarrollador**

| Usuario | Nombre | Email | Password |
|---------|--------|-------|----------|
| `dev_alberto` | Alberto Fernández | alberto.dev@cocinandosoftware.es | `dev123` |
| `dev_sofia` | Sofía González | sofia.dev@cocinandosoftware.es | `dev123` |
| `dev_miguel` | Miguel Ruiz | miguel.dev@cocinandosoftware.es | `dev123` |
| `dev_elena` | Elena Torres | elena.dev@cocinandosoftware.es | `dev123` |
| `dev_javier` | Javier Moreno | javier.dev@cocinandosoftware.es | `dev123` |
| `dev_lucia` | Lucía Jiménez | lucia.dev@cocinandosoftware.es | `dev123` |

### 🚀 **8 Proyectos de Ejemplo**
- Plataforma E-commerce
- App Móvil Fintech
- Sistema de Gestión CRM
- Portal Web Corporativo
- API REST Microservicios
- Dashboard Analytics
- Sistema de Facturación
- Marketplace Digital

## 🧪 Guía de Pruebas

### 1. **Probar Dashboard de Cliente**
```bash
# Ve a: http://127.0.0.1:8000/login/
Usuario: cliente_maria
Password: cliente123
```
**Resultado esperado:**
- Redirige a dashboard de cliente
- Muestra información de la empresa TechInno
- Muestra cards específicas para clientes
- Botón de logout funcional

### 2. **Probar Dashboard de Desarrollador**
```bash
# Ve a: http://127.0.0.1:8000/login/
Usuario: dev_sofia
Password: dev123
```
**Resultado esperado:**
- Redirige a dashboard de desarrollador (verde)
- Muestra herramientas para desarrolladores
- Cards específicas para gestión de proyectos
- Estadísticas de rendimiento

### 3. **Probar Dashboard de Admin**
```bash
# Ve a: http://127.0.0.1:8000/login/
Usuario: admin
Password: (tu contraseña)
```
**Resultado esperado:**
- Redirige a dashboard de backoffice (rojo)
- Muestra estadísticas globales del sistema
- Botón directo al panel admin
- Gestión completa del sistema

### 4. **Probar Restricciones de Acceso**

#### Cliente intentando acceder a desarrolladores:
```
http://127.0.0.1:8000/desarrolladores/
```
**Resultado:** Mensaje de error y redirección

#### Desarrollador intentando acceder a clientes:
```
http://127.0.0.1:8000/clientes/
```
**Resultado:** Mensaje de error y redirección

#### Usuario no autenticado:
```
http://127.0.0.1:8000/dashboard/
```
**Resultado:** Redirección a login

## 🔧 Comandos Útiles

### Crear datos de semilla
```bash
python manage.py crear_semilla
```

### Resetear y crear datos nuevos
```bash
python manage.py crear_semilla --reset
```

### Script interactivo de gestión
```bash
./gestionar_datos.sh
```

### Ver usuarios en shell de Django
```bash
python manage.py shell
>>> from core.usuarios.UsuarioModel import Usuario
>>> Usuario.objects.filter(tipo_usuario='cliente').values('username', 'first_name', 'last_name')
```

## 🌐 URLs de Prueba

| URL | Descripción | Acceso |
|-----|-------------|--------|
| `http://127.0.0.1:8000/` | Página principal | Público |
| `http://127.0.0.1:8000/login/` | Página de login | Público |
| `http://127.0.0.1:8000/dashboard/` | Dashboard principal | Autenticado |
| `http://127.0.0.1:8000/clientes/` | Gestión de clientes | Cliente/Admin |
| `http://127.0.0.1:8000/desarrolladores/` | Área desarrolladores | Desarrollador/Admin |
| `http://127.0.0.1:8000/backoffice/` | Backoffice | Solo Admin |
| `http://127.0.0.1:8000/admin/` | Django Admin | Staff/Superuser |

## 🎯 Escenarios de Prueba Sugeridos

### Escenario 1: Flujo Completo de Cliente
1. Ir a página principal
2. Hacer clic en "Iniciar Sesión"
3. Login con `cliente_maria` / `cliente123`
4. Verificar dashboard de cliente
5. Verificar información de empresa TechInno
6. Intentar acceder a `/desarrolladores/` (debe fallar)
7. Logout y verificar redirección

### Escenario 2: Flujo Completo de Desarrollador
1. Login con `dev_alberto` / `dev123`
2. Verificar dashboard de desarrollador
3. Verificar cards específicas de desarrollo
4. Intentar acceder a `/clientes/` (debe fallar)
5. Intentar acceder a `/backoffice/` (debe fallar)

### Escenario 3: Gestión Administrativa
1. Login como admin
2. Ir a dashboard de backoffice
3. Verificar estadísticas (5 clientes, 6 desarrolladores)
4. Ir al panel de Django admin
5. Crear nuevos usuarios
6. Editar información de clientes

### Escenario 4: Seguridad y Restricciones
1. Intentar acceder a URLs protegidas sin login
2. Login con cada tipo de usuario
3. Verificar que cada uno solo ve su área
4. Probar logout desde diferentes dashboards

## 📝 Notas de Desarrollo

- **Contraseñas simples**: Solo para desarrollo, en producción usar contraseñas seguras
- **Datos ficticios**: Todos los datos son de prueba
- **Regeneración**: Puedes resetear datos con `--reset`
- **Escalabilidad**: Fácil agregar más usuarios/empresas modificando el comando

## 🚀 Próximos Pasos

Con estos datos de semilla ya puedes:
1. **Probar completamente** el sistema de autenticación
2. **Desarrollar nuevas funcionalidades** con datos reales
3. **Hacer demos** del sistema a stakeholders
4. **Testear permisos** y restricciones de acceso
5. **Desarrollar APIs** con usuarios de diferentes tipos

¡El sistema está listo para desarrollo y pruebas! 🎉

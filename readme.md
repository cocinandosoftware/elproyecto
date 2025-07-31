

TITULO
Cocinando Software - ElProyectoEl entorno para que clientes y desarrolladores cocinen sus proyectos

DESCRIPCION GENERAL
El problema:
En el proceso de desarrollo de software hay muchísimas ineficiencias provocadas por la falta de comunicación y entendimiento entre clientes y desarrolladores. Ineficiencias que podrían evitarse si ambos hablasen un idioma similar o bien cada uno pusiera de su parte para compartir la idea de proyecto, evolución y proceso de implementación. Algunos ejemplos:

Clientes que no saben cómo pedir lo que necesitan.
Desarrolladores que reciben proyectos mal definidos o sin contexto.
Pérdida de tiempo y dinero en malentendidos y desarrollos ineficaces.
Falta de seguimiento claro de tareas, fases, entregables y decisiones.
Dificultad para generar confianza mutua entre cliente y proveedor.

Visión:
Crear un entorno común que unifique la comunicación entre clientes y desarrolladores, asegurando que los proyectos se planifican, desarrollan y entregan con claridad, orden y responsabilidad compartida.

Misión:Desarrollar una plataforma que actúe como intermediaria entre ambas partes, permitiendo estructurar los proyectos, seguir su evolución y garantizar una comunicación fluida basada en una metodología clara.

A quién va dirigido?
Clientes:
Empresas que contratan desarrolladores freelance o equipos externos de desarrollo
Personas no técnicas que necesitan desarrollar software sin saber cómo gestionarlo.
Desarrolladores:
Freelance que trabajan para varios clientes.
Equipos de desarrollo que quieren estandarizar la toma de requisitos y la relación con clientes.

Propuesta de valor
Esta herramienta permite hablar el mismo idioma a ambos lados del desarrollo. Los proyectos se definen con claridad, los roles y responsables están identificados, y las decisiones y tareas quedan documentadas. Tanto el cliente como el desarrollador trabajan con una metodología común que garantiza mayor calidad y menor fricción.

Metodología de desarrollo
Este proyecto será desarrollado de forma pública y documentada a través del canal @CocinandoSoftware, para que otros desarrolladores puedan aprender del proceso, y los clientes puedan, además de entender cómo se construye un software de calidad desde cero, hacer uso de la plataforma de proyectos compartida

Tecnologías previstas
De momento  implementaremos el Backend en Django (Python), el Frontend con Javascript Vanilla y la base de datos será SQlite inicialmente (luego Postgresql)

Funcionalidades de la plataforma inicialesEl objetivo será ir construyendo la plataforma poco a poco y que también la audiencia del canal pueda hacer sus aportaciones para que podamos tener en cuenta más cosas

ESTRUCTURAS INICIALES O ROLES Y ESPECIFICACIONES

Área de Desarrolladores:
Gestión de proyectos
Listado de proyectos y su estado
Envío de invitación al cliente para que pueda unirse al proyecto
Ficha del proyecto (modo lectura)
Gestión de clientes
Listado de clientes y proyectos vinculados
Ficha del cliente
Gestión de historias de usuario
Listado de historias de usuarios categorizadas
Acceso a la ficha de cada historia de usuario (modo lectura)
Gestión y seguimiento de tareas
Listado de tareas y su estado de implementación (+ historias asociadas + usuario creador, + fecha limite + descripción tarea, etc..)
Acceso ficha de una tarea

Área de Clientes:
Gestión de proyectos
Listado de proyectos y su estado
Envío de invitación al desarrollador para que pueda unirse al proyecto
Ficha del proyecto
Gestión de proveedores
Listado de proveedores y proyectos vinculados
Ficha del proveedor
Gestión de historias de usuario
Listado de historias de usuarios categorizadas
Ficha de  historia de usuario (descripción, imágenes asociadas, criterios aceptación)
Gestión y seguimiento de tareas
Listado de tareas y su estado de implementación (+ historias asociadas + usuario creador, + fecha limite + descripción tarea, etc..)
Acceso ficha de una tarea


PASOS A SEGUIR INICIALES 


Pasos a seguir:
Desarrollo de un entorno tipo "CRM" para que toda la plataforma esté basada en una estructura funcional standard. Básicamente se trata de crear
Una estructura de tipo listado de registros, con su buscador por filtros, sus indicadores para kpis relevantes, un sistema de paginación para los registros obtenidos y finalmente un sistema de acciones vinculado a cada registro.
Una estructura de tipo popup que permita mostrar información detallada y/o  funcionalidades de formulario para actualizar o bien insertar datos
Desarrollo del entorno admin que nos permita incorporar datos en la base de datos a través de un entorno amigable que proporciona Django de forma automática
Diagrama de la estructura del proyecto
Desarrollo del entorno clientes básico
Desarrollo del entorno desarrolladores básico
Desarrollo del sistema login para que el usuario pueda acceder a un entorno o al otro
Implementación de sistema de seguridad para evitar accesos no permitidos
Usuarios no permitidos
El desarrollador solo puede acceder a su área de trabajo
El cliente solo puede acceder a su área de trabajo
Implementación del entorno de trabajo del desarrollador
Historias de usuario
Prototipos
Implementaciones
Implementación del entorno de trabajo del cliente
Historias de usuario
Prototipos
Implementaciones
Configuración y publicación en un servidor dedicado (manual)
Aplicando integración continua...
Pensado en un entorno Móvil para clientes ...
"""
Script para generar usuarios masivamente en el sistema ElProyecto.
Genera clientes y desarrolladores con datos realistas para testing y desarrollo.

Uso desde Django shell:
    python manage.py shell
    from library.generar_usuarios import generar_usuarios_masivos
    generar_usuarios_masivos(num_clientes=80, num_desarrolladores=70)

Uso como comando directo:
    python library/generar_usuarios.py
"""

import os
import sys
import django
import random
from datetime import datetime

# Configurar Django
if __name__ == '__main__':
    # Agregar el directorio raíz al path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elproyecto.settings')
    django.setup()

from django.db import transaction
from core.usuarios.UsuarioModel import Usuario
from core.clientes.ClienteModel import Cliente
from core.desarrolladores.DesarrolladorModel import Desarrollador


# Datos para generar usuarios realistas
NOMBRES = [
    'Ana', 'Carlos', 'María', 'José', 'Laura', 'David', 'Elena', 'Miguel',
    'Carmen', 'Francisco', 'Isabel', 'Antonio', 'Rosa', 'Manuel', 'Patricia',
    'Pedro', 'Lucía', 'Javier', 'Marta', 'Ángel', 'Teresa', 'Juan', 'Cristina',
    'Luis', 'Beatriz', 'Sergio', 'Silvia', 'Fernando', 'Pilar', 'Rafael',
    'Victoria', 'Pablo', 'Mónica', 'Alberto', 'Sandra', 'Raúl', 'Natalia',
    'Alejandro', 'Andrea', 'Jorge', 'Eva', 'Daniel', 'Irene', 'Rubén', 'Sofía',
    'Adrián', 'Clara', 'Iván', 'Paula', 'Óscar', 'Nuria', 'Marcos', 'Julia',
    'Álvaro', 'Marina', 'Gonzalo', 'Alicia', 'Hugo', 'Rocío', 'Diego',
]

APELLIDOS = [
    'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez',
    'Sánchez', 'Pérez', 'Gómez', 'Martín', 'Jiménez', 'Ruiz', 'Hernández',
    'Díaz', 'Moreno', 'Muñoz', 'Álvarez', 'Romero', 'Alonso', 'Gutiérrez',
    'Navarro', 'Torres', 'Domínguez', 'Vázquez', 'Ramos', 'Gil', 'Ramírez',
    'Serrano', 'Blanco', 'Suárez', 'Molina', 'Morales', 'Ortega', 'Delgado',
    'Castro', 'Ortiz', 'Rubio', 'Marín', 'Sanz', 'Iglesias', 'Nuñez',
    'Medina', 'Garrido', 'Santos', 'Castillo', 'Cortés', 'Lozano', 'Méndez',
]

EMPRESAS = [
    'Soluciones', 'Sistemas', 'Tecnología', 'Digital', 'Consulting', 'Group',
    'Innovación', 'Software', 'Tech', 'Data', 'Cloud', 'Web', 'Apps', 'Labs',
    'Studio', 'Factory', 'Works', 'Solutions', 'Partners', 'Associates',
]

SECTORES = [
    'Retail', 'Finanzas', 'Salud', 'Educación', 'Logística', 'Industrial',
    'Turismo', 'Inmobiliaria', 'Automoción', 'Alimentación', 'Textil', 'Media',
]

PERFILES_DEV = [
    'Frontend', 'Backend', 'Full Stack', 'DevOps', 'QA', 'Mobile',
    'Data Engineer', 'ML Engineer', 'UI/UX', 'Arquitecto',
]

DOMINIOS_EMAIL = [
    'gmail.com', 'hotmail.com', 'yahoo.es', 'outlook.com', 'empresa.com',
    'tech.es', 'consulting.es', 'solutions.com', 'mail.com',
]


def generar_username(nombre, apellido, numero):
    """
    Genera un nombre de usuario único basado en nombre y apellido
    """
    # Remover acentos y caracteres especiales
    nombre_clean = nombre.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
    apellido_clean = apellido.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
    
    # Generar variaciones
    opciones = [
        f"{nombre_clean}.{apellido_clean}{numero}",
        f"{nombre_clean}{apellido_clean}{numero}",
        f"{nombre_clean[0]}{apellido_clean}{numero}",
        f"{nombre_clean}_{apellido_clean}{numero}",
        f"{apellido_clean}{nombre_clean}{numero}",
    ]
    
    return random.choice(opciones)


def generar_email(nombre, apellido, dominio):
    """
    Genera un email único
    """
    nombre_clean = nombre.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
    apellido_clean = apellido.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
    
    opciones = [
        f"{nombre_clean}.{apellido_clean}@{dominio}",
        f"{nombre_clean}{apellido_clean}@{dominio}",
        f"{nombre_clean[0]}{apellido_clean}@{dominio}",
        f"{apellido_clean}.{nombre_clean}@{dominio}",
    ]
    
    return random.choice(opciones)


def generar_nombre_empresa(apellido):
    """
    Genera un nombre de empresa realista
    """
    tipo_empresa = random.choice(EMPRESAS)
    sector = random.choice(SECTORES)
    
    opciones = [
        f"{apellido} {tipo_empresa}",
        f"{sector} {tipo_empresa}",
        f"{apellido} {sector}",
        f"{tipo_empresa} {apellido}",
    ]
    
    return random.choice(opciones)


def generar_telefono():
    """
    Genera un número de teléfono español realista
    """
    prefijos = ['6', '7', '9']
    prefijo = random.choice(prefijos)
    
    if prefijo in ['6', '7']:
        # Móviles
        numero = f"{prefijo}{random.randint(0, 9)}{random.randint(100000000, 999999999) % 100000000:08d}"
    else:
        # Fijos
        numero = f"{prefijo}{random.randint(1, 9)}{random.randint(100000000, 999999999) % 10000000:07d}"
    
    return numero


def generar_nif():
    """
    Genera un NIF español aleatorio (formato simplificado para testing)
    """
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return f"{random.randint(10000000, 99999999)}{random.choice(letras)}"


def generar_clientes(cantidad, inicio=1):
    """
    Genera múltiples clientes con datos realistas
    """
    clientes_creados = []
    
    print(f"\n{'='*60}")
    print(f"Generando {cantidad} clientes...")
    print(f"{'='*60}")
    
    for i in range(cantidad):
        try:
            with transaction.atomic():
                # Generar datos aleatorios
                nombre = random.choice(NOMBRES)
                apellido1 = random.choice(APELLIDOS)
                apellido2 = random.choice(APELLIDOS)
                apellidos = f"{apellido1} {apellido2}"
                
                numero = inicio + i
                username = generar_username(nombre, apellido1, numero)
                dominio = random.choice(DOMINIOS_EMAIL)
                email = generar_email(nombre, apellido1, dominio)
                
                # Verificar que no exista el usuario
                while Usuario.objects.filter(username=username).exists():
                    numero += 1000
                    username = generar_username(nombre, apellido1, numero)
                
                while Usuario.objects.filter(email=email).exists():
                    dominio = random.choice(DOMINIOS_EMAIL)
                    email = generar_email(nombre, apellido1, dominio)
                
                nombre_empresa = generar_nombre_empresa(apellido1)
                razon_social = f"{nombre_empresa} S.L."
                telefono = generar_telefono()
                nif = generar_nif()
                
                # Crear el cliente
                cliente = Cliente()
                cliente.nombre = nombre_empresa
                cliente.razon_social = razon_social
                cliente.nif = nif
                cliente.contacto_nombre = f"{nombre} {apellidos}"
                cliente.contacto_email = email
                cliente.contacto_telefono = telefono
                cliente.total_facturacion = round(random.uniform(1000, 50000), 2)
                cliente.save()
                
                # Crear el usuario asociado
                usuario = Usuario()
                usuario.username = username
                usuario.email = email
                usuario.set_password('cliente123')  # Contraseña por defecto
                usuario.first_name = nombre
                usuario.last_name = apellidos
                usuario.tipo_usuario = 'cliente'
                usuario.cliente_asociado = cliente
                usuario.telefono = telefono
                usuario.save()
                
                clientes_creados.append({
                    'username': username,
                    'email': email,
                    'nombre': f"{nombre} {apellidos}",
                    'empresa': nombre_empresa,
                })
                
                # Progress bar
                if (i + 1) % 10 == 0:
                    print(f"[{'#' * ((i + 1) // 10)}{'.' * ((cantidad - i - 1) // 10)}] {i + 1}/{cantidad} clientes creados")
        
        except Exception as e:
            print(f"❌ Error al crear cliente {i + 1}: {str(e)}")
            continue
    
    print(f"\n✅ {len(clientes_creados)} clientes creados exitosamente")
    return clientes_creados


def generar_desarrolladores(cantidad, inicio=1):
    """
    Genera múltiples desarrolladores con datos realistas
    """
    desarrolladores_creados = []
    
    print(f"\n{'='*60}")
    print(f"Generando {cantidad} desarrolladores...")
    print(f"{'='*60}")
    
    for i in range(cantidad):
        try:
            with transaction.atomic():
                # Generar datos aleatorios
                nombre = random.choice(NOMBRES)
                apellido1 = random.choice(APELLIDOS)
                apellido2 = random.choice(APELLIDOS)
                apellidos = f"{apellido1} {apellido2}"
                
                numero = inicio + i
                username = generar_username(nombre, apellido1, numero)
                dominio = random.choice(DOMINIOS_EMAIL)
                email = generar_email(nombre, apellido1, dominio)
                
                # Verificar que no exista el usuario
                while Usuario.objects.filter(username=username).exists():
                    numero += 1000
                    username = generar_username(nombre, apellido1, numero)
                
                while Usuario.objects.filter(email=email).exists():
                    dominio = random.choice(DOMINIOS_EMAIL)
                    email = generar_email(nombre, apellido1, dominio)
                
                perfil = random.choice(PERFILES_DEV)
                telefono = generar_telefono()
                
                # Crear el desarrollador
                desarrollador = Desarrollador()
                desarrollador.nombre = f"{nombre} {apellidos}"
                desarrollador.perfil = perfil
                desarrollador.save()
                
                # Crear el usuario asociado
                usuario = Usuario()
                usuario.username = username
                usuario.email = email
                usuario.set_password('dev123')  # Contraseña por defecto
                usuario.first_name = nombre
                usuario.last_name = apellidos
                usuario.tipo_usuario = 'desarrollador'
                usuario.desarrollador_asociado = desarrollador
                usuario.telefono = telefono
                usuario.save()
                
                desarrolladores_creados.append({
                    'username': username,
                    'email': email,
                    'nombre': f"{nombre} {apellidos}",
                    'perfil': perfil,
                })
                
                # Progress bar
                if (i + 1) % 10 == 0:
                    print(f"[{'#' * ((i + 1) // 10)}{'.' * ((cantidad - i - 1) // 10)}] {i + 1}/{cantidad} desarrolladores creados")
        
        except Exception as e:
            print(f"❌ Error al crear desarrollador {i + 1}: {str(e)}")
            continue
    
    print(f"\n✅ {len(desarrolladores_creados)} desarrolladores creados exitosamente")
    return desarrolladores_creados


def generar_usuarios_masivos(num_clientes=80, num_desarrolladores=70, verbose=True):
    """
    Función principal para generar usuarios masivos.
    
    Args:
        num_clientes (int): Cantidad de clientes a generar
        num_desarrolladores (int): Cantidad de desarrolladores a generar
        verbose (bool): Mostrar información detallada
    
    Returns:
        dict: Resumen de usuarios creados
    """
    inicio = datetime.now()
    
    print(f"\n{'='*60}")
    print(f"GENERACIÓN MASIVA DE USUARIOS - {inicio.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*60}")
    print(f"Clientes a generar: {num_clientes}")
    print(f"Desarrolladores a generar: {num_desarrolladores}")
    print(f"Total usuarios: {num_clientes + num_desarrolladores}")
    print(f"{'='*60}\n")
    
    # Generar clientes
    clientes = generar_clientes(num_clientes, inicio=1000)
    
    # Generar desarrolladores
    desarrolladores = generar_desarrolladores(num_desarrolladores, inicio=2000)
    
    # Resumen final
    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()
    
    print(f"\n{'='*60}")
    print(f"RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"✅ Clientes creados: {len(clientes)}")
    print(f"✅ Desarrolladores creados: {len(desarrolladores)}")
    print(f"✅ Total usuarios creados: {len(clientes) + len(desarrolladores)}")
    print(f"⏱️  Tiempo total: {duracion:.2f} segundos")
    print(f"{'='*60}")
    
    # Mostrar contraseñas por defecto
    print(f"\n📝 NOTAS IMPORTANTES:")
    print(f"   - Contraseña clientes: cliente123")
    print(f"   - Contraseña desarrolladores: dev123")
    print(f"   - Los usernames y emails son únicos")
    print(f"   - Los datos son aleatorios pero realistas")
    print(f"{'='*60}\n")
    
    if verbose and (clientes or desarrolladores):
        print(f"\n📋 MUESTRA DE USUARIOS CREADOS:")
        print(f"{'='*60}")
        
        if clientes:
            print(f"\nPrimeros 5 clientes:")
            for i, cliente in enumerate(clientes[:5], 1):
                print(f"  {i}. {cliente['username']} - {cliente['nombre']} ({cliente['empresa']}) - {cliente['email']}")
        
        if desarrolladores:
            print(f"\nPrimeros 5 desarrolladores:")
            for i, dev in enumerate(desarrolladores[:5], 1):
                print(f"  {i}. {dev['username']} - {dev['nombre']} ({dev['perfil']}) - {dev['email']}")
        
        print(f"{'='*60}\n")
    
    return {
        'clientes': clientes,
        'desarrolladores': desarrolladores,
        'total': len(clientes) + len(desarrolladores),
        'duracion': duracion,
    }


def limpiar_usuarios_generados():
    """
    Función para limpiar usuarios generados (¡USAR CON CUIDADO!)
    Solo elimina usuarios con usernames que contengan números > 1000
    """
    print("\n⚠️  LIMPIEZA DE USUARIOS GENERADOS")
    print("="*60)
    
    # Confirmación
    confirmacion = input("¿Estás seguro de eliminar usuarios generados? (escribe 'SI' para confirmar): ")
    
    if confirmacion != 'SI':
        print("❌ Operación cancelada")
        return
    
    # Eliminar usuarios generados (basado en el patrón de username)
    usuarios_eliminados = 0
    
    # Buscar usuarios con números en el username que indican que fueron generados
    usuarios_gen = Usuario.objects.filter(tipo_usuario__in=['cliente', 'desarrollador'])
    
    for usuario in usuarios_gen:
        # Extraer números del username
        numeros = ''.join(filter(str.isdigit, usuario.username))
        if numeros and int(numeros) >= 1000:
            usuario.delete()
            usuarios_eliminados += 1
            if usuarios_eliminados % 10 == 0:
                print(f"Eliminados {usuarios_eliminados} usuarios...")
    
    print(f"✅ {usuarios_eliminados} usuarios eliminados")
    print("="*60)


if __name__ == '__main__':
    """
    Ejecución directa del script
    """
    import sys
    
    # Configuración por defecto
    num_clientes = 80
    num_desarrolladores = 70
    
    # Parsear argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == 'limpiar':
            limpiar_usuarios_generados()
            sys.exit(0)
        else:
            try:
                num_clientes = int(sys.argv[1])
                if len(sys.argv) > 2:
                    num_desarrolladores = int(sys.argv[2])
            except ValueError:
                print("Uso: python generar_usuarios.py [num_clientes] [num_desarrolladores]")
                print("Ejemplo: python generar_usuarios.py 100 50")
                sys.exit(1)
    
    # Generar usuarios
    resultado = generar_usuarios_masivos(
        num_clientes=num_clientes,
        num_desarrolladores=num_desarrolladores,
        verbose=True
    )

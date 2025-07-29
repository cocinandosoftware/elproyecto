from django.core.management.base import BaseCommand
from django.db import transaction
from core.usuarios.UsuarioModel import Usuario
from core.clientes.ClienteModel import Cliente
from core.proyectos.ProyectoModel import Proyecto
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Crea datos de semilla para usuarios clientes y desarrolladores'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🌱 Iniciando creación de datos de semilla...')
        )

        if options['reset']:
            self.reset_data()

        with transaction.atomic():
            # Crear clientes empresa
            clientes = self.create_clientes()
            
            # Crear usuarios clientes
            usuarios_clientes = self.create_usuarios_clientes(clientes)
            
            # Crear usuarios desarrolladores
            usuarios_desarrolladores = self.create_usuarios_desarrolladores()
            
            # Crear algunos proyectos
            proyectos = self.create_proyectos()

        self.stdout.write(
            self.style.SUCCESS('\n✅ Datos de semilla creados exitosamente!')
        )
        
        self.print_summary(usuarios_clientes, usuarios_desarrolladores, clientes, proyectos)

    def reset_data(self):
        self.stdout.write('🗑️  Eliminando datos existentes...')
        
        # Eliminar en orden correcto para evitar problemas de claves foráneas
        Usuario.objects.filter(is_superuser=False).delete()
        Proyecto.objects.all().delete()
        Cliente.objects.all().delete()
        
        self.stdout.write(
            self.style.WARNING('   Datos existentes eliminados.')
        )

    def create_clientes(self):
        self.stdout.write('🏢 Creando clientes empresa...')
        
        clientes_data = [
            {
                'razon_social': 'Tecnologías Innovadoras S.L.',
                'nombre_comercial': 'TechInno',
                'nif': '12345678A',
                'contacto_nombre': 'María García',
                'contacto_telefono': '+34 600 123 456',
                'contacto_email': 'maria.garcia@techinno.es',
                'total_facturacion': Decimal('50000.00')
            },
            {
                'razon_social': 'Desarrollo Web Profesional S.A.',
                'nombre_comercial': 'WebPro',
                'nif': '87654321B',
                'contacto_nombre': 'Carlos Rodríguez',
                'contacto_telefono': '+34 600 234 567',
                'contacto_email': 'carlos.rodriguez@webpro.es',
                'total_facturacion': Decimal('75000.00')
            },
            {
                'razon_social': 'Startup Digital Solutions',
                'nombre_comercial': 'DigitalStart',
                'nif': '11223344C',
                'contacto_nombre': 'Ana Martínez',
                'contacto_telefono': '+34 600 345 678',
                'contacto_email': 'ana.martinez@digitalstart.es',
                'total_facturacion': Decimal('25000.00')
            },
            {
                'razon_social': 'E-Commerce Global S.L.',
                'nombre_comercial': 'EcomGlobal',
                'nif': '55667788D',
                'contacto_nombre': 'Pedro López',
                'contacto_telefono': '+34 600 456 789',
                'contacto_email': 'pedro.lopez@ecomglobal.es',
                'total_facturacion': Decimal('120000.00')
            },
            {
                'razon_social': 'Fintech Innovations S.A.',
                'nombre_comercial': 'FintechInn',
                'nif': '99887766E',
                'contacto_nombre': 'Laura Sánchez',
                'contacto_telefono': '+34 600 567 890',
                'contacto_email': 'laura.sanchez@fintechinn.es',
                'total_facturacion': Decimal('90000.00')
            }
        ]
        
        clientes = []
        for cliente_data in clientes_data:
            cliente = Cliente.objects.create(**cliente_data)
            clientes.append(cliente)
            self.stdout.write(f'   ✓ Cliente: {cliente.nombre_comercial}')
        
        return clientes

    def create_usuarios_clientes(self, clientes):
        self.stdout.write('👥 Creando usuarios clientes...')
        
        usuarios_clientes_data = [
            {
                'username': 'cliente_maria',
                'email': 'maria.garcia@techinno.es',
                'first_name': 'María',
                'last_name': 'García',
                'password': 'cliente123',
                'tipo_usuario': 'cliente',
                'telefono': '+34 600 123 456',
                'cliente_asociado': clientes[0]
            },
            {
                'username': 'cliente_carlos',
                'email': 'carlos.rodriguez@webpro.es',
                'first_name': 'Carlos',
                'last_name': 'Rodríguez',
                'password': 'cliente123',
                'tipo_usuario': 'cliente',
                'telefono': '+34 600 234 567',
                'cliente_asociado': clientes[1]
            },
            {
                'username': 'cliente_ana',
                'email': 'ana.martinez@digitalstart.es',
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'password': 'cliente123',
                'tipo_usuario': 'cliente',
                'telefono': '+34 600 345 678',
                'cliente_asociado': clientes[2]
            },
            {
                'username': 'cliente_pedro',
                'email': 'pedro.lopez@ecomglobal.es',
                'first_name': 'Pedro',
                'last_name': 'López',
                'password': 'cliente123',
                'tipo_usuario': 'cliente',
                'telefono': '+34 600 456 789',
                'cliente_asociado': clientes[3]
            },
            {
                'username': 'cliente_laura',
                'email': 'laura.sanchez@fintechinn.es',
                'first_name': 'Laura',
                'last_name': 'Sánchez',
                'password': 'cliente123',
                'tipo_usuario': 'cliente',
                'telefono': '+34 600 567 890',
                'cliente_asociado': clientes[4]
            }
        ]
        
        usuarios_clientes = []
        for usuario_data in usuarios_clientes_data:
            password = usuario_data.pop('password')
            usuario = Usuario.objects.create_user(**usuario_data)
            usuario.set_password(password)
            usuario.save()
            usuarios_clientes.append(usuario)
            self.stdout.write(f'   ✓ Usuario cliente: {usuario.username} ({usuario.nombre_completo})')
        
        return usuarios_clientes

    def create_usuarios_desarrolladores(self):
        self.stdout.write('💻 Creando usuarios desarrolladores...')
        
        usuarios_dev_data = [
            {
                'username': 'dev_alberto',
                'email': 'alberto.dev@cocinandosoftware.es',
                'first_name': 'Alberto',
                'last_name': 'Fernández',
                'password': 'dev123',
                'tipo_usuario': 'desarrollador',
                'telefono': '+34 700 111 222'
            },
            {
                'username': 'dev_sofia',
                'email': 'sofia.dev@cocinandosoftware.es',
                'first_name': 'Sofía',
                'last_name': 'González',
                'password': 'dev123',
                'tipo_usuario': 'desarrollador',
                'telefono': '+34 700 222 333'
            },
            {
                'username': 'dev_miguel',
                'email': 'miguel.dev@cocinandosoftware.es',
                'first_name': 'Miguel',
                'last_name': 'Ruiz',
                'password': 'dev123',
                'tipo_usuario': 'desarrollador',
                'telefono': '+34 700 333 444'
            },
            {
                'username': 'dev_elena',
                'email': 'elena.dev@cocinandosoftware.es',
                'first_name': 'Elena',
                'last_name': 'Torres',
                'password': 'dev123',
                'tipo_usuario': 'desarrollador',
                'telefono': '+34 700 444 555'
            },
            {
                'username': 'dev_javier',
                'email': 'javier.dev@cocinandosoftware.es',
                'first_name': 'Javier',
                'last_name': 'Moreno',
                'password': 'dev123',
                'tipo_usuario': 'desarrollador',
                'telefono': '+34 700 555 666'
            },
            {
                'username': 'dev_lucia',
                'email': 'lucia.dev@cocinandosoftware.es',
                'first_name': 'Lucía',
                'last_name': 'Jiménez',
                'password': 'dev123',
                'tipo_usuario': 'desarrollador',
                'telefono': '+34 700 666 777'
            }
        ]
        
        usuarios_desarrolladores = []
        for usuario_data in usuarios_dev_data:
            password = usuario_data.pop('password')
            usuario = Usuario.objects.create_user(**usuario_data)
            usuario.set_password(password)
            usuario.save()
            usuarios_desarrolladores.append(usuario)
            self.stdout.write(f'   ✓ Usuario desarrollador: {usuario.username} ({usuario.nombre_completo})')
        
        return usuarios_desarrolladores

    def create_proyectos(self):
        self.stdout.write('🚀 Creando proyectos de ejemplo...')
        
        proyectos_data = [
            {'nombre': 'Plataforma E-commerce'},
            {'nombre': 'App Móvil Fintech'},
            {'nombre': 'Sistema de Gestión CRM'},
            {'nombre': 'Portal Web Corporativo'},
            {'nombre': 'API REST Microservicios'},
            {'nombre': 'Dashboard Analytics'},
            {'nombre': 'Sistema de Facturación'},
            {'nombre': 'Marketplace Digital'}
        ]
        
        proyectos = []
        for proyecto_data in proyectos_data:
            proyecto = Proyecto.objects.create(**proyecto_data)
            proyectos.append(proyecto)
            self.stdout.write(f'   ✓ Proyecto: {proyecto.nombre}')
        
        return proyectos

    def print_summary(self, usuarios_clientes, usuarios_desarrolladores, clientes, proyectos):
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📊 RESUMEN DE DATOS CREADOS'))
        self.stdout.write('='*60)
        
        self.stdout.write(f'🏢 Clientes empresa: {len(clientes)}')
        self.stdout.write(f'👥 Usuarios clientes: {len(usuarios_clientes)}')
        self.stdout.write(f'💻 Usuarios desarrolladores: {len(usuarios_desarrolladores)}')
        self.stdout.write(f'🚀 Proyectos: {len(proyectos)}')
        
        self.stdout.write('\n' + self.style.WARNING('🔑 CREDENCIALES PARA PROBAR:'))
        self.stdout.write('-'*40)
        
        self.stdout.write('\n👨‍💼 USUARIOS CLIENTES (password: cliente123):')
        for usuario in usuarios_clientes:
            self.stdout.write(f'   • {usuario.username} - {usuario.nombre_completo}')
            self.stdout.write(f'     📧 {usuario.email}')
            if usuario.cliente_asociado:
                self.stdout.write(f'     🏢 {usuario.cliente_asociado.nombre_comercial}')
        
        self.stdout.write('\n💻 USUARIOS DESARROLLADORES (password: dev123):')
        for usuario in usuarios_desarrolladores:
            self.stdout.write(f'   • {usuario.username} - {usuario.nombre_completo}')
            self.stdout.write(f'     📧 {usuario.email}')
        
        self.stdout.write('\n🌐 URLS PARA PROBAR:')
        self.stdout.write('   • Página principal: http://127.0.0.1:8000/')
        self.stdout.write('   • Login: http://127.0.0.1:8000/login/')
        self.stdout.write('   • Admin: http://127.0.0.1:8000/admin/')
        
        self.stdout.write('\n🎯 PRUEBA EL FLUJO COMPLETO:')
        self.stdout.write('   1. Inicia sesión con cualquier usuario')
        self.stdout.write('   2. Verás el dashboard correspondiente a su rol')
        self.stdout.write('   3. Los clientes verán información de su empresa')
        self.stdout.write('   4. Los desarrolladores verán herramientas de desarrollo')
        
        self.stdout.write('\n' + '='*60)

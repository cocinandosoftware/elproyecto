from django.core.management.base import BaseCommand
from django.db import transaction
from core.desarrolladores.DesarrolladorModel import Desarrollador
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
            
            # Crear clientes 
            clientes = self.create_clientes()
            usuarios_clientes = self.create_usuarios_clientes(clientes)
            
            # Crear usuarios desarrolladores
            desarrolladores = self.create_desarrolladores()
            usuarios_desarrolladores = self.create_usuarios_desarrolladores(desarrolladores)

            # Crear algunos proyectos
            proyectos = self.create_proyectos(usuarios_clientes, usuarios_desarrolladores)

        self.stdout.write(
            self.style.SUCCESS('\n✅ Datos de semilla creados exitosamente!')
        )
        
        self.print_summary(usuarios_clientes, usuarios_desarrolladores, clientes, proyectos)

    def reset_data(self):
        self.stdout.write('🗑️  Eliminando datos existentes...')
        
        # Eliminar en orden correcto para evitar problemas de claves foráneas
        Usuario.objects.filter(is_superuser=False).delete()
        Proyecto.objects.all().delete()
        Desarrollador.objects.all().delete()
        Cliente.objects.all().delete()
        
        self.stdout.write(
            self.style.WARNING('   Datos existentes eliminados.')
        )

    def create_clientes(self):
        self.stdout.write('🏢 Creando clientes empresa...')
        
        clientes_data = [
            {
                'razon_social': 'Tecnologías Innovadoras S.L.',
                'nombre': 'TechInno',
                'nif': '12345678A',
                'contacto_nombre': 'María García',
                'contacto_telefono': '+34 600 123 456',
                'contacto_email': 'maria.garcia@techinno.es',
                'total_facturacion': Decimal('50000.00')
            }
        ]
        
        clientes = []
        for cliente_data in clientes_data:
            cliente = Cliente.objects.create(**cliente_data)
            clientes.append(cliente)
            self.stdout.write(f'   ✓ Cliente: {cliente.nombre}')
        
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

    def create_desarrolladores(self):
        self.stdout.write('💻 Creando usuarios desarrolladores...')
        
        desarrolladores_data = [
            {
                'nombre': 'Alberto Fernández',
                'perfil': 'Full Stack Developer',
            }
        ]
        
        desarrolladores = []
        for desarrollador_data in desarrolladores_data:
            desarrollador = Desarrollador.objects.create(**desarrollador_data)
            desarrolladores.append(desarrollador)
            self.stdout.write(f'   ✓ Desarrollador: {desarrollador.nombre}')

        return desarrolladores

    def create_usuarios_desarrolladores(self, desarrolladores):
        self.stdout.write('💻 Creando usuarios desarrolladores...')
        
        usuarios_dev_data = [
            {
                'username': 'dev_alberto',
                'email': 'alberto.dev@cocinandosoftware.es',
                'first_name': 'Alberto',
                'last_name': 'Fernández',
                'password': 'dev123',
                'tipo_usuario': 'desarrollador',
                'telefono': '+34 700 111 222',
                'desarrollador_asociado': desarrolladores[0]
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

    def create_proyectos(self, usuarios_clientes, usuarios_desarrolladores):
        self.stdout.write('🚀 Creando proyectos de ejemplo...')
        
        proyectos_data = [
            {'nombre': 'Plataforma E-commerce',
             'cliente': usuarios_clientes[0],
             'desarrollador': usuarios_desarrolladores[0]
            },

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
                self.stdout.write(f'     🏢 {usuario.cliente_asociado.nombre}')
        
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

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea usuarios de prueba para el desarrollo'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌱 Iniciando creación de usuarios de prueba...'))
        
        # Crear superusuario admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@elproyecto.com',
                password='admin123',
                first_name='Administrador',
                last_name='Principal',
                role='admin',
                telefono='+34 900 000 000'
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Creado administrador: {admin.username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️  El administrador ya existe: admin')
            )
        
        # Crear clientes de prueba
        clientes_data = [
            {
                'username': 'maria.cliente',
                'email': 'maria@ejemplo.com',
                'password': 'cliente123',
                'first_name': 'María',
                'last_name': 'García',
                'telefono': '+34 600 111 111'
            },
            {
                'username': 'juan.cliente',
                'email': 'juan@ejemplo.com',
                'password': 'cliente123',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'telefono': '+34 600 222 222'
            },
            {
                'username': 'sofia.cliente',
                'email': 'sofia@ejemplo.com',
                'password': 'cliente123',
                'first_name': 'Sofía',
                'last_name': 'Rodríguez',
                'telefono': '+34 600 777 777'
            }
        ]
        
        for cliente_data in clientes_data:
            if not User.objects.filter(username=cliente_data['username']).exists():
                cliente = User.objects.create_user(
                    role='cliente',
                    **cliente_data
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Creado cliente: {cliente.username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  El cliente ya existe: {cliente_data["username"]}')
                )
        
        # Crear desarrolladores de prueba
        desarrolladores_data = [
            {
                'username': 'ana.dev',
                'email': 'ana@ejemplo.com',
                'password': 'dev123',
                'first_name': 'Ana',
                'last_name': 'López',
                'telefono': '+34 600 333 333'
            },
            {
                'username': 'carlos.dev',
                'email': 'carlos@ejemplo.com',
                'password': 'dev123',
                'first_name': 'Carlos',
                'last_name': 'Ruiz',
                'telefono': '+34 600 444 444'
            },
            {
                'username': 'laura.dev',
                'email': 'laura@ejemplo.com',
                'password': 'dev123',
                'first_name': 'Laura',
                'last_name': 'Martín',
                'telefono': '+34 600 555 555'
            },
            {
                'username': 'diego.dev',
                'email': 'diego@ejemplo.com',
                'password': 'dev123',
                'first_name': 'Diego',
                'last_name': 'Fernández',
                'telefono': '+34 600 666 666'
            }
        ]
        
        for dev_data in desarrolladores_data:
            if not User.objects.filter(username=dev_data['username']).exists():
                desarrollador = User.objects.create_user(
                    role='desarrollador',
                    **dev_data
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Creado desarrollador: {desarrollador.username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  El desarrollador ya existe: {dev_data["username"]}')
                )
        
        # Resumen final
        total_users = User.objects.count()
        admin_count = User.objects.filter(role='admin').count()
        client_count = User.objects.filter(role='cliente').count()
        dev_count = User.objects.filter(role='desarrollador').count()
        
        self.stdout.write(self.style.SUCCESS('\n🎉 ¡Proceso completado!'))
        self.stdout.write(self.style.SUCCESS('📊 Resumen de usuarios:'))
        self.stdout.write(f'   👥 Total: {total_users}')
        self.stdout.write(f'   🔧 Administradores: {admin_count}')
        self.stdout.write(f'   👤 Clientes: {client_count}')
        self.stdout.write(f'   💻 Desarrolladores: {dev_count}')
        
        self.stdout.write(self.style.SUCCESS('\n🔑 Credenciales de acceso:'))
        self.stdout.write('🔧 Admin: admin / admin123')
        self.stdout.write('👤 Clientes: maria.cliente, juan.cliente, sofia.cliente / cliente123')
        self.stdout.write('💻 Desarrolladores: ana.dev, carlos.dev, laura.dev, diego.dev / dev123')
        
        self.stdout.write(self.style.SUCCESS('\n🚀 ¡Ya puedes probar los dashboards!'))
        self.stdout.write('🌐 Inicia el servidor: python manage.py runserver')
        self.stdout.write('🔗 Accede en: http://127.0.0.1:8000/')

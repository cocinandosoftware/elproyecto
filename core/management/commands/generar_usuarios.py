"""
Comando Django para generar usuarios masivos en el sistema.

Uso:
    python manage.py generar_usuarios
    python manage.py generar_usuarios --clientes 100 --desarrolladores 50
    python manage.py generar_usuarios --help
"""

from django.core.management.base import BaseCommand, CommandError
from library.generar_usuarios import generar_usuarios_masivos, limpiar_usuarios_generados


class Command(BaseCommand):
    help = 'Genera usuarios masivos (clientes y desarrolladores) con datos realistas para testing'

    def add_arguments(self, parser):
        """
        Agregar argumentos al comando
        """
        parser.add_argument(
            '--clientes',
            type=int,
            default=80,
            help='Número de clientes a generar (default: 80)'
        )
        
        parser.add_argument(
            '--desarrolladores',
            type=int,
            default=70,
            help='Número de desarrolladores a generar (default: 70)'
        )
        
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Eliminar usuarios generados previamente'
        )
        
        parser.add_argument(
            '--silencioso',
            action='store_true',
            help='No mostrar información detallada'
        )

    def handle(self, *args, **options):
        """
        Ejecutar el comando
        """
        num_clientes = options['clientes']
        num_desarrolladores = options['desarrolladores']
        limpiar = options['limpiar']
        verbose = not options['silencioso']
        
        try:
            if limpiar:
                self.stdout.write(self.style.WARNING('Iniciando limpieza de usuarios...'))
                limpiar_usuarios_generados()
                self.stdout.write(self.style.SUCCESS('✅ Limpieza completada'))
                return
            
            # Validar números
            if num_clientes < 0 or num_desarrolladores < 0:
                raise CommandError('El número de usuarios debe ser mayor o igual a 0')
            
            if num_clientes == 0 and num_desarrolladores == 0:
                raise CommandError('Debe generar al menos un usuario')
            
            # Generar usuarios
            self.stdout.write(
                self.style.WARNING(
                    f'Generando {num_clientes} clientes y {num_desarrolladores} desarrolladores...'
                )
            )
            
            resultado = generar_usuarios_masivos(
                num_clientes=num_clientes,
                num_desarrolladores=num_desarrolladores,
                verbose=verbose
            )
            
            # Mensaje de éxito
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ ¡Generación completada! {resultado["total"]} usuarios creados en {resultado["duracion"]:.2f}s'
                )
            )
            
            self.stdout.write(
                self.style.WARNING(
                    f'\n📝 Contraseñas por defecto:'
                )
            )
            self.stdout.write(f'   - Clientes: cliente123')
            self.stdout.write(f'   - Desarrolladores: dev123')
            
        except Exception as e:
            raise CommandError(f'Error al generar usuarios: {str(e)}')

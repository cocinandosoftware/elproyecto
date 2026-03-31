/**
 * Script de diagnóstico para verificar la carga de módulos
 * Agregar temporalmente al template para depurar problemas
 */

console.log('🔍 Diagnóstico de Módulos JavaScript');

// 1. Verificar que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ DOM cargado correctamente');
    
    // 2. Verificar que existan los contenedores necesarios
    const checks = [
        { selector: '.listado-container', name: 'Contenedor principal' },
        { selector: '.kpis-section', name: 'Sección de KPIs' },
        { selector: '.search-section', name: 'Sección de búsqueda' },
        { selector: '.table-section', name: 'Sección de tabla' },
        { selector: '.data-table', name: 'Tabla de datos' },
        { selector: '#filter_busqueda', name: 'Input de búsqueda' },
        { selector: '#filter_tipo_usuario', name: 'Select tipo usuario' },
        { selector: '#filter_estado', name: 'Select estado' },
        { selector: '#btn-limpiar-filtros', name: 'Botón limpiar filtros' }
    ];
    
    checks.forEach(check => {
        const element = document.querySelector(check.selector);
        if (element) {
            console.log(`✅ ${check.name} encontrado`);
        } else {
            console.error(`❌ ${check.name} NO encontrado (selector: ${check.selector})`);
        }
    });
    
    // 3. Verificar que la tabla de usuarios exista en window (si el módulo se cargó)
    setTimeout(() => {
        if (window.usuariosTable) {
            console.log('✅ UsuariosTable inicializada correctamente');
            console.log('Estado de la tabla:', window.usuariosTable.state);
        } else {
            console.error('❌ UsuariosTable NO está disponible en window');
            console.log('Esto puede indicar un error en la carga del módulo');
        }
    }, 500);
});

// 4. Capturar errores de módulos
window.addEventListener('error', (event) => {
    if (event.filename && event.filename.includes('.js')) {
        console.error('❌ Error cargando módulo:', event.filename);
        console.error('Mensaje:', event.message);
        console.error('Línea:', event.lineno);
        console.error('Columna:', event.colno);
    }
});

console.log('📍 Ruta de módulos esperada: /static/js/modules/usuarios/usuarios-init.js');
console.log('🔧 Si hay errores 404, verificar configuración de STATICFILES_DIRS en settings.py');

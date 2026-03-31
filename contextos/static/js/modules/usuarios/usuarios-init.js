/**
 * Punto de entrada para el módulo de Usuarios
 * Inicializa el módulo de usuarios con todas sus funcionalidades
 */

import { UsuariosModule } from './UsuariosModule.js';

/**
 * Inicialización del módulo
 */
document.addEventListener('DOMContentLoaded', () => {
    // Instanciar y inicializar el módulo de usuarios
    const usuariosModule = new UsuariosModule();
    usuariosModule.init();

    // Exponer globalmente para debugging y acceso desde otros scripts
    window.usuariosModule = usuariosModule;

    // Botón crear usuario
    const btnCrear = document.getElementById('btn-crear-usuario');
    if (btnCrear) {
        btnCrear.addEventListener('click', () => {
            usuariosModule.handleCreate();
        });
    }

    // Botón buscar usuarios
    const btnBuscar = document.getElementById('btn-buscar');
    if (btnBuscar) {
        btnBuscar.addEventListener('click', () => {
            usuariosModule.handleBuscar();
        });
    }

    // Permitir búsqueda con Enter en el campo de búsqueda
    const searchInput = document.getElementById('filter_busqueda');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                usuariosModule.handleBuscar();
            }
        });
    }

    // Botón limpiar filtros
    const btnLimpiarFiltros = document.getElementById('btn-limpiar-filtros');
    if (btnLimpiarFiltros) {
        btnLimpiarFiltros.addEventListener('click', () => {
            usuariosModule.limpiarFiltros();
        });
    }

    console.log('✅ Módulo de Usuarios inicializado correctamente');
});


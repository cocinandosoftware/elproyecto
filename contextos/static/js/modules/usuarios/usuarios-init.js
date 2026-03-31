/**
 * Punto de entrada para el módulo de Usuarios
 * Inicializa la tabla de usuarios y sus componentes
 */

import { UsuariosTable } from './UsuariosTable.js';

/**
 * Inicialización del módulo
 */
document.addEventListener('DOMContentLoaded', () => {
    // Instanciar y inicializar la tabla de usuarios
    const usuariosTable = new UsuariosTable();
    usuariosTable.init();

    // Exponer globalmente para debugging (opcional)
    window.usuariosTable = usuariosTable;

    // Botón limpiar filtros (si existe en el HTML)
    const btnLimpiarFiltros = document.getElementById('btn-limpiar-filtros');
    if (btnLimpiarFiltros) {
        btnLimpiarFiltros.addEventListener('click', () => {
            usuariosTable.limpiarFiltros();
        });
    }

    console.log('✅ Módulo de Usuarios inicializado correctamente');
});

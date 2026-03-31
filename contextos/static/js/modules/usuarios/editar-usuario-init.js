/**
 * Punto de entrada para la edición de usuario
 * Maneja:
 * - Navegación entre tabs
 * - Formulario de datos generales
 */

import { ApiClient } from '../../core/ApiClient.js';
import { Utils } from '../../core/Utils.js';

/**
 * Inicialización de la página de edición
 */
document.addEventListener('DOMContentLoaded', () => {
    // ====================
    // NAVEGACIÓN DE TABS
    // ====================
    const tabs = document.querySelectorAll('.tab-button');
    const contents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.dataset.tab;
            
            // Desactivar todos los tabs
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            // Activar tab seleccionado
            tab.classList.add('active');
            document.getElementById(`tab-${targetId}`).classList.add('active');
        });
    });

    // ====================
    // FORMULARIO DE DATOS
    // ====================
    const form = document.getElementById('form-usuario-datos');
    const btnGuardar = document.getElementById('btn-guardar-usuario');
    
    if (!form || !btnGuardar) {
        return; // No estamos en la pestaña de datos
    }
    
    const apiClient = new ApiClient();
    
    // Prevenir submit normal del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Obtener datos del formulario
        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password') || '',
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
            tipo_usuario: formData.get('tipo_usuario'),
            telefono: formData.get('telefono'),
            activo: formData.get('activo') === 'on' || document.getElementById('activo').checked,
        };
        
        // Limpiar errores previos
        document.querySelectorAll('.form-error').forEach(el => {
            el.textContent = '';
            el.style.display = 'none';
        });
        document.querySelectorAll('.form-input, .form-select').forEach(el => {
            el.classList.remove('error');
        });
        
        // Estado de carga
        btnGuardar.disabled = true;
        btnGuardar.textContent = 'Guardando...';
        
        try {
            const response = await apiClient.post(form.action, data);
            
            if (response.success) {
                Utils.mostrarMensaje('success', response.message);
                
                // Opcional: recargar página para mostrar datos actualizados
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                // Mostrar errores de validación
                if (response.errors) {
                    Object.keys(response.errors).forEach(fieldName => {
                        const errorContainer = document.getElementById(`${fieldName}-error`);
                        const inputElement = document.getElementById(fieldName);
                        
                        if (errorContainer && response.errors[fieldName].length > 0) {
                            errorContainer.textContent = response.errors[fieldName].join(', ');
                            errorContainer.style.display = 'block';
                        }
                        
                        if (inputElement) {
                            inputElement.classList.add('error');
                        }
                    });
                    
                    Utils.mostrarMensaje('error', 'Hay errores en el formulario');
                } else {
                    Utils.mostrarMensaje('error', response.message);
                }
            }
        } catch (error) {
            console.error('Error al guardar usuario:', error);
            Utils.mostrarMensaje('error', 'Error al guardar los cambios');
        } finally {
            btnGuardar.disabled = false;
            btnGuardar.textContent = '💾 Guardar Cambios';
        }
    });
    
    // Limpiar errores al escribir
    form.querySelectorAll('.form-input, .form-select, .form-checkbox').forEach(input => {
        input.addEventListener('input', () => {
            const errorContainer = document.getElementById(`${input.name}-error`);
            if (errorContainer) {
                errorContainer.textContent = '';
                errorContainer.style.display = 'none';
            }
            input.classList.remove('error');
        });
    });
});

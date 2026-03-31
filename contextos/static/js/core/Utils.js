/**
 * Utilidades globales para la aplicación
 * Funciones reutilizables en toda la app
 */

export class Utils {
    /**
     * Obtiene el token CSRF de las cookies
     * @returns {string|null} Token CSRF
     */
    static getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Muestra un mensaje de sistema (tipo Django messages)
     * @param {string} tipo - Tipo de mensaje: 'success', 'error', 'warning', 'info'
     * @param {string} mensaje - Texto del mensaje
     */
    static mostrarMensaje(tipo, mensaje) {
        // Crear elemento de mensaje
        const mensajeDiv = document.createElement('div');
        mensajeDiv.className = `mensaje-sistema mensaje-${tipo}`;
        mensajeDiv.textContent = mensaje;
        
        // Añadir al DOM (en la parte superior del contenedor)
        const container = document.querySelector('.listado-container');
        if (container) {
            container.insertBefore(mensajeDiv, container.firstChild);
            
            // Mostrar con animación
            setTimeout(() => mensajeDiv.classList.add('show'), 10);
            
            // Auto-ocultar después de 4 segundos
            setTimeout(() => {
                mensajeDiv.classList.remove('show');
                setTimeout(() => mensajeDiv.remove(), 300);
            }, 4000);
        }
    }

    /**
     * Función debounce para limitar la frecuencia de ejecución
     * @param {Function} func - Función a ejecutar
     * @param {number} delay - Retraso en milisegundos
     * @returns {Function} Función debounced
     */
    static debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    /**
     * Escapa comillas simples en strings para uso en HTML
     * @param {string} str - String a escapar
     * @returns {string} String escapado
     */
    static escapeQuotes(str) {
        return str.replace(/'/g, "\\'");
    }

    /**
     * Formatea un número con separadores de miles
     * @param {number} num - Número a formatear
     * @returns {string} Número formateado
     */
    static formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    /**
     * Valida si un elemento existe en el DOM
     * @param {string} selector - Selector CSS
     * @returns {boolean} True si existe
     */
    static elementExists(selector) {
        return document.querySelector(selector) !== null;
    }
}

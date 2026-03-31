/**
 * Cliente HTTP para peticiones asíncronas
 * Wrapper de fetch API con manejo automático de CSRF y errores
 */

import { Utils } from './Utils.js';

export class ApiClient {
    /**
     * Realiza una petición GET
     * @param {string} url - URL del endpoint
     * @param {Object} params - Parámetros de query string
     * @returns {Promise<Object>} Respuesta JSON
     */
    async get(url, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;
        
        try {
            const response = await fetch(fullUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error en petición GET:', error);
            throw error;
        }
    }

    /**
     * Realiza una petición POST
     * @param {string} url - URL del endpoint
     * @param {Object} data - Datos a enviar
     * @returns {Promise<Object>} Respuesta JSON
     */
    async post(url, data = {}) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': Utils.getCsrfToken()
                },
                body: JSON.stringify(data)
            });
            
            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error en petición POST:', error);
            throw error;
        }
    }

    /**
     * Realiza una petición DELETE
     * @param {string} url - URL del endpoint
     * @returns {Promise<Object>} Respuesta JSON
     */
    async delete(url) {
        try {
            const response = await fetch(url, {
                method: 'POST', // Django usa POST para delete via formularios
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': Utils.getCsrfToken()
                }
            });
            
            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error en petición DELETE:', error);
            throw error;
        }
    }

    /**
     * Maneja la respuesta de la petición
     * @param {Response} response - Respuesta del fetch
     * @returns {Promise<Object>} Datos JSON
     * @throws {Error} Si la respuesta no es ok
     */
    async handleResponse(response) {
        if (!response.ok) {
            // Intentar obtener mensaje de error del servidor
            try {
                const errorData = await response.json();
                throw new Error(errorData.message || `Error ${response.status}: ${response.statusText}`);
            } catch {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
        }
        
        return await response.json();
    }
}

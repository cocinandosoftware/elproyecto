/**
 * Componente de sección de KPIs (Indicadores Clave)
 * Muestra métricas y estadísticas importantes
 */

import { Utils } from '../core/Utils.js';

export class KPISection {
    /**
     * Constructor
     * @param {Object} config - Configuración de KPIs
     */
    constructor(config) {
        this.config = {
            containerSelector: config.containerSelector || '.kpis-section',
            kpis: config.kpis || [], // Array de objetos {id, label, value, icon, color}
            animateNumbers: config.animateNumbers !== false,
            ...config
        };

        this.elements = {
            container: null,
            kpiElements: {}
        };

        this.currentValues = {};
    }

    /**
     * Inicializa el componente
     */
    init() {
        this.cacheElements();
        if (!this.elements.container) {
            this.createContainer();
        }
        this.render();
    }

    /**
     * Cachea elementos del DOM
     */
    cacheElements() {
        this.elements.container = document.querySelector(this.config.containerSelector);
    }

    /**
     * Crea el contenedor si no existe
     */
    createContainer() {
        const container = document.createElement('div');
        container.className = 'kpis-section';
        
        // Insertar al principio del contenido principal
        const main = document.querySelector('main') || document.querySelector('.container');
        if (main) {
            main.insertBefore(container, main.firstChild);
            this.elements.container = container;
        }
    }

    /**
     * Renderiza el HTML de los KPIs
     */
    render() {
        if (!this.elements.container) return;

        const html = `
            <div class="kpis-grid">
                ${this.config.kpis.map(kpi => this.buildKPICard(kpi)).join('')}
            </div>
        `;

        this.elements.container.innerHTML = html;
        this.cacheKPIElements();
    }

    /**
     * Genera el HTML de una tarjeta KPI
     * @param {Object} kpi - Configuración del KPI
     * @returns {string} HTML de la tarjeta
     */
    buildKPICard(kpi) {
        const icon = kpi.icon || '📊';
        const color = kpi.color || 'primary';
        const value = kpi.value !== undefined ? kpi.value : 0;
        const subtitle = kpi.subtitle || '';

        // Guardar valor inicial
        this.currentValues[kpi.id] = value;

        return `
            <div class="kpi-card kpi-${color}" data-kpi-id="${kpi.id}">
                <div class="kpi-icon">${icon}</div>
                <div class="kpi-content">
                    <div class="kpi-label">${kpi.label}</div>
                    <div class="kpi-value" data-kpi-value="${kpi.id}">${Utils.formatNumber(value)}</div>
                    ${subtitle ? `<div class="kpi-subtitle">${subtitle}</div>` : ''}
                </div>
            </div>
        `;
    }

    /**
     * Cachea las referencias a los elementos KPI
     */
    cacheKPIElements() {
        this.config.kpis.forEach(kpi => {
            const element = this.elements.container?.querySelector(`[data-kpi-value="${kpi.id}"]`);
            if (element) {
                this.elements.kpiElements[kpi.id] = element;
            }
        });
    }

    /**
     * Actualiza un KPI específico
     * @param {string} kpiId - ID del KPI
     * @param {number} newValue - Nuevo valor
     * @param {Object} options - Opciones de actualización
     */
    updateKPI(kpiId, newValue, options = {}) {
        const element = this.elements.kpiElements[kpiId];
        if (!element) return;

        const oldValue = this.currentValues[kpiId] || 0;
        this.currentValues[kpiId] = newValue;

        if (this.config.animateNumbers && options.animate !== false) {
            this.animateValue(element, oldValue, newValue);
        } else {
            element.textContent = Utils.formatNumber(newValue);
        }

        // Aplicar clase de cambio si se especifica
        if (options.highlight) {
            this.highlightChange(element, oldValue, newValue);
        }
    }

    /**
     * Anima el cambio de valor de un KPI
     * @param {HTMLElement} element - Elemento del KPI
     * @param {number} start - Valor inicial
     * @param {number} end - Valor final
     */
    animateValue(element, start, end) {
        const duration = 800; // ms
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (ease-out)
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = start + (end - start) * easeOut;

            element.textContent = Utils.formatNumber(Math.round(current));

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    /**
     * Resalta un cambio en el KPI
     * @param {HTMLElement} element - Elemento del KPI
     * @param {number} oldValue - Valor anterior
     * @param {number} newValue - Valor nuevo
     */
    highlightChange(element, oldValue, newValue) {
        const card = element.closest('.kpi-card');
        if (!card) return;

        // Determinar tipo de cambio
        let changeClass = 'kpi-updated';
        if (newValue > oldValue) {
            changeClass = 'kpi-increased';
        } else if (newValue < oldValue) {
            changeClass = 'kpi-decreased';
        }

        // Agregar clase de animación
        card.classList.add(changeClass);

        // Remover clase después de la animación
        setTimeout(() => {
            card.classList.remove(changeClass);
        }, 1000);
    }

    /**
     * Actualiza múltiples KPIs
     * @param {Object} kpisData - Objeto con {kpiId: valor}
     * @param {Object} options - Opciones de actualización
     */
    updateAll(kpisData, options = {}) {
        Object.entries(kpisData).forEach(([kpiId, value]) => {
            this.updateKPI(kpiId, value, options);
        });
    }

    /**
     * Obtiene el valor actual de un KPI
     * @param {string} kpiId - ID del KPI
     * @returns {number} Valor actual
     */
    getValue(kpiId) {
        return this.currentValues[kpiId] || 0;
    }

    /**
     * Obtiene todos los valores actuales
     * @returns {Object} Objeto con todos los valores
     */
    getAllValues() {
        return { ...this.currentValues };
    }

    /**
     * Resetea todos los KPIs a 0
     */
    reset() {
        Object.keys(this.currentValues).forEach(kpiId => {
            this.updateKPI(kpiId, 0, { animate: false });
        });
    }

    /**
     * Agrega un nuevo KPI dinámicamente
     * @param {Object} kpi - Configuración del nuevo KPI
     */
    addKPI(kpi) {
        this.config.kpis.push(kpi);
        this.render();
    }

    /**
     * Elimina un KPI
     * @param {string} kpiId - ID del KPI a eliminar
     */
    removeKPI(kpiId) {
        const index = this.config.kpis.findIndex(k => k.id === kpiId);
        if (index !== -1) {
            this.config.kpis.splice(index, 1);
            delete this.currentValues[kpiId];
            delete this.elements.kpiElements[kpiId];
            this.render();
        }
    }

    /**
     * Muestra un estado de carga en los KPIs
     * @param {boolean} loading - Si está cargando
     */
    setLoading(loading) {
        if (!this.elements.container) return;

        this.elements.container.classList.toggle('loading', loading);

        if (loading) {
            Object.values(this.elements.kpiElements).forEach(element => {
                element.textContent = '...';
            });
        }
    }
}


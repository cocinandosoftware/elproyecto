/**
 * Componente de búsqueda y filtros
 * Gestiona inputs de búsqueda y filtros personalizados
 */

import { Utils } from '../core/Utils.js';

export class SearchFilters {
    /**
     * Constructor
     * @param {Object} config - Configuración de filtros
     */
    constructor(config) {
        this.config = {
            containerSelector: config.containerSelector || '.filters-container',
            searchInputId: config.searchInputId || 'filter_busqueda',
            searchPlaceholder: config.searchPlaceholder || 'Buscar...',
            filters: config.filters || [], // Array de objetos con {type, id, label, options}
            onSearch: config.onSearch || null,
            onFilterChange: config.onFilterChange || null,
            debounceDelay: config.debounceDelay || 300,
            ...config
        };

        this.elements = {
            container: null,
            searchInput: null,
            filterInputs: {}
        };

        this.filterValues = {};
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
        this.setupEventListeners();
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
        container.className = 'filters-container';
        
        // Insertar antes de la tabla (asumiendo estructura común)
        const table = document.querySelector('.data-table');
        if (table) {
            table.parentElement.insertBefore(container, table);
            this.elements.container = container;
        }
    }

    /**
     * Renderiza el HTML de los filtros
     */
    render() {
        if (!this.elements.container) return;

        const html = `
            <div class="search-filters">
                ${this.buildSearchInput()}
                ${this.buildFilters()}
                ${this.buildActionButtons()}
            </div>
        `;

        this.elements.container.innerHTML = html;
        this.cacheFilterElements();
    }

    /**
     * Genera el HTML del input de búsqueda
     * @returns {string} HTML del input
     */
    buildSearchInput() {
        return `
            <div class="filter-group">
                <label for="${this.config.searchInputId}">🔍 Búsqueda</label>
                <input 
                    type="text" 
                    id="${this.config.searchInputId}" 
                    class="form-control" 
                    placeholder="${this.config.searchPlaceholder}"
                >
            </div>
        `;
    }

    /**
     * Genera el HTML de los filtros personalizados
     * @returns {string} HTML de filtros
     */
    buildFilters() {
        if (!this.config.filters || this.config.filters.length === 0) return '';

        return this.config.filters.map(filter => {
            switch (filter.type) {
                case 'select':
                    return this.buildSelectFilter(filter);
                case 'text':
                    return this.buildTextFilter(filter);
                case 'date':
                    return this.buildDateFilter(filter);
                case 'checkbox':
                    return this.buildCheckboxFilter(filter);
                default:
                    return '';
            }
        }).join('');
    }

    /**
     * Genera un filtro de tipo select
     * @param {Object} filter - Configuración del filtro
     * @returns {string} HTML del select
     */
    buildSelectFilter(filter) {
        const options = filter.options || [];
        const optionsHTML = options.map(opt => 
            `<option value="${opt.value}">${opt.label}</option>`
        ).join('');

        return `
            <div class="filter-group">
                <label for="${filter.id}">${filter.label}</label>
                <select id="${filter.id}" class="form-control filter-input" data-filter="${filter.id}">
                    <option value="">Todos</option>
                    ${optionsHTML}
                </select>
            </div>
        `;
    }

    /**
     * Genera un filtro de tipo text
     * @param {Object} filter - Configuración del filtro
     * @returns {string} HTML del input
     */
    buildTextFilter(filter) {
        return `
            <div class="filter-group">
                <label for="${filter.id}">${filter.label}</label>
                <input 
                    type="text" 
                    id="${filter.id}" 
                    class="form-control filter-input" 
                    placeholder="${filter.placeholder || ''}"
                    data-filter="${filter.id}"
                >
            </div>
        `;
    }

    /**
     * Genera un filtro de tipo date
     * @param {Object} filter - Configuración del filtro
     * @returns {string} HTML del input date
     */
    buildDateFilter(filter) {
        return `
            <div class="filter-group">
                <label for="${filter.id}">${filter.label}</label>
                <input 
                    type="date" 
                    id="${filter.id}" 
                    class="form-control filter-input" 
                    data-filter="${filter.id}"
                >
            </div>
        `;
    }

    /**
     * Genera un filtro de tipo checkbox
     * @param {Object} filter - Configuración del filtro
     * @returns {string} HTML del checkbox
     */
    buildCheckboxFilter(filter) {
        return `
            <div class="filter-group filter-checkbox">
                <label>
                    <input 
                        type="checkbox" 
                        id="${filter.id}" 
                        class="filter-input" 
                        data-filter="${filter.id}"
                    >
                    ${filter.label}
                </label>
            </div>
        `;
    }

    /**
     * Genera botones de acción (reset, etc)
     * @returns {string} HTML de botones
     */
    buildActionButtons() {
        return `
            <div class="filter-actions">
                <button type="button" class="btn btn-secondary btn-sm btn-reset-filters">
                    🔄 Limpiar Filtros
                </button>
            </div>
        `;
    }

    /**
     * Cachea las referencias a los inputs de filtro
     */
    cacheFilterElements() {
        this.elements.searchInput = document.getElementById(this.config.searchInputId);
        
        const filterInputs = document.querySelectorAll('.filter-input');
        filterInputs.forEach(input => {
            const filterId = input.dataset.filter;
            if (filterId) {
                this.elements.filterInputs[filterId] = input;
            }
        });
    }

    /**
     * Configura los event listeners
     */
    setupEventListeners() {
        // Búsqueda con debounce
        if (this.elements.searchInput && this.config.onSearch) {
            const debouncedSearch = Utils.debounce(
                () => this.handleSearchChange(),
                this.config.debounceDelay
            );
            this.elements.searchInput.addEventListener('input', debouncedSearch);
        }

        // Filtros personalizados
        Object.entries(this.elements.filterInputs).forEach(([filterId, input]) => {
            const eventType = input.type === 'checkbox' ? 'change' : 'input';
            input.addEventListener(eventType, () => this.handleFilterChange(filterId, input));
        });

        // Botón reset
        const resetBtn = this.elements.container?.querySelector('.btn-reset-filters');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.reset());
        }
    }

    /**
     * Maneja cambios en la búsqueda
     */
    handleSearchChange() {
        const value = this.elements.searchInput?.value.trim() || '';
        if (this.config.onSearch) {
            this.config.onSearch(value);
        }
    }

    /**
     * Maneja cambios en un filtro
     * @param {string} filterId - ID del filtro
     * @param {HTMLElement} input - Input del filtro
     */
    handleFilterChange(filterId, input) {
        let value;

        if (input.type === 'checkbox') {
            value = input.checked;
        } else {
            value = input.value.trim();
        }

        this.filterValues[filterId] = value;

        if (this.config.onFilterChange) {
            this.config.onFilterChange(filterId, value, this.getAllFilters());
        }
    }

    /**
     * Obtiene todos los valores de filtros actuales
     * @returns {Object} Objeto con todos los filtros
     */
    getAllFilters() {
        const allFilters = { ...this.filterValues };

        // Agregar búsqueda si existe
        if (this.elements.searchInput) {
            const searchValue = this.elements.searchInput.value.trim();
            if (searchValue) {
                allFilters.busqueda = searchValue;
            }
        }

        return allFilters;
    }

    /**
     * Resetea todos los filtros
     */
    reset() {
        // Reset búsqueda
        if (this.elements.searchInput) {
            this.elements.searchInput.value = '';
        }

        // Reset filtros personalizados
        Object.values(this.elements.filterInputs).forEach(input => {
            if (input.type === 'checkbox') {
                input.checked = false;
            } else {
                input.value = '';
            }
        });

        this.filterValues = {};

        // Notificar cambio
        if (this.config.onSearch) {
            this.config.onSearch('');
        }
        if (this.config.onFilterChange) {
            this.config.onFilterChange(null, null, {});
        }
    }

    /**
     * Establece un valor de filtro programáticamente
     * @param {string} filterId - ID del filtro
     * @param {*} value - Valor a establecer
     */
    setFilterValue(filterId, value) {
        const input = this.elements.filterInputs[filterId];
        if (input) {
            if (input.type === 'checkbox') {
                input.checked = Boolean(value);
            } else {
                input.value = value;
            }
            this.handleFilterChange(filterId, input);
        }
    }

    /**
     * Obtiene el valor de un filtro
     * @param {string} filterId - ID del filtro
     * @returns {*} Valor del filtro
     */
    getFilterValue(filterId) {
        return this.filterValues[filterId];
    }
}

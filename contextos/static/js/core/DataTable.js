/**
 * Clase base para tablas con paginación y ordenación
 * Implementa el patrón Template Method
 */

import { Utils } from './Utils.js';
import { ApiClient } from './ApiClient.js';

export class DataTable {
    /**
     * Constructor de la tabla
     * @param {Object} config - Configuración de la tabla
     */
    constructor(config) {
        this.config = {
            apiUrl: config.apiUrl || '',
            tableSelector: config.tableSelector || '.data-table',
            paginationSelector: config.paginationSelector || '.pagination',
            searchInputSelector: config.searchInputSelector || '#filter_busqueda',
            sortableHeaders: config.sortableHeaders || [],
            debounceDelay: config.debounceDelay || 300,
            ...config
        };

        // Estado de la tabla
        this.state = {
            currentPage: 1,
            pageSize: 20,
            sortBy: null,
            sortOrder: 'asc',
            totalPages: 1,
            totalItems: 0,
            filters: {}
        };

        // Referencias al DOM
        this.elements = {
            table: null,
            tableBody: null,
            pagination: null,
            searchInput: null
        };

        this.apiClient = new ApiClient();
        this.isLoading = false;
    }

    /**
     * Método abstracto: debe ser implementado por subclases
     * Genera el HTML de una fila de la tabla
     * @param {Object} item - Item a renderizar
     * @returns {string} HTML de la fila
     */
    buildRow(item) {
        throw new Error('buildRow() debe ser implementado por la subclase');
    }

    /**
     * Método abstracto: puede ser sobreescrito por subclases
     * Obtiene los filtros actuales
     * @returns {Object} Filtros a aplicar
     */
    getFilters() {
        return this.state.filters;
    }

    /**
     * Inicializa la tabla
     */
    async init() {
        this.cacheElements();
        this.setupEventListeners();
        await this.loadData();
    }

    /**
     * Cachea las referencias a elementos del DOM
     */
    cacheElements() {
        this.elements.table = document.querySelector(this.config.tableSelector);
        this.elements.tableBody = this.elements.table?.querySelector('tbody');
        this.elements.pagination = document.querySelector(this.config.paginationSelector);
        this.elements.searchInput = document.querySelector(this.config.searchInputSelector);

        if (!this.elements.table || !this.elements.tableBody) {
            console.error('Elementos de tabla no encontrados');
        }
    }

    /**
     * Configura los event listeners
     */
    setupEventListeners() {
        // Búsqueda con debounce
        if (this.elements.searchInput) {
            const debouncedSearch = Utils.debounce(
                () => this.handleSearch(),
                this.config.debounceDelay
            );
            this.elements.searchInput.addEventListener('input', debouncedSearch);
        }

        // Ordenación en headers
        this.setupSortingHeaders();

        // Event listeners personalizados (puede ser extendido por subclases)
        this.setupCustomListeners();
    }

    /**
     * Configura la ordenación en los headers
     */
    setupSortingHeaders() {
        if (!this.elements.table) return;

        const headers = this.elements.table.querySelectorAll('th.sortable');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                const field = header.dataset.field;
                if (field) this.handleSort(field);
            });
        });
    }

    /**
     * Hook para listeners personalizados (puede ser sobreescrito)
     */
    setupCustomListeners() {
        // Implementar en subclases si es necesario
    }

    /**
     * Maneja el evento de búsqueda
     */
    async handleSearch() {
        this.state.currentPage = 1; // Reset a primera página
        const searchValue = this.elements.searchInput?.value.trim() || '';
        this.state.filters.busqueda = searchValue;
        await this.loadData();
    }

    /**
     * Maneja el evento de ordenación
     * @param {string} field - Campo por el cual ordenar
     */
    async handleSort(field) {
        if (this.state.sortBy === field) {
            // Alternar orden
            this.state.sortOrder = this.state.sortOrder === 'asc' ? 'desc' : 'asc';
        } else {
            this.state.sortBy = field;
            this.state.sortOrder = 'asc';
        }

        this.updateSortingIndicators();
        await this.loadData();
    }

    /**
     * Actualiza los indicadores visuales de ordenación
     */
    updateSortingIndicators() {
        if (!this.elements.table) return;

        const headers = this.elements.table.querySelectorAll('th.sortable');
        headers.forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
            if (header.dataset.field === this.state.sortBy) {
                header.classList.add(`sort-${this.state.sortOrder}`);
            }
        });
    }

    /**
     * Carga los datos desde la API
     */
    async loadData() {
        if (this.isLoading) return;

        this.setLoading(true);

        try {
            const params = {
                page: this.state.currentPage,
                page_size: this.state.pageSize,
                ...this.getFilters()
            };

            // Agregar ordenación si está definida
            if (this.state.sortBy) {
                params.order_by = this.state.sortBy;
                params.order_dir = this.state.sortOrder;
            }

            const data = await this.apiClient.get(this.config.apiUrl, params);

            // La API puede devolver items, results, o un array directamente
            const items = data.usuarios || data.items || data.results || data;
            
            this.updateTable(items);
            this.updatePagination(data.pagination || {});
            this.updateKPIs?.(data.kpis || {});

        } catch (error) {
            console.error('Error cargando datos:', error);
            Utils.mostrarMensaje('error', 'Error al cargar los datos');
        } finally {
            this.setLoading(false);
        }
    }

    /**
     * Actualiza la tabla con nuevos datos
     * @param {Array} items - Items a renderizar
     */
    updateTable(items) {
        if (!this.elements.tableBody) return;

        const fragment = document.createDocumentFragment();

        if (items.length === 0) {
            const tr = document.createElement('tr');
            tr.innerHTML = '<td colspan="100%" class="no-data">No hay datos para mostrar</td>';
            fragment.appendChild(tr);
        } else {
            items.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = this.buildRow(item);
                fragment.appendChild(tr);
            });
        }

        // Actualizar el tbody con efecto fade
        this.elements.tableBody.classList.add('fade-out');
        setTimeout(() => {
            this.elements.tableBody.innerHTML = '';
            this.elements.tableBody.appendChild(fragment);
            this.elements.tableBody.classList.remove('fade-out');
            this.elements.tableBody.classList.add('fade-in');

            // Reattach event listeners después de actualizar
            this.attachRowEventListeners();
        }, 150);
    }

    /**
     * Hook para adjuntar event listeners a las filas (puede ser sobreescrito)
     */
    attachRowEventListeners() {
        // Implementar en subclases si es necesario
    }

    /**
     * Actualiza la paginación
     * @param {Object} pagination - Datos de paginación
     */
    updatePagination(pagination) {
        this.state.totalPages = pagination.total_pages || 1;
        this.state.totalItems = pagination.total_items || 0;

        if (!this.elements.pagination) return;

        this.elements.pagination.innerHTML = this.buildPaginationHTML(pagination);
        this.attachPaginationListeners();
    }

    /**
     * Genera el HTML de la paginación
     * @param {Object} pagination - Datos de paginación
     * @returns {string} HTML de paginación
     */
    buildPaginationHTML(pagination) {
        const { current_page, total_pages, has_previous, has_next } = pagination;

        let html = '<div class="pagination-controls">';

        // Botón anterior
        if (has_previous) {
            html += `<button class="btn btn-sm pagination-btn" data-page="${current_page - 1}">Anterior</button>`;
        }

        // Números de página
        const pages = this.getPaginationRange(current_page, total_pages);
        pages.forEach(page => {
            if (page === '...') {
                html += '<span class="pagination-ellipsis">...</span>';
            } else {
                const activeClass = page === current_page ? 'active' : '';
                html += `<button class="btn btn-sm pagination-btn ${activeClass}" data-page="${page}">${page}</button>`;
            }
        });

        // Botón siguiente
        if (has_next) {
            html += `<button class="btn btn-sm pagination-btn" data-page="${current_page + 1}">Siguiente</button>`;
        }

        html += '</div>';
        html += `<div class="pagination-info">Mostrando página ${current_page} de ${total_pages} (${this.state.totalItems} total)</div>`;

        return html;
    }

    /**
     * Calcula el rango de páginas a mostrar
     * @param {number} current - Página actual
     * @param {number} total - Total de páginas
     * @returns {Array} Array con números de página y elipsis
     */
    getPaginationRange(current, total) {
        const delta = 2;
        const range = [];
        const rangeWithDots = [];

        for (let i = 1; i <= total; i++) {
            if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
                range.push(i);
            }
        }

        let prev = 0;
        range.forEach(i => {
            if (prev && i - prev > 1) {
                rangeWithDots.push('...');
            }
            rangeWithDots.push(i);
            prev = i;
        });

        return rangeWithDots;
    }

    /**
     * Adjunta event listeners a los botones de paginación
     */
    attachPaginationListeners() {
        if (!this.elements.pagination) return;

        const buttons = this.elements.pagination.querySelectorAll('.pagination-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const page = parseInt(btn.dataset.page);
                if (page && page !== this.state.currentPage) {
                    this.goToPage(page);
                }
            });
        });
    }

    /**
     * Navega a una página específica
     * @param {number} page - Número de página
     */
    async goToPage(page) {
        if (page < 1 || page > this.state.totalPages) return;
        this.state.currentPage = page;
        await this.loadData();
    }

    /**
     * Establece el estado de carga
     * @param {boolean} loading - Si está cargando o no
     */
    setLoading(loading) {
        this.isLoading = loading;

        if (this.elements.table) {
            const container = this.elements.table.closest('.listado-container');
            if (container) {
                container.classList.toggle('loading', loading);
            }
        }
    }

    /**
     * Refresca los datos de la tabla
     */
    async refresh() {
        await this.loadData();
    }

    /**
     * Resetea los filtros y recarga
     */
    async reset() {
        this.state.currentPage = 1;
        this.state.sortBy = null;
        this.state.sortOrder = 'asc';
        this.state.filters = {};

        if (this.elements.searchInput) {
            this.elements.searchInput.value = '';
        }

        this.updateSortingIndicators();
        await this.loadData();
    }
}

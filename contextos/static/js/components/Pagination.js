/**
 * Componente de paginación standalone
 * Genera y gestiona controles de paginación
 */

export class Pagination {
    /**
     * Constructor
     * @param {Object} config - Configuración de paginación
     */
    constructor(config) {
        this.config = {
            containerSelector: config.containerSelector || '.pagination',
            delta: config.delta || 2, // Páginas a mostrar alrededor de la actual
            onChange: config.onChange || null, // Callback al cambiar de página
            ...config
        };

        this.state = {
            currentPage: 1,
            totalPages: 1,
            totalItems: 0,
            hasNext: false,
            hasPrevious: false
        };

        this.elements = {
            container: null
        };
    }

    /**
     * Inicializa el componente
     */
    init() {
        this.cacheElements();
        this.render();
    }

    /**
     * Cachea elementos del DOM
     */
    cacheElements() {
        this.elements.container = document.querySelector(this.config.containerSelector);
    }

    /**
     * Actualiza el estado de paginación
     * @param {Object} paginationData - Datos de paginación del backend
     */
    update(paginationData) {
        this.state = {
            currentPage: paginationData.current_page || 1,
            totalPages: paginationData.total_pages || 1,
            totalItems: paginationData.total_items || 0,
            hasNext: paginationData.has_next || false,
            hasPrevious: paginationData.has_previous || false
        };

        this.render();
    }

    /**
     * Renderiza el HTML de paginación
     */
    render() {
        if (!this.elements.container) return;

        const html = `
            ${this.buildControls()}
            ${this.buildInfo()}
        `;

        this.elements.container.innerHTML = html;
        this.attachEventListeners();
    }

    /**
     * Genera el HTML de los controles de paginación
     * @returns {string} HTML de controles
     */
    buildControls() {
        const { currentPage, totalPages, hasNext, hasPrevious } = this.state;

        let html = '<div class="pagination-controls">';

        // Botón anterior
        if (hasPrevious) {
            html += `<button class="btn btn-sm pagination-btn" data-page="${currentPage - 1}">Anterior</button>`;
        } else {
            html += `<button class="btn btn-sm pagination-btn" disabled>Anterior</button>`;
        }

        // Números de página
        const pages = this.getPageRange();
        pages.forEach(page => {
            if (page === '...') {
                html += '<span class="pagination-ellipsis">...</span>';
            } else {
                const activeClass = page === currentPage ? 'active' : '';
                html += `<button class="btn btn-sm pagination-btn ${activeClass}" data-page="${page}">${page}</button>`;
            }
        });

        // Botón siguiente
        if (hasNext) {
            html += `<button class="btn btn-sm pagination-btn" data-page="${currentPage + 1}">Siguiente</button>`;
        } else {
            html += `<button class="btn btn-sm pagination-btn" disabled>Siguiente</button>`;
        }

        html += '</div>';

        return html;
    }

    /**
     * Genera el HTML de información de paginación
     * @returns {string} HTML de info
     */
    buildInfo() {
        const { currentPage, totalPages, totalItems } = this.state;

        return `
            <div class="pagination-info">
                Mostrando página ${currentPage} de ${totalPages} (${totalItems} total)
            </div>
        `;
    }

    /**
     * Calcula el rango de páginas a mostrar
     * @returns {Array} Array con números de página y elipsis
     */
    getPageRange() {
        const { currentPage, totalPages } = this.state;
        const { delta } = this.config;
        const range = [];
        const rangeWithDots = [];

        // Siempre incluir primera y última página
        // Incluir páginas dentro del delta de la página actual
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= currentPage - delta && i <= currentPage + delta)) {
                range.push(i);
            }
        }

        // Agregar elipsis donde haya gaps
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
     * Adjunta event listeners a los botones
     */
    attachEventListeners() {
        if (!this.elements.container) return;

        const buttons = this.elements.container.querySelectorAll('.pagination-btn[data-page]');
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const page = parseInt(btn.dataset.page);
                if (page && !btn.disabled) {
                    this.goToPage(page);
                }
            });
        });
    }

    /**
     * Navega a una página específica
     * @param {number} page - Número de página
     */
    goToPage(page) {
        if (page < 1 || page > this.state.totalPages) return;
        if (page === this.state.currentPage) return;

        this.state.currentPage = page;

        if (this.config.onChange) {
            this.config.onChange(page);
        }
    }

    /**
     * Va a la primera página
     */
    goToFirst() {
        this.goToPage(1);
    }

    /**
     * Va a la última página
     */
    goToLast() {
        this.goToPage(this.state.totalPages);
    }

    /**
     * Va a la página siguiente
     */
    goToNext() {
        if (this.state.hasNext) {
            this.goToPage(this.state.currentPage + 1);
        }
    }

    /**
     * Va a la página anterior
     */
    goToPrevious() {
        if (this.state.hasPrevious) {
            this.goToPage(this.state.currentPage - 1);
        }
    }

    /**
     * Obtiene la página actual
     * @returns {number} Número de página actual
     */
    getCurrentPage() {
        return this.state.currentPage;
    }

    /**
     * Obtiene el total de páginas
     * @returns {number} Total de páginas
     */
    getTotalPages() {
        return this.state.totalPages;
    }

    /**
     * Verifica si hay página siguiente
     * @returns {boolean}
     */
    hasNext() {
        return this.state.hasNext;
    }

    /**
     * Verifica si hay página anterior
     * @returns {boolean}
     */
    hasPrevious() {
        return this.state.hasPrevious;
    }

    /**
     * Resetea a la primera página
     */
    reset() {
        this.state.currentPage = 1;
        this.render();
    }
}

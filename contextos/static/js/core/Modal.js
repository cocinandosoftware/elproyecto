/**
 * Sistema de modales genérico
 * Gestiona modales de confirmación y notificación
 */

export class Modal {
    /**
     * Constructor del modal
     * @param {string} modalId - ID del elemento modal en el DOM
     */
    constructor(modalId) {
        this.modalId = modalId;
        this.modal = null;
        this.onConfirmCallback = null;
    }

    /**
     * Genera el HTML del modal
     * @returns {HTMLElement} Elemento modal
     */
    generarHTML() {
        const modal = document.createElement('div');
        modal.id = this.modalId;
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title"></h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body"></div>
                <div class="modal-footer">
                    <button class="btn btn-cancel">Cancelar</button>
                    <button class="btn btn-primary modal-confirm">Confirmar</button>
                </div>
            </div>
        `;
        return modal;
    }

    /**
     * Inicializa el modal (crea si no existe)
     */
    init() {
        this.modal = document.getElementById(this.modalId);
        
        if (!this.modal) {
            this.modal = this.generarHTML();
            document.body.appendChild(this.modal);
        }
        
        this.setupEventListeners();
    }

    /**
     * Configura los event listeners del modal
     */
    setupEventListeners() {
        // Botón cerrar (X)
        const closeBtn = this.modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.onclick = () => this.hide();
        }

        // Botón cancelar
        const cancelBtn = this.modal.querySelector('.btn-cancel');
        if (cancelBtn) {
            cancelBtn.onclick = () => this.hide();
        }

        // Botón confirmar
        const confirmBtn = this.modal.querySelector('.modal-confirm');
        if (confirmBtn) {
            confirmBtn.onclick = () => this.handleConfirm();
        }

        // Click fuera del modal
        this.modal.onclick = (event) => {
            if (event.target === this.modal) {
                this.hide();
            }
        };

        // Tecla Escape
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && this.isVisible()) {
                this.hide();
            }
        });
    }

    /**
     * Muestra el modal con contenido personalizado
     * @param {string} title - Título del modal
     * @param {string} content - Contenido HTML del modal
     * @param {Object} options - Opciones adicionales
     */
    show(title, content, options = {}) {
        if (!this.modal) this.init();

        const modalTitle = this.modal.querySelector('.modal-title');
        const modalBody = this.modal.querySelector('.modal-body');
        const confirmBtn = this.modal.querySelector('.modal-confirm');

        if (modalTitle) modalTitle.innerHTML = title;
        if (modalBody) modalBody.innerHTML = content;

        // Aplicar opciones
        if (options.confirmText && confirmBtn) {
            confirmBtn.textContent = options.confirmText;
        }
        if (options.confirmClass && confirmBtn) {
            confirmBtn.className = `btn ${options.confirmClass}`;
        }

        this.modal.style.display = 'flex';
    }

    /**
     * Oculta el modal
     */
    hide() {
        if (this.modal) {
            this.modal.style.display = 'none';
            this.onConfirmCallback = null;
        }
    }

    /**
     * Verifica si el modal está visible
     * @returns {boolean}
     */
    isVisible() {
        return this.modal && this.modal.style.display === 'flex';
    }

    /**
     * Modal de confirmación
     * @param {string} message - Mensaje de confirmación
     * @param {Function} onConfirm - Callback al confirmar
     * @param {Object} options - Opciones adicionales
     */
    confirm(message, onConfirm, options = {}) {
        this.onConfirmCallback = onConfirm;

        const defaultOptions = {
            title: '⚠️ Confirmar Acción',
            confirmText: 'Confirmar',
            confirmClass: 'btn-danger',
            ...options
        };

        this.show(
            defaultOptions.title,
            `<p>${message}</p>`,
            {
                confirmText: defaultOptions.confirmText,
                confirmClass: defaultOptions.confirmClass
            }
        );
    }

    /**
     * Maneja la confirmación del modal
     */
    async handleConfirm() {
        if (this.onConfirmCallback) {
            const confirmBtn = this.modal.querySelector('.modal-confirm');
            const cancelBtn = this.modal.querySelector('.btn-cancel');
            
            // Deshabilitar botones durante la ejecución
            if (confirmBtn) confirmBtn.disabled = true;
            if (cancelBtn) cancelBtn.disabled = true;

            try {
                await this.onConfirmCallback();
            } finally {
                if (confirmBtn) confirmBtn.disabled = false;
                if (cancelBtn) cancelBtn.disabled = false;
            }
        }
    }

    /**
     * Destruye el modal del DOM
     */
    destroy() {
        if (this.modal) {
            this.modal.remove();
            this.modal = null;
        }
    }
}


/**
 * Modal especializado para formularios
 * Extiende Modal.js para soportar generación dinámica de formularios HTML
 */

import { Modal } from './Modal.js';

export class FormModal extends Modal {
    /**
     * Constructor del modal de formulario
     * @param {string} modalId - ID del elemento modal en el DOM
     */
    constructor(modalId) {
        super(modalId);
        this.formConfig = null;
        this.onSubmitCallback = null;
    }

    /**
     * Genera el HTML del modal con soporte para formularios
     * @returns {HTMLElement} Elemento modal
     */
    generarHTML() {
        const modal = document.createElement('div');
        modal.id = this.modalId;
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content modal-form">
                <div class="modal-header">
                    <h3 class="modal-title"></h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <form class="modal-form-content" id="${this.modalId}-form" autocomplete="off">
                        <!-- Campos del formulario generados dinámicamente -->
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary btn-cancel">Cancelar</button>
                    <button type="button" class="btn btn-primary modal-submit">Guardar</button>
                </div>
            </div>
        `;
        return modal;
    }

    /**
     * Configura los event listeners específicos del formulario
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

        // Botón submit del formulario
        const submitBtn = this.modal.querySelector('.modal-submit');
        if (submitBtn) {
            submitBtn.onclick = () => this.handleSubmit();
        }

        // NO cerrar al hacer click fuera del modal (para evitar pérdida de datos)
        // Los usuarios deben usar el botón X o Cancelar explícitamente
        this.modal.onclick = null;

        // Tecla Escape para cerrar
        const escapeHandler = (event) => {
            if (event.key === 'Escape' && this.isVisible()) {
                this.hide();
            }
        };
        document.addEventListener('keydown', escapeHandler);

        // Submit con Enter en inputs (excepto textarea)
        const form = this.modal.querySelector('.modal-form-content');
        if (form) {
            form.addEventListener('keypress', (event) => {
                if (event.key === 'Enter' && event.target.tagName !== 'TEXTAREA') {
                    event.preventDefault();
                    this.handleSubmit();
                }
            });
        }
    }

    /**
     * Muestra el modal con un formulario dinámico
     * @param {string} title - Título del modal
     * @param {Object} formConfig - Configuración del formulario
     * @param {Function} onSubmitCallback - Callback al enviar el formulario
     */
    showForm(title, formConfig, onSubmitCallback) {
        if (!this.modal) this.init();

        this.formConfig = formConfig;
        this.onSubmitCallback = onSubmitCallback;

        // Actualizar título
        const modalTitle = this.modal.querySelector('.modal-title');
        if (modalTitle) {
            modalTitle.innerHTML = title;
        }

        // Generar formulario
        const form = this.modal.querySelector('.modal-form-content');
        if (form) {
            form.innerHTML = this.renderFormFields(formConfig.fields);
        }

        // Actualizar textos de botones
        const submitBtn = this.modal.querySelector('.modal-submit');
        const cancelBtn = this.modal.querySelector('.btn-cancel');
        
        if (submitBtn && formConfig.submitText) {
            submitBtn.textContent = formConfig.submitText;
        }
        if (cancelBtn && formConfig.cancelText) {
            cancelBtn.textContent = formConfig.cancelText;
        }

        // Limpiar errores previos
        this.clearErrors();

        // Mostrar modal
        this.modal.style.display = 'flex';

        // Focus en el primer input
        setTimeout(() => {
            const firstInput = form.querySelector('input:not([type="checkbox"]), select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        }, 100);

        // Agregar listeners para limpiar errores al escribir
        this.setupErrorClearListeners();
    }

    /**
     * Renderiza los campos del formulario según configuración
     * @param {Array} fields - Array de configuración de campos
     * @returns {string} HTML de los campos
     */
    renderFormFields(fields) {
        return fields.map(field => {
            const requiredAttr = field.required ? 'required' : '';
            const requiredLabel = field.required ? '<span class="required-indicator">*</span>' : '';
            
            let inputHTML = '';
            
            switch (field.type) {
                case 'text':
                case 'email':
                case 'password':
                case 'tel':
                    // Determinar el valor de autocomplete apropiado
                    let autocompleteValue = 'off';
                    if (field.type === 'password') {
                        autocompleteValue = 'new-password';
                    } else if (field.name === 'username') {
                        autocompleteValue = 'off';
                    } else if (field.name === 'email') {
                        autocompleteValue = 'off';
                    }
                    
                    inputHTML = `
                        <input 
                            type="${field.type}" 
                            id="${field.name}" 
                            name="${field.name}" 
                            class="form-input" 
                            placeholder="${field.placeholder || ''}"
                            value="${field.value || ''}"
                            autocomplete="${autocompleteValue}"
                            data-lpignore="true"
                            data-form-type="other"
                            ${requiredAttr}
                        >
                    `;
                    break;
                
                case 'select':
                    const options = field.options.map(opt => 
                        `<option value="${opt.value}" ${field.value === opt.value ? 'selected' : ''}>${opt.label}</option>`
                    ).join('');
                    inputHTML = `
                        <select 
                            id="${field.name}" 
                            name="${field.name}" 
                            class="form-select"
                            ${requiredAttr}
                        >
                            <option value="">Seleccionar...</option>
                            ${options}
                        </select>
                    `;
                    break;
                
                case 'textarea':
                    inputHTML = `
                        <textarea 
                            id="${field.name}" 
                            name="${field.name}" 
                            class="form-input form-textarea" 
                            placeholder="${field.placeholder || ''}"
                            rows="${field.rows || 3}"
                            autocomplete="off"
                            data-lpignore="true"
                            data-form-type="other"
                            ${requiredAttr}
                        >${field.value || ''}</textarea>
                    `;
                    break;
                
                case 'checkbox':
                    inputHTML = `
                        <div class="form-checkbox-group">
                            <input 
                                type="checkbox" 
                                id="${field.name}" 
                                name="${field.name}" 
                                class="form-checkbox"
                                ${field.value ? 'checked' : ''}
                            >
                            <label for="${field.name}" class="checkbox-label">${field.label}</label>
                        </div>
                    `;
                    return `
                        <div class="form-group form-group-checkbox" data-field="${field.name}">
                            ${inputHTML}
                            <div class="form-error" id="${field.name}-error"></div>
                        </div>
                    `;
                
                default:
                    inputHTML = `
                        <input 
                            type="text" 
                            id="${field.name}" 
                            name="${field.name}" 
                            class="form-input"
                            value="${field.value || ''}"
                            autocomplete="off"
                            data-lpignore="true"
                            data-form-type="other"
                            ${requiredAttr}
                        >
                    `;
            }
            
            return `
                <div class="form-group" data-field="${field.name}">
                    <label for="${field.name}" class="form-label">
                        ${field.label}${requiredLabel}
                    </label>
                    ${inputHTML}
                    <div class="form-error" id="${field.name}-error"></div>
                </div>
            `;
        }).join('');
    }

    /**
     * Obtiene los datos del formulario
     * @returns {Object} Objeto con los valores del formulario
     */
    getFormData() {
        const form = this.modal.querySelector('.modal-form-content');
        if (!form) return {};

        const formData = {};
        const inputs = form.querySelectorAll('input, select, textarea');

        inputs.forEach(input => {
            if (input.type === 'checkbox') {
                formData[input.name] = input.checked;
            } else {
                formData[input.name] = input.value;
            }
        });

        return formData;
    }

    /**
     * Muestra errores de validación en los campos
     * @param {Object} errors - Objeto con errores por campo {campo: ['error1', 'error2']}
     */
    showErrors(errors) {
        this.clearErrors();

        Object.keys(errors).forEach(fieldName => {
            const errorMessages = errors[fieldName];
            const errorContainer = this.modal.querySelector(`#${fieldName}-error`);
            const inputElement = this.modal.querySelector(`#${fieldName}`);
            const formGroup = this.modal.querySelector(`[data-field="${fieldName}"]`);

            if (errorContainer && errorMessages.length > 0) {
                errorContainer.textContent = errorMessages.join(', ');
                errorContainer.style.display = 'block';
            }

            if (inputElement) {
                inputElement.classList.add('error');
            }

            if (formGroup) {
                formGroup.classList.add('has-error');
            }
        });

        // Scroll al primer error
        const firstError = this.modal.querySelector('.has-error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    /**
     * Limpia todos los errores de validación
     */
    clearErrors() {
        const errorContainers = this.modal.querySelectorAll('.form-error');
        errorContainers.forEach(container => {
            container.textContent = '';
            container.style.display = 'none';
        });

        const errorInputs = this.modal.querySelectorAll('.form-input.error, .form-select.error');
        errorInputs.forEach(input => {
            input.classList.remove('error');
        });

        const errorGroups = this.modal.querySelectorAll('.form-group.has-error');
        errorGroups.forEach(group => {
            group.classList.remove('has-error');
        });
    }

    /**
     * Configura listeners para limpiar errores al escribir
     */
    setupErrorClearListeners() {
        const inputs = this.modal.querySelectorAll('.form-input, .form-select, .form-checkbox');
        
        inputs.forEach(input => {
            const clearError = () => {
                const fieldName = input.name;
                const errorContainer = this.modal.querySelector(`#${fieldName}-error`);
                const formGroup = this.modal.querySelector(`[data-field="${fieldName}"]`);

                if (errorContainer) {
                    errorContainer.textContent = '';
                    errorContainer.style.display = 'none';
                }

                input.classList.remove('error');

                if (formGroup) {
                    formGroup.classList.remove('has-error');
                }
            };

            input.addEventListener('input', clearError);
            input.addEventListener('change', clearError);
        });
    }

    /**
     * Establece el estado de carga del formulario
     * @param {boolean} isLoading - Si está cargando o no
     */
    setLoading(isLoading) {
        const submitBtn = this.modal.querySelector('.modal-submit');
        const cancelBtn = this.modal.querySelector('.btn-cancel');
        const closeBtn = this.modal.querySelector('.modal-close');
        const inputs = this.modal.querySelectorAll('.form-input, .form-select, .form-checkbox');

        if (isLoading) {
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                submitBtn.dataset.originalText = submitBtn.textContent;
                submitBtn.textContent = 'Guardando...';
            }
            if (cancelBtn) cancelBtn.disabled = true;
            if (closeBtn) closeBtn.disabled = true;
            inputs.forEach(input => input.disabled = true);
        } else {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
                if (submitBtn.dataset.originalText) {
                    submitBtn.textContent = submitBtn.dataset.originalText;
                }
            }
            if (cancelBtn) cancelBtn.disabled = false;
            if (closeBtn) closeBtn.disabled = false;
            inputs.forEach(input => input.disabled = false);
        }
    }

    /**
     * Maneja el envío del formulario
     */
    async handleSubmit() {
        if (this.onSubmitCallback) {
            this.clearErrors();
            const formData = this.getFormData();
            
            try {
                await this.onSubmitCallback(formData);
            } catch (error) {
                console.error('Error en submit del formulario:', error);
            }
        }
    }

    /**
     * Oculta el modal y limpia el estado
     */
    hide() {
        super.hide();
        this.formConfig = null;
        this.onSubmitCallback = null;
        this.clearErrors();
        this.setLoading(false);
    }
}

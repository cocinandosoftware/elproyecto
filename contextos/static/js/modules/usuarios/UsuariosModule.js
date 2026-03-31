/**
 * Módulo de Usuarios
 * Gestión completa de usuarios: listado, creación, edición y eliminación
 * Implementación específica de DataTable para usuarios
 */

import { DataTable } from '../../core/DataTable.js';
import { Modal } from '../../core/Modal.js';
import { FormModal } from '../../core/FormModal.js';
import { KPISection } from '../../components/KPISection.js';
import { Utils } from '../../core/Utils.js';

export class UsuariosModule extends DataTable {
    /**
     * Constructor
     */
    constructor() {
        super({
            apiUrl: '/backoffice/usuarios/api/buscar/',
            tableSelector: '.data-table',
            paginationSelector: '.pagination',
            searchInputSelector: '#filter_busqueda',
            sortableHeaders: ['id', 'username', 'nombre_completo', 'email', 'tipo_usuario', 'activo', 'fecha_ultimo_acceso']
        });

        // Modal de confirmación para eliminar
        this.deleteModal = null;

        // Modal de formulario para crear/editar
        this.formModal = null;

        // KPIs
        this.kpiSection = null;

        // Usuario a eliminar (contexto)
        this.usuarioToDelete = null;

        // Usuario a editar (contexto)
        this.usuarioToEdit = null;
    }

    /**
     * Inicializa el módulo de usuarios
     */
    async init() {
        this.initKPIs();
        this.initModals();
        await super.init();
    }

    /**
     * Inicializa los KPIs
     */
    initKPIs() {
        this.kpiSection = new KPISection({
            containerSelector: '.kpis-section',
            kpis: [
                { id: 'total', label: 'Total Usuarios', value: 0, icon: '👥', color: 'primary' },
                { id: 'admins', label: 'Administradores', value: 0, icon: '👑', color: 'danger' },
                { id: 'clientes', label: 'Clientes', value: 0, icon: '👤', color: 'success' },
                { id: 'desarrolladores', label: 'Desarrolladores', value: 0, icon: '💻', color: 'info' }
            ]
        });
        this.kpiSection.init();
    }

    /**
     * Inicializa los modales (confirmación y formulario)
     */
    initModals() {
        this.deleteModal = new Modal('confirmDeleteModal');
        this.deleteModal.init();

        this.formModal = new FormModal('usuarioFormModal');
        this.formModal.init();
    }

    /**
     * Implementación del método abstracto buildRow
     * Genera el HTML de una fila de usuario
     * @param {Object} usuario - Datos del usuario
     * @returns {string} HTML de la fila
     */
    buildRow(usuario) {
        const estadoBadge = usuario.activo 
            ? '<span class="badge badge-success">Activo</span>'
            : '<span class="badge badge-warning">Inactivo</span>';

        const tipoUsuario = this.formatTipoUsuario(usuario.tipo_usuario);

        const lastLogin = usuario.fecha_ultimo_acceso || '<em>Nunca</em>';

        const email = Utils.escapeQuotes(usuario.email);
        const fullName = Utils.escapeQuotes(usuario.nombre_completo);

        return `
            <td>${usuario.id}</td>
            <td><strong>${usuario.username}</strong></td>
            <td><strong>${usuario.nombre_completo}</strong></td>
            <td>${usuario.email}</td>
            <td>${tipoUsuario}</td>
            <td>${estadoBadge}</td>
            <td>${usuario.telefono || '—'}</td>
            <td>${lastLogin}</td>
            <td class="actions">
                <a href="/backoffice/usuarios/${usuario.id}/editar/" 
                   class="btn btn-sm btn-primary" 
                   title="Editar">
                    ✏️
                </a>
                <button class="btn btn-sm btn-danger btn-delete" 
                        data-user-id="${usuario.id}" 
                        data-user-email="${email}"
                        data-user-name="${fullName}"
                        title="Eliminar">
                    🗑️
                </button>
            </td>
        `;
    }

    /**
     * Formatea el tipo de usuario
     * @param {string} tipo - Tipo de usuario
     * @returns {string} Tipo formateado
     */
    formatTipoUsuario(tipo) {
        const tipos = {
            'admin': '👑 Admin',
            'cliente': '👤 Cliente',
            'desarrollador': '💻 Desarrollador'
        };
        return tipos[tipo] || tipo;
    }

    /**
     * Implementación del método abstracto getFilters
     * Obtiene los filtros específicos de usuarios
     * @returns {Object} Filtros a aplicar
     */
    getFilters() {
        const filters = { ...this.state.filters };

        // Filtro de búsqueda
        const searchInput = document.getElementById('filter_busqueda');
        if (searchInput?.value.trim()) {
            filters.filter_busqueda = searchInput.value.trim();
        }

        // Filtro de tipo de usuario
        const tipoSelect = document.getElementById('filter_tipo_usuario');
        if (tipoSelect?.value) {
            filters.filter_tipo_usuario = tipoSelect.value;
        }

        // Filtro de estado
        const estadoSelect = document.getElementById('filter_estado');
        if (estadoSelect?.value !== '') {
            filters.filter_estado = estadoSelect.value;
        }

        return filters;
    }

    /**
     * Sobrescribe setupEventListeners para desactivar búsqueda automática.
     * La búsqueda se activa solo con el botón "Buscar"
     */
    setupEventListeners() {
        // NO agregar listener de búsqueda automática en el input
        // Solo mantener la ordenación en headers
        this.setupSortingHeaders();

        // Event listeners personalizados (sin búsqueda automática)
        this.setupCustomListeners();
    }

    /**
     * Sobrescribe setupCustomListeners para NO activar búsqueda automática.
     * La búsqueda se activa solo con el botón "Buscar"
     */
    setupCustomListeners() {
        // NO agregar listeners de cambio automático
        // El usuario debe hacer click en "Buscar" explícitamente
    }

    /**
     * Maneja el evento de búsqueda manual (botón Buscar)
     */
    async handleBuscar() {
        this.state.currentPage = 1;
        await this.loadData();
    }

    /**
     * Sobrescribe attachRowEventListeners para botones de acción
     */
    attachRowEventListeners() {
        // Los botones de editar ahora son enlaces, no necesitan event listeners
        
        // Botones de eliminar
        const deleteButtons = document.querySelectorAll('.btn-delete');
        deleteButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const userId = btn.dataset.userId;
                const userEmail = btn.dataset.userEmail;
                const userName = btn.dataset.userName;
                this.handleDelete(userId, userEmail, userName);
            });
        });
    }

    /**
     * Maneja la creación de un nuevo usuario
     * Abre el modal con formulario vacío
     */
    handleCreate() {
        const formConfig = {
            fields: [
                { name: 'username', label: 'Nombre de Usuario', type: 'text', required: true, placeholder: 'usuario123' },
                { name: 'email', label: 'Email', type: 'email', required: true, placeholder: 'usuario@ejemplo.com' },
                { name: 'password', label: 'Contraseña', type: 'password', required: true, placeholder: 'Mínimo 8 caracteres' },
                { name: 'first_name', label: 'Nombre', type: 'text', placeholder: 'Juan' },
                { name: 'last_name', label: 'Apellidos', type: 'text', placeholder: 'Pérez García' },
                { 
                    name: 'tipo_usuario', 
                    label: 'Tipo de Usuario', 
                    type: 'select', 
                    required: true,
                    options: [
                        { value: 'admin', label: '👑 Administrador' },
                        { value: 'cliente', label: '👤 Cliente' },
                        { value: 'desarrollador', label: '💻 Desarrollador' }
                    ]
                },
                { name: 'telefono', label: 'Teléfono', type: 'tel', placeholder: '+34 600 000 000' },
                { name: 'activo', label: 'Usuario Activo', type: 'checkbox', value: true }
            ],
            submitText: '➕ Crear Usuario',
            cancelText: 'Cancelar'
        };

        this.formModal.showForm(
            '➕ Crear Nuevo Usuario',
            formConfig,
            async (formData) => await this.submitCreateForm(formData)
        );
    }

    /**
     * Maneja la eliminación de un usuario
     * @param {string} userId - ID del usuario
     * @param {string} userEmail - Email del usuario
     * @param {string} userName - Nombre del usuario
     */
    handleDelete(userId, userEmail, userName) {
        this.usuarioToDelete = userId;

        this.deleteModal.confirm(
            `
            <p><strong>¿Estás seguro de que deseas eliminar este usuario?</strong></p>
            <p>Usuario: <strong>${userName}</strong><br>Email: <strong>${userEmail}</strong></p>
            <p class="text-warning">⚠️ Esta acción no se puede deshacer.</p>
            `,
            async () => await this.confirmDelete(),
            {
                title: '🗑️ Eliminar Usuario',
                confirmText: 'Sí, eliminar',
                confirmClass: 'btn-danger'
            }
        );
    }

    /**
     * Confirma la eliminación del usuario
     */
    async confirmDelete() {
        if (!this.usuarioToDelete) return;

        try {
            await this.apiClient.post(`/backoffice/usuarios/eliminar/${this.usuarioToDelete}/`, {});
            
            Utils.mostrarMensaje('success', 'Usuario eliminado correctamente');
            this.deleteModal.hide();
            this.usuarioToDelete = null;

            // Recargar datos
            await this.refresh();

        } catch (error) {
            console.error('Error eliminando usuario:', error);
            Utils.mostrarMensaje('error', error.message || 'Error al eliminar el usuario');
        }
    }

    /**
     * Actualiza los KPIs con los datos recibidos
     * @param {Object} kpis - Datos de KPIs
     */
    updateKPIs(kpis) {
        if (this.kpiSection && kpis) {
            this.kpiSection.updateAll({
                total: kpis.total || 0,
                admins: kpis.admins || 0,
                clientes: kpis.clientes || 0,
                desarrolladores: kpis.desarrolladores || 0
            }, { animate: true, highlight: true });
        }
    }

    /**
     * Sobrescribe loadData para incluir actualización de KPIs
     */
    async loadData() {
        // Llamar al método padre
        await super.loadData();
    }

    /**
     * Limpia los filtros y recarga
     */
    async limpiarFiltros() {
        // Reset búsqueda
        const searchInput = document.getElementById('filter_busqueda');
        if (searchInput) searchInput.value = '';

        // Reset tipo de usuario
        const tipoSelect = document.getElementById('filter_tipo_usuario');
        if (tipoSelect) tipoSelect.value = '';

        // Reset estado
        const estadoSelect = document.getElementById('filter_estado');
        if (estadoSelect) estadoSelect.value = '';

        // Llamar al reset del padre
        await this.reset();
    }

    /**
     * Envía el formulario de creación de usuario
     * @param {Object} formData - Datos del formulario
     */
    async submitCreateForm(formData) {
        try {
            // Establecer estado de carga
            this.formModal.setLoading(true);

            // Enviar petición de creación
            const response = await this.apiClient.post('/backoffice/usuarios/api/crear/', formData);

            if (response.success) {
                // Éxito: cerrar modal y mostrar mensaje
                Utils.mostrarMensaje('success', response.message || 'Usuario creado correctamente');
                this.formModal.hide();
                
                // Si hay redirect_url, redirigir a la página de edición completa
                if (response.redirect_url) {
                    setTimeout(() => {
                        window.location.href = response.redirect_url;
                    }, 500);
                } else {
                    // Si no hay redirect, recargar tabla
                    await this.refresh();
                }
            } else {
                // Error: mostrar errores de validación
                if (response.errors) {
                    this.formModal.showErrors(response.errors);
                } else {
                    Utils.mostrarMensaje('error', response.message || 'Error al crear el usuario');
                }
            }

        } catch (error) {
            console.error('Error al crear usuario:', error);
            Utils.mostrarMensaje('error', error.message || 'Error al crear el usuario');
        } finally {
            this.formModal.setLoading(false);
        }
    }
}

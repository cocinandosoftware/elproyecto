/**
 * Tabla de Usuarios
 * Implementación específica de DataTable para gestión de usuarios
 */

import { DataTable } from '../../core/DataTable.js';
import { Modal } from '../../core/Modal.js';
import { KPISection } from '../../components/KPISection.js';
import { Utils } from '../../core/Utils.js';

export class UsuariosTable extends DataTable {
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

        // Modal de confirmación
        this.deleteModal = null;

        // KPIs
        this.kpiSection = null;

        // Usuario a eliminar (contexto)
        this.usuarioToDelete = null;
    }

    /**
     * Inicializa la tabla de usuarios
     */
    async init() {
        this.initKPIs();
        this.initModal();
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
     * Inicializa el modal de confirmación
     */
    initModal() {
        this.deleteModal = new Modal('confirmDeleteModal');
        this.deleteModal.init();
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
                <button class="btn btn-sm btn-primary btn-edit" data-user-id="${usuario.id}" title="Editar">
                    ✏️
                </button>
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
     * Sobrescribe setupCustomListeners para agregar listeners específicos
     */
    setupCustomListeners() {
        // Filtro de tipo de usuario
        const tipoSelect = document.getElementById('filter_tipo_usuario');
        if (tipoSelect) {
            tipoSelect.addEventListener('change', () => this.handleFilterChange());
        }

        // Filtro de estado
        const estadoSelect = document.getElementById('filter_estado');
        if (estadoSelect) {
            estadoSelect.addEventListener('change', () => this.handleFilterChange());
        }
    }

    /**
     * Maneja cambios en los filtros
     */
    async handleFilterChange() {
        this.state.currentPage = 1;
        await this.loadData();
    }

    /**
     * Sobrescribe attachRowEventListeners para botones de acción
     */
    attachRowEventListeners() {
        // Botones de editar
        const editButtons = document.querySelectorAll('.btn-edit');
        editButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const userId = btn.dataset.userId;
                this.handleEdit(userId);
            });
        });

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
     * Maneja la edición de un usuario
     * @param {string} userId - ID del usuario
     */
    handleEdit(userId) {
        window.location.href = `/backoffice/usuarios/${userId}/editar/`;
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
}

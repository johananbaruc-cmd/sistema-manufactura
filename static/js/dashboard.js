// static/js/dashboard.js

// Cargar estadísticas
async function loadStats() {
    try {
        const response = await fetch('/api/dashboard/stats');
        const stats = await response.json();
        
        document.getElementById('total-productos').textContent = stats.total_productos || 0;
        document.getElementById('total-maquinas').textContent = stats.total_maquinas || 0;
        document.getElementById('total-producciones').textContent = stats.total_producciones || 0;
        document.getElementById('total-defectos').textContent = stats.total_defectos || 0;
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
    }
}

// Gráfico: Producción vs Defectos
async function loadProduccionChart() {
    try {
        const response = await fetch('/api/dashboard/produccion-ultimos-dias?dias=30');
        const data = await response.json();
        
        const ctx = document.getElementById('produccionChart').getContext('2d');
        const labels = data.map(d => d._id);
        const produccion = data.map(d => d.total);
        const defectos = data.map(d => d.defectos);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Producción',
                        data: produccion,
                        backgroundColor: 'rgba(52, 152, 219, 0.6)',
                        borderColor: 'rgba(52, 152, 219, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Defectos',
                        data: defectos,
                        backgroundColor: 'rgba(231, 76, 60, 0.6)',
                        borderColor: 'rgba(231, 76, 60, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error cargando gráfico de producción:', error);
    }
}

// Gráfico: Estado de Máquinas
async function loadEstadoMaquinasChart() {
    try {
        const response = await fetch('/api/dashboard/estado-maquinas');
        const data = await response.json();
        
        const ctx = document.getElementById('estadoMaquinasChart').getContext('2d');
        const labels = data.map(d => d._id);
        const values = data.map(d => d.count);
        const colors = {
            'operando': '#27ae60',
            'mantenimiento': '#f39c12',
            'parada': '#e74c3c'
        };
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: labels.map(l => colors[l] || '#3498db'),
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error cargando gráfico de estado de máquinas:', error);
    }
}

// Gráfico: Defectos por Producto
async function loadDefectosProductoChart() {
    try {
        const response = await fetch('/api/dashboard/defectos-por-producto');
        const data = await response.json();
        
        const ctx = document.getElementById('defectosProductoChart').getContext('2d');
        const labels = data.map(d => d.producto_nombre);
        const values = data.map(d => d.total_defectos);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Defectos',
                    data: values,
                    backgroundColor: 'rgba(231, 76, 60, 0.6)',
                    borderColor: 'rgba(231, 76, 60, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error cargando gráfico de defectos por producto:', error);
    }
}

// Gráfico: Top Productos
async function loadTopProductosChart() {
    try {
        const response = await fetch('/api/dashboard/top-productos');
        const data = await response.json();
        
        const ctx = document.getElementById('topProductosChart').getContext('2d');
        const labels = data.map(d => d.producto_nombre);
        const values = data.map(d => d.total_producido);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Unidades Producidas',
                    data: values,
                    backgroundColor: [
                        'rgba(52, 152, 219, 0.8)',
                        'rgba(46, 204, 113, 0.8)',
                        'rgba(241, 196, 15, 0.8)',
                        'rgba(231, 76, 60, 0.8)',
                        'rgba(155, 89, 182, 0.8)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error cargando gráfico de top productos:', error);
    }
}

// Cargar últimas actividades
async function loadUltimasActividades() {
    try {
        // Cargar últimas producciones
        const response = await fetch('/api/produccion');
        const data = await response.json();
        
        const container = document.getElementById('ultimas-actividades');
        if (data.length === 0) {
            container.innerHTML = '<p class="text-muted">No hay actividades recientes</p>';
            return;
        }
        
        let html = '<ul class="list-group list-group-flush">';
        data.slice(0, 10).forEach(item => {
            const fecha = new Date(item.fecha).toLocaleString('es-ES');
            html += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <i class="fas fa-gears text-primary me-2"></i>
                        <strong>${item.producto_nombre || 'Producto'}</strong>
                        <span class="text-muted ms-2">- ${item.cantidad_producida} unidades</span>
                    </div>
                    <div>
                        <span class="badge ${item.estado === 'completado' ? 'bg-success' : 'bg-warning'}">${item.estado || 'N/A'}</span>
                        <small class="text-muted ms-2">${fecha}</small>
                    </div>
                </li>
            `;
        });
        html += '</ul>';
        container.innerHTML = html;
    } catch (error) {
        console.error('Error cargando últimas actividades:', error);
    }
}

// Inicializar
document.addEventListener('DOMContentLoaded', async function() {
    await loadStats();
    await loadProduccionChart();
    await loadEstadoMaquinasChart();
    await loadDefectosProductoChart();
    await loadTopProductosChart();
    await loadUltimasActividades();
});
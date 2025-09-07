// Reports JavaScript functionality
let statusChart, priorityChart, categoryChart, timelineChart;

// Color schemes for charts
const colors = {
    primary: ['#0d6efd', '#6610f2', '#6f42c1', '#d63384', '#dc3545'],
    success: ['#198754', '#20c997', '#0dcaf0', '#fd7e14', '#ffc107'],
    warm: ['#fd7e14', '#ffc107', '#198754', '#0dcaf0', '#6f42c1']
};

async function loadReports() {
    try {
        // Load ticket statistics
        const statsResponse = await fetch('/api/stats/tickets');
        const statsData = await statsResponse.json();
        
        // Load timeline data
        const timelineResponse = await fetch('/api/stats/timeline');
        const timelineData = await timelineResponse.json();
        
        // Load performance data
        const performanceResponse = await fetch('/api/stats/performance');
        const performanceData = await performanceResponse.json();
        
        // Create charts
        createStatusChart(statsData.status);
        createPriorityChart(statsData.priority);
        createCategoryChart(statsData.category);
        createTimelineChart(timelineData);
        displayPerformanceMetrics(performanceData);
        
    } catch (error) {
        console.error('Error loading reports:', error);
        displayError('Failed to load report data. Please try again later.');
    }
}

function createStatusChart(data) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(item => item.label.charAt(0).toUpperCase() + item.label.slice(1).replace('_', ' ')),
            datasets: [{
                data: data.map(item => item.count),
                backgroundColor: colors.primary,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: false
                }
            }
        }
    });
}

function createPriorityChart(data) {
    const ctx = document.getElementById('priorityChart').getContext('2d');
    
    // Custom colors for priorities
    const priorityColors = {
        'urgent': '#dc3545',
        'high': '#fd7e14',
        'medium': '#ffc107',
        'low': '#198754'
    };
    
    const backgroundColors = data.map(item => priorityColors[item.label] || '#6c757d');
    
    priorityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.label.charAt(0).toUpperCase() + item.label.slice(1)),
            datasets: [{
                label: 'Tickets',
                data: data.map(item => item.count),
                backgroundColor: backgroundColors,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function createCategoryChart(data) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    categoryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(item => item.label.replace('_', ' ').split(' ').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ')),
            datasets: [{
                data: data.map(item => item.count),
                backgroundColor: colors.warm,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createTimelineChart(data) {
    const ctx = document.getElementById('timelineChart').getContext('2d');
    timelineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => {
                const date = new Date(item.date);
                return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            }),
            datasets: [{
                label: 'Tickets Created',
                data: data.map(item => item.count),
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function displayPerformanceMetrics(data) {
    const container = document.getElementById('performanceMetrics');
    
    const metricsHtml = `
        <div class="row text-center">
            <div class="col-md-4 mb-3">
                <div class="metric-card">
                    <h3 class="text-primary">${data.avg_resolution_time.toFixed(1)}h</h3>
                    <p class="text-muted mb-0">Avg Resolution Time</p>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="metric-card">
                    <h3 class="text-success">${data.total_resolved}</h3>
                    <p class="text-muted mb-0">Total Resolved</p>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="metric-card">
                    <h3 class="text-info">${data.resolution_rate.toFixed(1)}%</h3>
                    <p class="text-muted mb-0">Resolution Rate</p>
                </div>
            </div>
        </div>
        <div class="mt-3">
            <small class="text-muted">
                <i class="fas fa-info-circle me-1"></i>
                Metrics are calculated based on all historical ticket data.
            </small>
        </div>
    `;
    
    container.innerHTML = metricsHtml;
}

function displayError(message) {
    const containers = ['statusChart', 'priorityChart', 'categoryChart', 'timelineChart'];
    
    containers.forEach(containerId => {
        const container = document.getElementById(containerId);
        if (container) {
            container.parentElement.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-exclamation-triangle fa-2x text-warning mb-2"></i>
                    <p class="text-muted">${message}</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="loadReports()">
                        <i class="fas fa-redo me-1"></i>Retry
                    </button>
                </div>
            `;
        }
    });
    
    // Also update performance metrics
    const performanceContainer = document.getElementById('performanceMetrics');
    if (performanceContainer) {
        performanceContainer.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-exclamation-triangle fa-2x text-warning mb-2"></i>
                <p class="text-muted">${message}</p>
            </div>
        `;
    }
}

// Utility function to format dates
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Export functions for potential external use
window.reportsModule = {
    loadReports,
    createStatusChart,
    createPriorityChart,
    createCategoryChart,
    createTimelineChart,
    displayPerformanceMetrics
};

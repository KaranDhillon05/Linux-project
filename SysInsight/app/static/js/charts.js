/**
 * Chart.js configuration and management
 */

class MetricsBuffer {
    constructor(maxSize = 300) {
        this.maxSize = maxSize;
        this.timestamps = [];
        this.values = [];
    }

    add(timestamp, value) {
        this.timestamps.push(timestamp);
        this.values.push(value);

        if (this.timestamps.length > this.maxSize) {
            this.timestamps.shift();
            this.values.shift();
        }
    }

    getData() {
        return {
            labels: [...this.timestamps],
            data: [...this.values]
        };
    }

    clear() {
        this.timestamps = [];
        this.values = [];
    }
}

class ChartManager {
    constructor() {
        this.charts = {};
        this.buffers = {};
    }

    createLineChart(canvasId, label, color = '#2563eb') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        this.buffers[canvasId] = new MetricsBuffer(300);

        this.charts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: label,
                    data: [],
                    borderColor: color,
                    backgroundColor: color + '20',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 0
                }]
            },
            options: {
                animation: false,
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: true,
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'second',
                            displayFormats: {
                                second: 'HH:mm:ss'
                            }
                        },
                        ticks: {
                            maxRotation: 0,
                            autoSkip: true,
                            maxTicksLimit: 8
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        min: 0,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    updateChart(canvasId, timestamp, value) {
        const buffer = this.buffers[canvasId];
        const chart = this.charts[canvasId];

        if (!buffer || !chart) return;

        buffer.add(new Date(timestamp), value);
        const data = buffer.getData();

        chart.data.labels = data.labels;
        chart.data.datasets[0].data = data.data;
        chart.update('none');
    }

    destroy() {
        Object.values(this.charts).forEach(chart => chart.destroy());
        Object.values(this.buffers).forEach(buffer => buffer.clear());
    }
}

// Export for use in dashboard.js
window.ChartManager = ChartManager;

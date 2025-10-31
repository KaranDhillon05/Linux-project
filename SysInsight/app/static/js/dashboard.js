/**
 * Dashboard real-time data management
 */

class SystemMonitor {
    constructor(apiBaseUrl = '/api', updateInterval = 5000) {
        this.apiBaseUrl = apiBaseUrl;
        this.updateInterval = updateInterval;
        this.chartManager = new ChartManager();
        this.pollingTimer = null;
        this.isConnected = false;
    }

    init() {
        // Create charts
        this.chartManager.createLineChart('cpu-chart', 'CPU %', '#2563eb');
        this.chartManager.createLineChart('memory-chart', 'Memory %', '#8b5cf6');
        this.chartManager.createLineChart('disk-chart', 'Disk %', '#f59e0b');

        // Start polling
        this.startPolling();

        // Handle page visibility
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopPolling();
            } else {
                this.startPolling();
            }
        });
    }

    async fetchMetrics() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/metrics/all`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                timeout: 5000
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.updateConnectionStatus(true);
            this.handleMetricsUpdate(data);

        } catch (error) {
            console.error('Failed to fetch metrics:', error);
            this.updateConnectionStatus(false);
            this.showError('Failed to fetch metrics. Retrying...');
        }
    }

    handleMetricsUpdate(data) {
        const timestamp = data.timestamp;

        // Update CPU
        if (data.cpu && !data.cpu.error) {
            this.updateCPU(data.cpu, timestamp);
        }

        // Update Memory
        if (data.memory && !data.memory.error) {
            this.updateMemory(data.memory, timestamp);
        }

        // Update Disk
        if (data.disk && !data.disk.error) {
            this.updateDisk(data.disk, timestamp);
        }

        // Handle alerts
        if (data.alerts) {
            this.handleAlerts(data.alerts);
        }
    }

    updateCPU(cpuData, timestamp) {
        const percent = cpuData.percent;

        // Update current value
        const valueEl = document.getElementById('cpu-value');
        valueEl.textContent = percent.toFixed(1);
        valueEl.className = this.getValueClass(percent, 70, 85);

        // Update cores info
        if (cpuData.cores) {
            document.getElementById('cpu-cores').textContent =
                `${cpuData.cores.physical}/${cpuData.cores.logical}`;
        }

        // Update chart
        this.chartManager.updateChart('cpu-chart', timestamp, percent);

        // Update timestamp
        this.updateTimestamp('cpu-updated');
    }

    updateMemory(memData, timestamp) {
        const percent = memData.virtual.percent;

        // Update current value
        const valueEl = document.getElementById('memory-value');
        valueEl.textContent = percent.toFixed(1);
        valueEl.className = this.getValueClass(percent, 75, 85);

        // Update stats
        document.getElementById('memory-used').textContent =
            memData.virtual.used_gb.toFixed(1);
        document.getElementById('memory-total').textContent =
            memData.virtual.total_gb.toFixed(1);

        // Update chart
        this.chartManager.updateChart('memory-chart', timestamp, percent);

        // Update timestamp
        this.updateTimestamp('memory-updated');
    }

    updateDisk(diskData, timestamp) {
        if (!diskData.partitions || diskData.partitions.length === 0) {
            return;
        }

        // Find partition with highest usage (typically root)
        const mainPartition = diskData.partitions.reduce((max, p) =>
            p.percent > max.percent ? p : max
        );

        const percent = mainPartition.percent;

        // Update current value
        const valueEl = document.getElementById('disk-value');
        valueEl.textContent = percent.toFixed(1);
        valueEl.className = this.getValueClass(percent, 80, 90);

        // Update stats
        const statsHtml = diskData.partitions.map(p =>
            `<span>${p.mountpoint}: <strong>${p.used_gb.toFixed(1)}/${p.total_gb.toFixed(1)} GB</strong></span>`
        ).join('');
        document.getElementById('disk-stats').innerHTML = statsHtml;

        // Update chart
        this.chartManager.updateChart('disk-chart', timestamp, percent);

        // Update timestamp
        this.updateTimestamp('disk-updated');
    }

    getValueClass(value, warningThreshold, criticalThreshold) {
        if (value >= criticalThreshold) return 'value-large critical';
        if (value >= warningThreshold) return 'value-large warning';
        return 'value-large';
    }

    updateTimestamp(elementId) {
        const now = new Date();
        const timeStr = now.toLocaleTimeString();
        document.getElementById(elementId).textContent = `Updated: ${timeStr}`;
    }

    handleAlerts(alerts) {
        const criticalAlerts = Object.entries(alerts)
            .filter(([key, value]) => value === 'critical')
            .map(([key]) => key.toUpperCase());

        if (criticalAlerts.length > 0) {
            this.showAlert(`Critical: ${criticalAlerts.join(', ')} usage is very high!`);
        }
    }

    showAlert(message) {
        const banner = document.getElementById('alert-banner');
        const messageEl = document.getElementById('alert-message');

        messageEl.textContent = message;
        banner.style.display = 'block';

        // Auto-hide after 10 seconds
        setTimeout(() => {
            this.closeAlert();
        }, 10000);
    }

    closeAlert() {
        const banner = document.getElementById('alert-banner');
        banner.style.display = 'none';
    }

    showError(message) {
        console.error(message);
        // Could show error toast here
    }

    updateConnectionStatus(connected) {
        this.isConnected = connected;
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-text');

        if (connected) {
            statusDot.classList.remove('disconnected');
            statusText.textContent = 'Connected';
        } else {
            statusDot.classList.add('disconnected');
            statusText.textContent = 'Disconnected';
        }
    }

    startPolling() {
        if (this.pollingTimer) return;

        // Fetch immediately
        this.fetchMetrics();

        // Then poll at interval
        this.pollingTimer = setInterval(() => {
            this.fetchMetrics();
        }, this.updateInterval);
    }

    stopPolling() {
        if (this.pollingTimer) {
            clearInterval(this.pollingTimer);
            this.pollingTimer = null;
        }
    }

    destroy() {
        this.stopPolling();
        this.chartManager.destroy();
    }
}

// Make closeAlert available globally for onclick handler
function closeAlert() {
    const banner = document.getElementById('alert-banner');
    banner.style.display = 'none';
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const monitor = new SystemMonitor('/api', 5000);
    monitor.init();

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        monitor.destroy();
    });
});

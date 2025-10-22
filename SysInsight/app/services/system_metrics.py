"""
System metrics collection service using psutil
"""
import psutil
from datetime import datetime
from typing import Dict, List, Any

class SystemMetricsService:
    """Service for collecting system metrics"""

    @staticmethod
    def get_cpu_metrics() -> Dict[str, Any]:
        """
        Collect CPU usage metrics

        Returns:
            Dictionary with CPU metrics
        """
        try:
            return {
                'percent': round(psutil.cpu_percent(interval=1), 2),
                'per_core': [round(x, 2) for x in psutil.cpu_percent(interval=1, percpu=True)],
                'cores': {
                    'physical': psutil.cpu_count(logical=False),
                    'logical': psutil.cpu_count(logical=True)
                },
                'frequency': {
                    'current': round(psutil.cpu_freq().current, 2) if psutil.cpu_freq() else None,
                    'min': round(psutil.cpu_freq().min, 2) if psutil.cpu_freq() else None,
                    'max': round(psutil.cpu_freq().max, 2) if psutil.cpu_freq() else None
                },
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.utcnow().isoformat()}

    @staticmethod
    def get_memory_metrics() -> Dict[str, Any]:
        """
        Collect memory usage metrics

        Returns:
            Dictionary with memory metrics
        """
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                'virtual': {
                    'total_gb': round(mem.total / (1024**3), 2),
                    'available_gb': round(mem.available / (1024**3), 2),
                    'used_gb': round(mem.used / (1024**3), 2),
                    'percent': round(mem.percent, 2)
                },
                'swap': {
                    'total_gb': round(swap.total / (1024**3), 2),
                    'used_gb': round(swap.used / (1024**3), 2),
                    'percent': round(swap.percent, 2)
                },
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.utcnow().isoformat()}

    @staticmethod
    def get_disk_metrics() -> Dict[str, Any]:
        """
        Collect disk usage metrics

        Returns:
            Dictionary with disk metrics
        """
        try:
            partitions = []

            for partition in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    partitions.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total_gb': round(usage.total / (1024**3), 2),
                        'used_gb': round(usage.used / (1024**3), 2),
                        'free_gb': round(usage.free / (1024**3), 2),
                        'percent': round(usage.percent, 2)
                    })
                except PermissionError:
                    continue

            # Disk I/O statistics
            io_counters = psutil.disk_io_counters()
            io_stats = {
                'read_count': io_counters.read_count,
                'write_count': io_counters.write_count,
                'read_mb': round(io_counters.read_bytes / (1024**2), 2),
                'write_mb': round(io_counters.write_bytes / (1024**2), 2)
            } if io_counters else None

            return {
                'partitions': partitions,
                'io_stats': io_stats,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.utcnow().isoformat()}

    @staticmethod
    def get_all_metrics() -> Dict[str, Any]:
        """
        Collect all system metrics

        Returns:
            Dictionary with all metrics
        """
        return {
            'cpu': SystemMetricsService.get_cpu_metrics(),
            'memory': SystemMetricsService.get_memory_metrics(),
            'disk': SystemMetricsService.get_disk_metrics(),
            'timestamp': datetime.utcnow().isoformat()
        }

    @staticmethod
    def evaluate_thresholds(metrics: Dict[str, Any], config) -> Dict[str, str]:
        """
        Evaluate metrics against configured thresholds

        Args:
            metrics: Metrics dictionary
            config: Flask config object

        Returns:
            Dictionary with alert levels
        """
        alerts = {}

        # CPU evaluation
        if 'cpu' in metrics and 'percent' in metrics['cpu']:
            cpu_percent = metrics['cpu']['percent']
            if cpu_percent >= config['CPU_CRITICAL_THRESHOLD']:
                alerts['cpu'] = 'critical'
            elif cpu_percent >= config['CPU_WARNING_THRESHOLD']:
                alerts['cpu'] = 'warning'
            else:
                alerts['cpu'] = 'normal'

        # Memory evaluation
        if 'memory' in metrics and 'virtual' in metrics['memory']:
            mem_percent = metrics['memory']['virtual']['percent']
            if mem_percent >= config['MEMORY_CRITICAL_THRESHOLD']:
                alerts['memory'] = 'critical'
            elif mem_percent >= config['MEMORY_WARNING_THRESHOLD']:
                alerts['memory'] = 'warning'
            else:
                alerts['memory'] = 'normal'

        # Disk evaluation (check highest partition usage)
        if 'disk' in metrics and 'partitions' in metrics['disk']:
            max_disk_percent = max(
                (p['percent'] for p in metrics['disk']['partitions']),
                default=0
            )
            if max_disk_percent >= config['DISK_CRITICAL_THRESHOLD']:
                alerts['disk'] = 'critical'
            elif max_disk_percent >= config['DISK_WARNING_THRESHOLD']:
                alerts['disk'] = 'warning'
            else:
                alerts['disk'] = 'normal'

        return alerts

# Create service instance
system_metrics = SystemMetricsService()

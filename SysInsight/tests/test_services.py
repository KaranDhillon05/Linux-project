"""
Service layer tests
"""
import pytest
from app.services.system_metrics import system_metrics

def test_get_cpu_metrics():
    """Test CPU metrics collection"""
    data = system_metrics.get_cpu_metrics()
    assert 'percent' in data
    assert 'cores' in data
    assert 'timestamp' in data
    assert isinstance(data['percent'], (int, float))
    assert 0 <= data['percent'] <= 100

def test_get_memory_metrics():
    """Test memory metrics collection"""
    data = system_metrics.get_memory_metrics()
    assert 'virtual' in data
    assert 'swap' in data
    assert 'timestamp' in data
    assert 'total_gb' in data['virtual']
    assert 'percent' in data['virtual']

def test_get_disk_metrics():
    """Test disk metrics collection"""
    data = system_metrics.get_disk_metrics()
    assert 'partitions' in data
    assert 'timestamp' in data
    assert isinstance(data['partitions'], list)

def test_get_all_metrics():
    """Test all metrics collection"""
    data = system_metrics.get_all_metrics()
    assert 'cpu' in data
    assert 'memory' in data
    assert 'disk' in data
    assert 'timestamp' in data

def test_evaluate_thresholds():
    """Test threshold evaluation"""
    mock_metrics = {
        'cpu': {'percent': 80},
        'memory': {'virtual': {'percent': 60}},
        'disk': {'partitions': [{'percent': 85}]}
    }
    mock_config = {
        'CPU_WARNING_THRESHOLD': 70,
        'CPU_CRITICAL_THRESHOLD': 85,
        'MEMORY_WARNING_THRESHOLD': 75,
        'MEMORY_CRITICAL_THRESHOLD': 90,
        'DISK_WARNING_THRESHOLD': 80,
        'DISK_CRITICAL_THRESHOLD': 90
    }

    alerts = system_metrics.evaluate_thresholds(mock_metrics, mock_config)
    assert 'cpu' in alerts
    assert alerts['cpu'] == 'warning'
    assert alerts['memory'] == 'normal'
    assert alerts['disk'] == 'warning'

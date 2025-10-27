"""
API endpoint tests
"""
import pytest
import json

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

def test_ready_endpoint(client):
    """Test readiness check endpoint"""
    response = client.get('/ready')
    assert response.status_code in [200, 503]
    data = json.loads(response.data)
    assert 'status' in data

def test_cpu_metrics_endpoint(client):
    """Test CPU metrics endpoint"""
    response = client.get('/api/metrics/cpu')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'percent' in data
    assert 'timestamp' in data

def test_memory_metrics_endpoint(client):
    """Test memory metrics endpoint"""
    response = client.get('/api/metrics/memory')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'virtual' in data
    assert 'timestamp' in data

def test_disk_metrics_endpoint(client):
    """Test disk metrics endpoint"""
    response = client.get('/api/metrics/disk')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'partitions' in data
    assert 'timestamp' in data

def test_all_metrics_endpoint(client):
    """Test all metrics endpoint"""
    response = client.get('/api/metrics/all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'cpu' in data
    assert 'memory' in data
    assert 'disk' in data
    assert 'timestamp' in data

def test_api_404(client):
    """Test API 404 handling"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

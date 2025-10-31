"""
Health check endpoints
"""
from flask import Blueprint, jsonify
from datetime import datetime
import psutil

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
@health_bp.route('/healthz', methods=['GET'])
def health():
    """
    Basic health check endpoint

    Returns:
        JSON response with health status
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'SysInsight',
        'version': '1.0.0'
    }), 200

@health_bp.route('/ready', methods=['GET'])
@health_bp.route('/readyz', methods=['GET'])
def ready():
    """
    Readiness check endpoint with system resource validation

    Returns:
        JSON response with readiness status
    """
    try:
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=0.1)
        mem_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent

        # Determine if system is ready (not overwhelmed)
        is_ready = cpu_percent < 95 and mem_percent < 95 and disk_percent < 95

        status_code = 200 if is_ready else 503

        return jsonify({
            'status': 'ready' if is_ready else 'not_ready',
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {
                'cpu': cpu_percent < 95,
                'memory': mem_percent < 95,
                'disk': disk_percent < 95
            },
            'metrics': {
                'cpu_percent': round(cpu_percent, 2),
                'memory_percent': round(mem_percent, 2),
                'disk_percent': round(disk_percent, 2)
            }
        }), status_code
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

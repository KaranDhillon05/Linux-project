"""
API routes for metrics endpoints
"""
from flask import Blueprint, jsonify, current_app
from app.services.system_metrics import system_metrics

api_bp = Blueprint('api', __name__)

@api_bp.route('/metrics/cpu', methods=['GET'])
def get_cpu():
    """
    Get CPU metrics

    Returns:
        JSON response with CPU data
    """
    try:
        data = system_metrics.get_cpu_metrics()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"CPU metrics error: {e}")
        return jsonify({'error': 'Failed to collect CPU metrics'}), 500

@api_bp.route('/metrics/memory', methods=['GET'])
def get_memory():
    """
    Get memory metrics

    Returns:
        JSON response with memory data
    """
    try:
        data = system_metrics.get_memory_metrics()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Memory metrics error: {e}")
        return jsonify({'error': 'Failed to collect memory metrics'}), 500

@api_bp.route('/metrics/disk', methods=['GET'])
def get_disk():
    """
    Get disk metrics

    Returns:
        JSON response with disk data
    """
    try:
        data = system_metrics.get_disk_metrics()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"Disk metrics error: {e}")
        return jsonify({'error': 'Failed to collect disk metrics'}), 500

@api_bp.route('/metrics/all', methods=['GET'])
def get_all():
    """
    Get all system metrics

    Returns:
        JSON response with all metrics data
    """
    try:
        data = system_metrics.get_all_metrics()

        # Add alert evaluations if enabled
        if current_app.config['ENABLE_ALERTS']:
            alerts = system_metrics.evaluate_thresholds(data, current_app.config)
            data['alerts'] = alerts

        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"All metrics error: {e}")
        return jsonify({'error': 'Failed to collect metrics'}), 500

@api_bp.errorhandler(404)
def api_not_found(error):
    """Handle 404 errors in API"""
    return jsonify({'error': 'Endpoint not found'}), 404

@api_bp.errorhandler(500)
def api_internal_error(error):
    """Handle 500 errors in API"""
    return jsonify({'error': 'Internal server error'}), 500

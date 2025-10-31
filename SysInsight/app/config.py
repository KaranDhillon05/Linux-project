"""
Application configuration classes
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

    # Monitoring settings
    METRICS_INTERVAL = int(os.environ.get('METRICS_INTERVAL', '5'))  # seconds
    METRICS_RETENTION_DAYS = int(os.environ.get('METRICS_RETENTION_DAYS', '7'))

    # Alert thresholds (percentage)
    CPU_WARNING_THRESHOLD = float(os.environ.get('CPU_WARNING', '70'))
    CPU_CRITICAL_THRESHOLD = float(os.environ.get('CPU_CRITICAL', '85'))
    MEMORY_WARNING_THRESHOLD = float(os.environ.get('MEMORY_WARNING', '75'))
    MEMORY_CRITICAL_THRESHOLD = float(os.environ.get('MEMORY_CRITICAL', '90'))
    DISK_WARNING_THRESHOLD = float(os.environ.get('DISK_WARNING', '80'))
    DISK_CRITICAL_THRESHOLD = float(os.environ.get('DISK_CRITICAL', '90'))

    # CORS configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

    # Feature flags
    ENABLE_HISTORICAL_STORAGE = os.environ.get('ENABLE_HISTORICAL', 'false').lower() == 'true'
    ENABLE_ALERTS = os.environ.get('ENABLE_ALERTS', 'false').lower() == 'true'

    # Storage settings
    STORAGE_PATH = os.environ.get('STORAGE_PATH', '/data/metrics.db')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    METRICS_INTERVAL = 2  # Faster updates for development

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # In production, CORS should be restricted
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'https://yourdomain.com').split(',')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    METRICS_INTERVAL = 1

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

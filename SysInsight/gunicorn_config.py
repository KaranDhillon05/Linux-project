"""
Gunicorn production configuration
"""
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 60
keepalive = 5
graceful_timeout = 30

# Use /dev/shm for worker heartbeat
worker_tmp_dir = '/dev/shm'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'sysinsight'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

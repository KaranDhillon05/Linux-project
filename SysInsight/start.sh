#!/bin/bash
# Supervisor script to run Flask app and workload simulator together

echo "=========================================="
echo "🚀 SysInsight Container Startup"
echo "=========================================="

# Start workload simulator in background
echo "📊 Starting workload simulator..."
python3 /home/app/web/workload_simulator.py &
WORKLOAD_PID=$!
echo "   Workload simulator PID: $WORKLOAD_PID"

# Give workload simulator time to start
sleep 2

# Start Gunicorn (main application)
echo "🌐 Starting Gunicorn server..."
exec gunicorn -c gunicorn_config.py wsgi:app

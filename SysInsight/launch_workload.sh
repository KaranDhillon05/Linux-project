#!/bin/bash
# Simple launcher for the workload menu

echo "╔════════════════════════════════════════════════════════╗"
echo "║     SysInsight - Workload Generator Launcher          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if we're inside container or host
if [ -f "/.dockerenv" ]; then
    echo "📦 Running inside Docker container"
    python3 /home/app/web/workload_menu.py
else
    echo "💻 Running on host machine"
    echo ""
    echo "Choose where to run the workload:"
    echo "  1. Inside the Docker container (recommended)"
    echo "  2. On this host machine"
    echo ""
    read -p "Enter choice (1-2): " choice
    
    if [ "$choice" = "1" ]; then
        echo ""
        echo "🐳 Launching workload menu inside container..."
        docker exec -it sysinsight python3 /home/app/web/workload_menu.py
    else
        echo ""
        echo "🖥️  Launching workload menu on host..."
        python3 workload_menu.py
    fi
fi

#!/bin/bash
# Snake Game Controller - Start/Stop the game to monitor resource usage

GAME_SCRIPT="/home/app/web/snake_game.py"
PID_FILE="/tmp/snake_game.pid"

show_banner() {
    clear
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║                                                        ║"
    echo "║           SNAKE GAME - Resource Monitor Demo          ║"
    echo "║                                                        ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
}

check_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "✅ Game is RUNNING (PID: $PID)"
            return 0
        else
            echo "❌ Game is STOPPED (stale PID file)"
            rm -f "$PID_FILE"
            return 1
        fi
    else
        echo "❌ Game is STOPPED"
        return 1
    fi
}

start_game() {
    show_banner
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "⚠️  Game is already running (PID: $PID)"
            echo ""
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    echo "🎮 Starting Snake Game..."
    echo ""
    echo "📊 Monitor system resources at:"
    echo "   👉 http://localhost:5001"
    echo ""
    echo "🎯 Game Controls:"
    echo "   • Arrow Keys - Move snake"
    echo "   • ESC - Quit game"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Start the game in background
    python3 "$GAME_SCRIPT" > /tmp/snake_game.log 2>&1 &
    GAME_PID=$!
    echo $GAME_PID > "$PID_FILE"
    
    sleep 2
    
    if ps -p $GAME_PID > /dev/null 2>&1; then
        echo "✅ Game started successfully!"
        echo "   PID: $GAME_PID"
        echo ""
        echo "💡 Tip: Watch your dashboard to see CPU and Memory increase!"
        echo ""
    else
        echo "❌ Failed to start game. Check /tmp/snake_game.log"
        rm -f "$PID_FILE"
    fi
}

stop_game() {
    show_banner
    
    if [ ! -f "$PID_FILE" ]; then
        echo "❌ Game is not running"
        echo ""
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    
    if ! ps -p $PID > /dev/null 2>&1; then
        echo "❌ Game is not running (stale PID)"
        rm -f "$PID_FILE"
        echo ""
        return 1
    fi
    
    echo "🛑 Stopping Snake Game (PID: $PID)..."
    
    kill $PID 2>/dev/null
    sleep 1
    
    # Force kill if still running
    if ps -p $PID > /dev/null 2>&1; then
        kill -9 $PID 2>/dev/null
    fi
    
    rm -f "$PID_FILE"
    
    echo "✅ Game stopped successfully!"
    echo ""
    echo "📊 Check your dashboard to see resources return to normal"
    echo "   http://localhost:5001"
    echo ""
}

show_menu() {
    show_banner
    
    echo "📊 Current Status:"
    check_status
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Choose an option:"
    echo ""
    echo "  1. ▶️  Start Game"
    echo "  2. ⏹️  Stop Game"
    echo "  3. 🔄 Restart Game"
    echo "  4. 📊 Check Status"
    echo "  5. 📈 Show Dashboard URL"
    echo "  6. 📋 View Game Log"
    echo "  7. ❌ Exit"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

show_dashboard_info() {
    show_banner
    echo "📈 SysInsight Dashboard Information"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Dashboard URL:"
    echo "  👉 http://localhost:5001"
    echo ""
    echo "What to watch when game is running:"
    echo "  • CPU Usage increases (game processing)"
    echo "  • Memory Usage increases (game graphics)"
    echo "  • Real-time graph updates"
    echo ""
    echo "API Endpoint:"
    echo "  curl http://localhost:5001/api/metrics/all"
    echo ""
}

view_log() {
    show_banner
    echo "📋 Game Log (last 20 lines)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ -f "/tmp/snake_game.log" ]; then
        tail -n 20 /tmp/snake_game.log
    else
        echo "No log file found. Game hasn't been started yet."
    fi
    
    echo ""
}

# Main menu loop
main() {
    while true; do
        show_menu
        read -p "Enter your choice (1-7): " choice
        
        case $choice in
            1)
                start_game
                read -p "Press ENTER to continue..."
                ;;
            2)
                stop_game
                read -p "Press ENTER to continue..."
                ;;
            3)
                stop_game
                sleep 1
                start_game
                read -p "Press ENTER to continue..."
                ;;
            4)
                show_banner
                echo "📊 Game Status:"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo ""
                check_status
                echo ""
                read -p "Press ENTER to continue..."
                ;;
            5)
                show_dashboard_info
                read -p "Press ENTER to continue..."
                ;;
            6)
                view_log
                read -p "Press ENTER to continue..."
                ;;
            7)
                show_banner
                echo "👋 Goodbye!"
                echo ""
                exit 0
                ;;
            *)
                show_banner
                echo "❌ Invalid choice. Please select 1-7."
                echo ""
                sleep 2
                ;;
        esac
    done
}

# Run main menu
main

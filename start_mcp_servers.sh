#!/bin/bash

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source .env file if it exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    source "$SCRIPT_DIR/.env"
fi

# Configuration with absolute paths
LOG_DIR="$SCRIPT_DIR/logs"
PID_DIR="$SCRIPT_DIR/pids"

# Create necessary directories first
mkdir -p "$LOG_DIR" "$PID_DIR"

# Configure log files
MAIN_LOG="$LOG_DIR/mcp_startup.log"
VLLM_RAG_LOG="$LOG_DIR/vllm_rag.log"
VLLM_MAIN_LOG="$LOG_DIR/vllm_main.log"
MCP_LOG="$LOG_DIR/mcp_server.log"
FRONTEND_LOG="$LOG_DIR/frontend.log"
BACKEND_LOG="$LOG_DIR/backend.log"

# Create/clear log files
: > "$MAIN_LOG"
: > "$VLLM_RAG_LOG"
: > "$VLLM_MAIN_LOG"
: > "$MCP_LOG"
: > "$FRONTEND_LOG"
: > "$BACKEND_LOG"

# Server Configuration
VLLM_MODEL_DIR="$SCRIPT_DIR/model_configs"
VLLM_PORT_MAIN=8000
VLLM_PORT_RAG=8001
FRONTEND_PORT=3088
BACKEND_PORT=8080

# Check for required environment variables
if [ -z "$ARANGO_USERNAME" ] || [ -z "$ARANGO_PASSWORD" ]; then
    echo "Error: ARANGO_USERNAME and ARANGO_PASSWORD must be set in .env file or environment"
    exit 1
fi

# Logging function
log() {
    local level=$1
    shift
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$MAIN_LOG"
}

# Error handling
handle_error() {
    local exit_code=$1
    local line_number=$2
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [ERROR] Error occurred in script at line $line_number with exit code $exit_code" | tee -a "$MAIN_LOG"
    cleanup
    exit 1
}

# Process management
cleanup() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [INFO] Cleaning up processes..." | tee -a "$MAIN_LOG"
    for pid_file in "$PID_DIR"/*.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            process_name=$(basename "$pid_file" .pid)
            if kill -0 "$pid" 2>/dev/null; then
                echo "[$(date +'%Y-%m-%d %H:%M:%S')] [INFO] Stopping $process_name (PID: $pid)" | tee -a "$MAIN_LOG"
                kill "$pid" 2>/dev/null || true
                wait "$pid" 2>/dev/null || true
            fi
            rm -f "$pid_file"
        fi
    done
}

# Set up traps early
trap 'handle_error $? $LINENO' ERR
trap cleanup EXIT INT TERM

# Check if process is running
is_process_running() {
    local pid_file="$PID_DIR/$1.pid"
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            return 0
        fi
    fi
    return 1
}

# Check dependencies
check_dependencies() {
    log "INFO" "Checking dependencies..."
    
    # Check for Node.js and npm
    if ! command -v node >/dev/null || ! command -v npm >/dev/null; then
        log "ERROR" "Node.js and npm are required"
        exit 1
    fi
    
    # Check for Python and pip
    if ! command -v python3 >/dev/null || ! command -v pip3 >/dev/null; then
        log "ERROR" "Python3 and pip3 are required"
        exit 1
    fi
}

# Start backend
start_backend() {
    log "INFO" "Starting backend on port $BACKEND_PORT..."
    
    cd "$SCRIPT_DIR" || exit 1
    
    # Create Python virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        log "INFO" "Creating Python virtual environment..."
        python3 -m venv .venv || {
            log "ERROR" "Failed to create virtual environment"
            exit 1
        }
    fi
    
    # Activate virtual environment and install dependencies
    source .venv/bin/activate || {
        log "ERROR" "Failed to activate virtual environment"
        exit 1
    }
    
    # Install CUDA-enabled vLLM first
    log "INFO" "Installing vLLM with CUDA support..."
    pip install vllm || {
        log "ERROR" "Failed to install vLLM"
        deactivate
        exit 1
    }

    # Install other requirements
    log "INFO" "Installing other dependencies..."
    pip install -r web_frontend/requirements.txt || {
        log "ERROR" "Failed to install requirements"
        deactivate
        exit 1
    }
    
    # Start backend server
    log "INFO" "Starting FastAPI backend server..."
    cd web_frontend || exit 1
    python -m uvicorn backend.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload > "$BACKEND_LOG" 2>&1 &
    local backend_pid=$!
    echo "$backend_pid" > "$PID_DIR/backend.pid"
    
    # Wait a moment and check if process is still running
    sleep 2
    if ! kill -0 "$backend_pid" 2>/dev/null; then
        log "ERROR" "Backend server failed to start. Check $BACKEND_LOG for details"
        deactivate
        cd ..
        exit 1
    fi
    
    log "INFO" "Backend server started successfully on port $BACKEND_PORT"
    deactivate
    cd ..
}

# Start frontend
start_frontend() {
    log "INFO" "Starting frontend on port $FRONTEND_PORT..."
    
    cd "$SCRIPT_DIR/web_frontend/frontend" || exit 1
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        log "INFO" "Installing frontend dependencies..."
        npm install || {
            log "ERROR" "Failed to install frontend dependencies"
            cd ../../..
            exit 1
        }
    fi
    
    # Start frontend server
    log "INFO" "Starting React frontend server..."
    PORT=$FRONTEND_PORT npm start > "$FRONTEND_LOG" 2>&1 &
    local frontend_pid=$!
    echo "$frontend_pid" > "$PID_DIR/frontend.pid"
    
    # Wait a moment and check if process is still running
    sleep 2
    if ! kill -0 "$frontend_pid" 2>/dev/null; then
        log "ERROR" "Frontend server failed to start. Check $FRONTEND_LOG for details"
        cd ../../..
        exit 1
    fi
    
    log "INFO" "Frontend server started successfully on port $FRONTEND_PORT"
    cd ../../..
}

# Start servers
start_servers() {
    check_dependencies
    start_backend
    start_frontend
}

# Monitor processes
monitor_processes() {
    while true; do
        sleep 5
        if ! is_process_running "backend" && ! is_process_running "frontend"; then
            log "ERROR" "Both backend and frontend servers have stopped"
            cleanup
            exit 1
        fi
    done
}

# Main execution
main() {
    log "INFO" "Starting HADES system..."
    start_servers
    monitor_processes
}

# Run main function
main

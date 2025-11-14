#!/bin/bash

# Configuration
API_SCRIPT="system_monitor.main"
REGISTER_SCRIPT="system_monitor.register"
PYTHON_API_CMD="python -m $API_SCRIPT"
PYTHON_REGISTER_CMD="python -m $REGISTER_SCRIPT"

source .venv/bin/activate

# Kill processes by script name
kill_process() {
    local SCRIPT_NAME=$1
    echo "Looking for running process: $SCRIPT_NAME..."
    PIDS=$(pgrep -f "$SCRIPT_NAME")

    if [ -z "$PIDS" ]; then
        echo "No running process found for $SCRIPT_NAME"
        return 1
    fi

    echo "Found process(es): $PIDS"
    for PID in $PIDS; do
        echo "Killing process $PID..."
        kill -TERM $PID && sleep 2
        kill -0 $PID 2>/dev/null && kill -KILL $PID
    done
    echo "All processes of $SCRIPT_NAME killed."
}

# Start a process
start_process() {
    local CMD=$1
    local LOG_FILE=$2
    echo "Starting process: $CMD..."
    nohup $CMD > $LOG_FILE 2>&1 &
    echo "Started new process with PID: $!"
    echo "Logs: $LOG_FILE"
}

# Main execution
echo "=== Restart Script ==="
kill_process "$API_SCRIPT"
kill_process "$REGISTER_SCRIPT"
sleep 1
start_process "$PYTHON_API_CMD" "api.log"
start_process "$PYTHON_REGISTER_CMD" "agent.log"
echo "=== Restart completed ==="
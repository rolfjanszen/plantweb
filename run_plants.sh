#!/usr/bin/env bash

# Name of the tmux session
SESSION_NAME="plant_ses"

# Check if the tmux session already exists
tmux has-session -t "$SESSION_NAME" 2>/dev/null

if [ $? -eq 0 ]; then
  echo "Session '$SESSION_NAME' already exists. Attaching..."
  tmux attach-session -t "$SESSION_NAME"
  exit 0
fi

echo "Creating new tmux session: '$SESSION_NAME'"

# 1. Create a new detached session with a specific window name
tmux new-session -d -s "$SESSION_NAME" -n "backend"

# 2. Window 1 ("backend"): Source venv/env and run a process
tmux send-keys -t "$SESSION_NAME:backend" "cd /home/pi/scripts/plantweb" C-m
tmux send-keys -t "$SESSION_NAME:backend" "source ~/scripts/plantweb/.venv/bin/activate" C-m
tmux send-keys -t "$SESSION_NAME:backend" "python3 app.py" C-m

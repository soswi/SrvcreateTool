from pathlib import Path

class ServerScriptTemplate:
    def __init__(self, name: str, base_path: Path, user_folder: str):
        self.name = name
        self.base_path = base_path
        self.user_folder = user_folder
        self.full_path = base_path / name

    def start_server(self):
        return f"""#!/bin/bash

cd "{self.full_path}"

SESSION_NAME="{self.name}"
SOCKET_PATH="/var/run/shared_tmux/{self.user_folder}/{self.name}.sock"
START_CMD="./run.sh"

if tmux -S "$SOCKET_PATH" list-sessions 2>/dev/null | grep -q "^$SESSION_NAME:"; then
    echo "Tmux session $SESSION_NAME already exists. Skipping start."
else
    echo "Starting code session..."
    tmux -S "$SOCKET_PATH" new-session -d -s "$SESSION_NAME" "$START_CMD"
    chmod g+rw "$SOCKET_PATH"
    echo "Code session started in tmux: $SESSION_NAME"
fi
"""

    def monitor(self):
        return "# No monitor script needed for code instance.\n"

    def run(self):
        return """#!/bin/bash
# Replace this with your actual startup command
python3 main.py
"""

    def stop_server(self):
        return f"""#!/bin/bash

SESSION_NAME="{self.name}"

if tmux list-sessions | grep -q "^$SESSION_NAME:"; then
    echo "Stopping code session..."
    tmux kill-session -t "$SESSION_NAME"
else
    echo "Tmux session $SESSION_NAME not found."
fi
"""

    def create_backup(self):
        return "# No backup required for code instance.\n"

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
MONITOR_SCRIPT_PATH="{self.full_path}/monitor.sh"
SOCKET_PATH="/var/run/shared_tmux/{self.user_folder}/{self.name}.sock"

if tmux -S "$SOCKET_PATH" list-sessions 2>/dev/null | grep -q "^$SESSION_NAME:"; then
    echo "Tmux session $SESSION_NAME already exists, skipping the start."
else
    echo "Starting Minecraft server..."
    tmux -S "$SOCKET_PATH" new-session -d -s "$SESSION_NAME" "$MONITOR_SCRIPT_PATH"
    chmod g+rw "$SOCKET_PATH"
    echo "Minecraft monitor script started in tmux session: $SESSION_NAME"
fi
"""

    def monitor(self):
        return f"""#!/bin/bash

RUN_SH_PATH="{self.full_path}/run.sh"

start_minecraft() {{
    echo "Starting Minecraft server..."
    bash $RUN_SH_PATH
    echo "Minecraft server stopped"
}}

while true; do
    start_minecraft
    echo "Server has stopped. Waiting for 60 seconds before restarting. Send 'confirm-stop' to abort."
    read -t 60 -p "Type 'confirm-stop' to prevent restart: " input
    if [[ $input == "confirm-stop" ]]; then
        echo "Server restart aborted by user."
        exit 0
    else
        echo "Restarting server..."
    fi
    sleep 5
done
"""

    def run(self):
        return """#!/usr/bin/env sh
java -Xmx10G -Xms10G -jar fabric-server-launch-1.20.1.jar nogui
"""

    def stop_server(self):
        return f"""#!/bin/bash

SESSION_NAME="{self.name}"

if tmux list-sessions | grep -q "^$SESSION_NAME:"; then
    echo "Sending stop command to the Minecraft server..."
    tmux send-keys -t $SESSION_NAME "stop" C-m
    echo "Waiting for server to shut down..."
    sleep 20
    tmux kill-session -t $SESSION_NAME
else
    echo "Tmux session $SESSION_NAME does not exist."
fi
"""

    def create_backup(self):
        return f"""#!/bin/bash

ROOT_FOLDER="{self.full_path}"
DATE=$(date +%d%m%Y)
ID="{self.name}"

echo "Creating a server backup"
tmux new-session -d -s "$ID-backup" "tar -czvf '$ROOT_FOLDER/backup-$DATE.tar.gz' \
    '$ROOT_FOLDER/world/' \
    '$ROOT_FOLDER/config/' \
    '$ROOT_FOLDER/logs/' \
    '$ROOT_FOLDER/whitelist.json' \
    '$ROOT_FOLDER/server.properties' \
    '$ROOT_FOLDER/banned-players.json' \
    '$ROOT_FOLDER/banned-ips.json'"

find "$ROOT_FOLDER" -name "backup-*.tar.gz" -type f -mtime +2 -exec rm {{}} \\;
echo "Old backups removed"
"""

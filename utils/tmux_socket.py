import os
from pathlib import Path
import grp

TMUX_CONF_PATH = Path("/etc/tmpfiles.d/shared_tmux.conf")

class TMUXSocketError(Exception):
    """Raised when tmux socket setup fails due to permissions or other errors."""
    pass

def ensure_tmux_socket_dir(user: str):
    try:
        grp.getgrnam(user)
    except KeyError:
        raise TMUXSocketError(f"Group '{user}' does not exist.")

    socket_path = Path(f"/run/shared_tmux/{user}")
    config_line = f"d /run/shared_tmux/{user} 0770 root {user} -"

    # Try to create socket directory if it doesn't exist
    if not socket_path.exists():
        print(f"[INFO] Tmux socket directory does not exist: {socket_path}")
        print("[INFO] Attempting to create it...")

        try:
            os.makedirs(socket_path, exist_ok=True)
            os.chmod(socket_path, 0o770)
        except PermissionError:
            raise TMUXSocketError("Cannot create tmux socket directory. Root privileges (sudo) are required.")

    # Try to update config if needed
    try:
        with open(TMUX_CONF_PATH, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"[WARN] Config file {TMUX_CONF_PATH} not found. It will be created.")
        lines = []

    if config_line not in lines:
        try:
            with open(TMUX_CONF_PATH, 'a') as f:
                f.write(f"{config_line}\n")
            print(f"[INFO] Added entry to {TMUX_CONF_PATH}")
        except PermissionError:
            raise TMUXSocketError("Cannot modify tmux config file. Root privileges (sudo) are required.")
    else:
        print(f"[OK] Entry already exists in {TMUX_CONF_PATH}")


Oto propozycja opisu (`README.md`) dla Twojego repozytorium **SrvcreateTool**:

---

## 🧰 SrvcreateTool

**SrvcreateTool** is a modular Linux tool for managing and launching service instances, such as game servers and code runners. It provides a unified interface to create, start, stop, monitor, and back up server instances, with automatic integration into user-defined startup and shutdown scripts.

### 🔑 Features

* Interactive, colored terminal menu with dynamic module loading
* Support for multiple users and customizable directory structures
* Instance creation based on selectable script templates
* Auto-registration in `automatic_server_startup.sh` and `shutdown_servers.sh`
* Modular structure ready for extensions (e.g., auto-reboot management)
* Clean separation between logic (`modules`), reusable functions (`utils`), and templates

### 📂 Folder Structure

```
SrvcreateTool/
├── main.py               # Main launcher with menu
├── modules/              # Functional modules (e.g. instance creation)
├── templates/            # Script templates (e.g. game servers)
├── utils/                # Common utilities (e.g. path navigation)
└── venv/ (excluded)      # Virtual environment
```

### 🚀 How to use

```bash
srvtool        # or: python3 /opt/SrvcreateTool/main.py
```

Choose an action from the menu and follow the prompts to create or manage instances.

### 📦 Installation (local)

1. Clone the repository into `/opt/`:

   ```bash
   sudo git clone https://github.com/yourname/SrvcreateTool.git /opt/SrvcreateTool
   ```
2. Create and activate virtual environment (optional):

   ```bash
   python3 -m venv /opt/SrvcreateTool/venv
   ```
3. Create launcher:

   ```bash
   echo '#!/bin/bash\nexec /opt/SrvcreateTool/venv/bin/python /opt/SrvcreateTool/main.py "$@"' | sudo tee /usr/local/bin/srvtool
   sudo chmod +x /usr/local/bin/srvtool
   ```

---

Jeśli chcesz, mogę od razu wrzucić tę treść do pliku `README.md`.

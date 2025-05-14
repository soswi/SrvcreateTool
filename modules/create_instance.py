import importlib
import sys
import os
from pathlib import Path

from utils.utilities import select_user, navigate_path

TEMPLATES_PATH = Path(__file__).resolve().parent.parent / "templates"

def select_template():
    template_files = [f.stem for f in TEMPLATES_PATH.glob("*.py") if f.name != "__init__.py"]
    if not template_files:
        print("[ERROR] No templates found in the 'templates' directory.")
        sys.exit(1)

    print("Available templates:")
    for i, name in enumerate(template_files, 1):
        print(f"{i}. {name}")

    while True:
        try:
            index = int(input("Choose template (number): ")) - 1
            if 0 <= index < len(template_files):
                return template_files[index]
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

def append_line(file_path: Path, line: str):
    with open(file_path, 'a') as f:
        f.write(f"\n{line}")

def run():
    user = select_user()
    user_home = Path("/home") / user
    print("Navigate to the folder where the new instance should be created:")
    target_base = navigate_path(user_home)

    template_name = select_template()
    module = importlib.import_module(f"templates.{template_name}")
    template_class = getattr(module, "ServerScriptTemplate")

    name_input = input("Enter instance name: ").strip()
    instance_name = name_input.replace(" ", "_")
    instance_path = target_base / instance_name

    print("\n\033[94mSummary:\033[0m")
    print(f"User: {user}")
    print(f"Target path: {target_base}")
    print(f"Instance name: {instance_name}")
    print(f"Full instance path: {instance_path}")
    print(f"Template: {template_name}")

    confirm = input("Are you sure you want to create this instance? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled. Restarting selection...\n")
        return run()

    autostart_script = user_home / "scripts" / "automatic_server_startup.sh"
    autoshutdown_script = user_home / "scripts" / "shutdown_servers.sh"

    if instance_path.exists():
        print("[ERROR] This instance already exists.")
        sys.exit(1)

    os.makedirs(instance_path, exist_ok=True)

    template = template_class(instance_name, target_base, user)
    scripts = {
        "start_server.sh": template.start_server(),
        "monitor.sh": template.monitor(),
        "run.sh": template.run(),
        "stop_server.sh": template.stop_server(),
        "create_backup.sh": template.create_backup()
    }

    for filename, content in scripts.items():
        file_path = instance_path / filename
        with open(file_path, 'w') as f:
            f.write(content)
        os.chmod(file_path, 0o755)

    append_line(autostart_script, f"cd {instance_path} && ./start_server.sh")
    append_line(autoshutdown_script, f"cd {instance_path} && ./stop_server.sh && ./create_backup.sh")

    print(f"\n\033[92m[OK]\033[0m Instance '{instance_name}' has been created.")

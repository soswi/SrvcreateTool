from pathlib import Path
import subprocess

REMINDER_FILE = Path("/opt/SrvcreateTool/reminders.txt")

def select_user():
    home_path = Path("/home")
    users = [d.name for d in home_path.iterdir() if d.is_dir()]
    print("Available users:")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user}")

    while True:
        try:
            index = int(input("Select user (number): ")) - 1
            if 0 <= index < len(users):
                return users[index]
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

def navigate_path(base: Path) -> tuple[Path, list[Path]]:
    current = base
    to_create = []

    while True:
        try:
            entries = [e for e in current.iterdir() if e.is_dir()]
        except FileNotFoundError:
            entries = []

        print(f"\nContents of: {current}")
        for i, entry in enumerate(entries, 1):
            print(f"{i}. {entry.name}")
        print(f"{len(entries)+1}. [DEFINE NEW FOLDER HERE]")
        print(f"0. [SELECT THIS FOLDER]")

        try:
            choice = int(input("Select number: "))
            if choice == 0:
                return current, to_create
            elif choice == len(entries) + 1:
                new_name = input("Enter new folder name: ").strip().replace(" ", "_")
                current = current / new_name
                to_create.append(current)
                print(f"Planned new folder: {current}")
            elif 1 <= choice <= len(entries):
                current = entries[choice - 1]
            else:
                print("Invalid choice.")
        except ValueError:
            print("Error. Try again.")

def add_reminder(description: str, command: str):
    REMINDER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REMINDER_FILE, 'a') as f:
        f.write(f"# {description}\n{command}\n\n")

def reminder():
    if REMINDER_FILE.exists():
        with open(REMINDER_FILE, 'r') as f:
            lines = f.readlines()

        commands = [line for line in lines if not line.startswith("#") and line.strip()]

        if not commands:
            return  # no actionable commands

        print(f"\n\033[93m[ADMIN TASKS PENDING — {len(commands)} item(s)]\033[0m")
        print("Execute with: sudo srvtool --reminder-update")

def reminder_update():
    if not REMINDER_FILE.exists():
        print("[INFO] No pending admin tasks.")
        return

    with open(REMINDER_FILE, 'r') as f:
        lines = f.readlines()

    commands = [line.strip() for line in lines if line.strip() and not line.startswith("#")]

    if not commands:
        print("[INFO] No executable commands found in reminder file.")
        REMINDER_FILE.unlink(missing_ok=True)
        return

    print(f"[INFO] Executing {len(commands)} task(s)...\n")

    all_success = True

    for cmd in commands:
        print(f"→ {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Command failed:\n{cmd}\n{e}")
            all_success = False

    if all_success:
        REMINDER_FILE.unlink(missing_ok=True)
        print("\n[OK] All tasks completed. Reminder file cleared.")
    else:
        print("\n[WARN] Some tasks failed. The reminder file was NOT removed.")

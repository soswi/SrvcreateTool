from pathlib import Path
import importlib
import sys

from utils.utilities import reminder, reminder_update

MODULES_PATH = Path(__file__).resolve().parent / "modules"

def menu():
    module_files = [f.stem for f in MODULES_PATH.glob("*.py") if f.name != "__init__.py"]
    if not module_files:
        print("No available modules found.")
        return

    print("\033[96m=== MAIN MENU ===\033[0m")
    reminder()
    for i, name in enumerate(module_files, 1):
        print(f"\033[93m{i}.\033[0m {name.replace('_', ' ').capitalize()}")

    while True:
        try:
            index = int(input("\nSelect an option (number): ")) - 1
            if 0 <= index < len(module_files):
                module_name = module_files[index]
                module = importlib.import_module(f"modules.{module_name}")
                if hasattr(module, "run"):
                    module.run()
                else:
                    print(f"Module '{module_name}' does not have a run() function.")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    if "--reminder-update" in sys.argv:
        reminder_update()
        sys.exit(0)

    menu()

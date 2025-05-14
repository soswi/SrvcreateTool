from pathlib import Path

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

def navigate_path(base: Path) -> Path:
    current = base
    while True:
        entries = [e for e in current.iterdir() if e.is_dir()]
        print(f"\nContents of: {current}")
        for i, entry in enumerate(entries, 1):
            print(f"{i}. {entry.name}")
        print(f"{len(entries)+1}. [CREATE NEW FOLDER HERE]")
        print(f"0. [SELECT THIS FOLDER]")

        try:
            choice = int(input("Select number: "))
            if choice == 0:
                return current
            elif choice == len(entries) + 1:
                new_name = input("Enter new folder name: ").strip().replace(" ", "_")
                new_path = current / new_name
                new_path.mkdir(exist_ok=False)
                print(f"Folder created: {new_path.name}")
                current = new_path
            elif 1 <= choice <= len(entries):
                current = entries[choice - 1]
            else:
                print("Invalid choice.")
        except (ValueError, FileExistsError):
            print("Error. Try again.")

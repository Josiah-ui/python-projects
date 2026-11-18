def new_note():
    print("=== New Note ===")
    print("Write your note (end with a single line 'END'):")
    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def view_note(note):
    print("=== Your Note ===")
    if not note or not note.strip():
        print("No note to display.")
    else:
        print(note)


def save_note(note):
    if not note or not note.strip():
        print("No note to save.")
        return

    filename = input("Enter filename to save (e.g. note.txt): ")
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(note)
        print(f"Note saved successfully in '{filename}'.")
    except Exception as e:
        print("Error saving note:", e)


def load_note():
    filename = input("Enter filename to load: ")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            note = file.read()
        print(f"Note loaded successfully from '{filename}'.")
        return note
    except FileNotFoundError:
        print(f"File '{filename}' was not found.")
    except OSError as e:
        print("Error loading note:", e)
    return None


def main():
    note = ""
    while True:
        print("\n=== NOTE PAD ===")
        print("1. New Note\n2. View Note\n3. Save Note\n4. Load Note\n5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            note = new_note()
        elif choice == "2":
            view_note(note)
        elif choice == "3":
            save_note(note)
        elif choice == "4":
            loaded_note = load_note()
            if loaded_note is not None:
                note = loaded_note
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()



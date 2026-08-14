import getpass
import sys
import pyperclip
from colorama import init, Fore, Style

from vault import Vault, MAX_LOGIN_ATTEMPTS
from session_manager import SessionManager
import password_generator

init(autoreset=True)


def print_success(msg): print(Fore.GREEN + msg)
def print_error(msg): print(Fore.RED + msg)
def print_warning(msg): print(Fore.YELLOW + msg)
def print_info(msg): print(Fore.CYAN + msg)
def print_heading(msg): print(Style.BRIGHT + Fore.MAGENTA + msg)


MENU = """
========================================
        SECURE PASSWORD MANAGER
========================================
1. Add New Password
2. Search Password by Website
3. List All Saved Websites
4. Update an Entry
5. Delete an Entry
6. Generate a Strong Password
7. Security Audit (weak/reused passwords)
8. Change Master Password
0. Lock & Exit
"""

vault = Vault()


def on_session_timeout():
    print_warning("\n\nSession timed out after 5 minutes of inactivity. Vault locked.")
    vault.lock()


session = SessionManager(on_timeout=on_session_timeout)


def require_unlock_flow():
    """Handles first-time setup or master password login, including lockout
    after too many failed attempts."""
    if not vault.vault_exists():
        print_heading("Welcome! No vault found - let's set up a new one.")
        while True:
            password_1 = getpass.getpass("Create a master password: ")
            password_2 = getpass.getpass("Confirm master password: ")
            if password_1 != password_2:
                print_error("Passwords don't match. Please try again.")
                continue
            if len(password_1) < 8:
                print_error("Master password should be at least 8 characters.")
                continue
            break

        vault.setup_master_password(password_1)
        print_success("Vault created and unlocked!")
        return True

    while vault.failed_attempts < MAX_LOGIN_ATTEMPTS:
        entered_password = getpass.getpass("Enter your master password: ")
        if vault.unlock(entered_password):
            print_success("Vault unlocked!")
            return True
        remaining = MAX_LOGIN_ATTEMPTS - vault.failed_attempts
        print_error(f"Incorrect master password. {remaining} attempt(s) remaining.")

    print_error("Too many failed attempts. Exiting for security.")
    return False


def handle_add_entry():
    website = input("Website: ").strip()
    username = input("Username/Email: ").strip()

    choice = input("Generate a strong password automatically? (y/n): ").strip().lower()
    if choice == "y":
        plain_password = password_generator.generate_password()
        print_info(f"Generated password: {plain_password}")
    else:
        plain_password = getpass.getpass("Password: ")

    notes = input("Notes (optional): ").strip()

    strength = password_generator.check_strength(plain_password)
    print_info(f"Password strength: {strength}")

    vault.add_entry(website, username, plain_password, notes)
    print_success(f"Saved password for '{website}'.")


def handle_search():
    query = input("Enter website to search for: ").strip()
    results = vault.search(query)

    if not results:
        print_warning("No matching entries found.")
        return

    print_heading(f"\nFound {len(results)} matching entry(ies):")
    for index, entry in enumerate(results, start=1):
        print(f"{index}. {entry.website} | {entry.username}")

    choice = input("\nEnter number to view/copy password (or press Enter to cancel): ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(results)):
        return

    selected_entry = results[int(choice) - 1]
    plain_password = vault.decrypt_password(selected_entry)

    if plain_password is None:
        print_error("Could not decrypt this entry.")
        return

    print_success(f"Password: {plain_password}")
    try:
        pyperclip.copy(plain_password)
        print_info("Password copied to clipboard!")
    except Exception:
        print_warning("Could not copy to clipboard (pyperclip may need a display environment).")


def handle_list_all():
    if not vault.entries:
        print_warning("No entries saved yet.")
        return
    print_heading(f"\n----- {len(vault.entries)} Saved Website(s) -----")
    for entry in vault.entries:
        print(f"{entry.website} | {entry.username} | added {entry.date_added}")


def handle_update_entry():
    query = input("Enter website to update: ").strip()
    results = vault.search(query)
    if not results:
        print_warning("No matching entries found.")
        return

    entry = results[0] if len(results) == 1 else _pick_from_multiple(results)
    if entry is None:
        return

    new_username = input(f"New username [{entry.username}] (Enter to keep): ").strip()
    change_password = input("Update password too? (y/n): ").strip().lower()
    new_password = getpass.getpass("New password: ") if change_password == "y" else None
    new_notes = input(f"New notes [{entry.notes}] (Enter to keep): ").strip()

    vault.update_entry(
        entry,
        new_username=new_username if new_username else None,
        new_password=new_password,
        new_notes=new_notes if new_notes else None,
    )
    print_success("Entry updated.")


def handle_delete_entry():
    query = input("Enter website to delete: ").strip()
    results = vault.search(query)
    if not results:
        print_warning("No matching entries found.")
        return

    entry = results[0] if len(results) == 1 else _pick_from_multiple(results)
    if entry is None:
        return

    confirm = input(f"Delete entry for '{entry.website}'? (y/n): ").strip().lower()
    if confirm == "y":
        vault.delete_entry(entry)
        print_success("Entry deleted.")
    else:
        print_warning("Delete cancelled.")


def _pick_from_multiple(results):
    print_heading(f"Found {len(results)} matches:")
    for index, entry in enumerate(results, start=1):
        print(f"{index}. {entry.website} | {entry.username}")
    choice = input("Enter number: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(results):
        return results[int(choice) - 1]
    return None


def handle_generate_password():
    length_input = input("Password length (default 16): ").strip()
    length = int(length_input) if length_input.isdigit() else 16

    generated = password_generator.generate_password(length=length)
    strength = password_generator.check_strength(generated)

    print_success(f"Generated password: {generated}")
    print_info(f"Strength: {strength}")

    try:
        pyperclip.copy(generated)
        print_info("Copied to clipboard!")
    except Exception:
        pass


def handle_audit():
    weak_entries, reused_passwords = vault.audit()

    print_heading("\n----- Security Audit -----")
    if not weak_entries and not reused_passwords:
        print_success("No weak or reused passwords found. Nice work!")
        return

    if weak_entries:
        print_warning(f"\n{len(weak_entries)} weak/medium-strength password(s):")
        for entry, strength in weak_entries:
            print(f"  {entry.website} - {strength}")

    if reused_passwords:
        print_warning(f"\n{len(reused_passwords)} password(s) reused across multiple sites:")
        for password, websites in reused_passwords.items():
            print(f"  Used on: {', '.join(websites)}")


def handle_change_master_password():
    import base64
    import security

    current = getpass.getpass("Enter current master password to confirm: ")

    raw_data = vault._read_raw()
    salt = base64.urlsafe_b64decode(raw_data["salt"])
    stored_verifier = raw_data["verifier"]

    if security.verify_master_password(current, salt, stored_verifier) is None:
        print_error("Incorrect current master password.")
        return

    new_password_1 = getpass.getpass("New master password: ")
    new_password_2 = getpass.getpass("Confirm new master password: ")
    if new_password_1 != new_password_2:
        print_error("Passwords don't match.")
        return
    if len(new_password_1) < 8:
        print_error("Master password should be at least 8 characters.")
        return

    vault.change_master_password(new_password_1)
    print_success("Master password changed. All entries re-encrypted.")


ACTIONS = {
    "1": handle_add_entry,
    "2": handle_search,
    "3": handle_list_all,
    "4": handle_update_entry,
    "5": handle_delete_entry,
    "6": handle_generate_password,
    "7": handle_audit,
    "8": handle_change_master_password,
}


def main():
    if not require_unlock_flow():
        sys.exit(1)

    session.start()
    is_running = True

    while is_running:
        if session.is_locked():
            print_info("Please unlock the vault to continue.")
            if not require_unlock_flow():
                sys.exit(1)
            session.start()

        print(MENU)
        choice = input("Enter your choice: ").strip()
        session.record_activity()

        if choice == "0":
            vault.lock()
            session.stop()
            print_success("Vault locked. Goodbye!")
            is_running = False
        elif choice in ACTIONS:
            ACTIONS[choice]()
        else:
            print_error("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

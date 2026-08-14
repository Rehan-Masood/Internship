import json
import os
import base64
from cryptography.fernet import Fernet, InvalidToken
from password_entry import PasswordEntry
import security

VAULT_FILE = "vault_data.json"
MAX_LOGIN_ATTEMPTS = 5


class Vault:
    """Main controller: manages the master password, encryption, and all
    saved password entries. Nothing sensitive is ever stored in plaintext -
    only a salt and a one-way verifier hash live on disk until you unlock it."""

    def __init__(self, filepath=VAULT_FILE):
        self.filepath = filepath
        self.entries = []
        self._fernet = None  # only set after a successful unlock
        self.failed_attempts = 0

    # ----- First-time setup -----
    def vault_exists(self):
        return os.path.exists(self.filepath)

    def setup_master_password(self, master_password):
        """Creates a brand new, empty vault protected by this master password."""
        salt = security.generate_salt()
        derived_key = security.derive_key(master_password, salt)
        verifier = security.compute_verifier(derived_key)

        self._fernet = Fernet(derived_key)
        self.entries = []

        vault_data = {
            "salt": base64.urlsafe_b64encode(salt).decode("utf-8"),
            "verifier": verifier,
            "entries": [],
        }
        self._write_to_disk(vault_data)

    # ----- Unlocking an existing vault -----
    def unlock(self, master_password):
        """Attempts to unlock the vault. Returns True on success, False on
        failure (and tracks failed attempts for lockout protection)."""
        if self.failed_attempts >= MAX_LOGIN_ATTEMPTS:
            return False  # locked out - too many wrong attempts

        with open(self.filepath, "r") as file:
            vault_data = json.load(file)

        salt = base64.urlsafe_b64decode(vault_data["salt"])
        stored_verifier = vault_data["verifier"]

        derived_key = security.verify_master_password(master_password, salt, stored_verifier)

        if derived_key is None:
            self.failed_attempts += 1
            return False

        self.failed_attempts = 0
        self._fernet = Fernet(derived_key)
        self.entries = [PasswordEntry.from_dict(e) for e in vault_data["entries"]]
        return True

    def lock(self):
        """Wipes the encryption key and decrypted entries from memory (used
        for auto-logout after inactivity)."""
        self._fernet = None
        self.entries = []

    def is_unlocked(self):
        return self._fernet is not None

    # ----- Entry management -----
    def add_entry(self, website, username, plain_password, notes=""):
        encrypted_password = self._fernet.encrypt(plain_password.encode("utf-8")).decode("utf-8")
        entry = PasswordEntry(website, username, encrypted_password, notes)
        self.entries.append(entry)
        self._save()
        return entry

    def search(self, query):
        """Case-insensitive search by website name (partial match)."""
        query_lower = query.lower()
        return [e for e in self.entries if query_lower in e.website.lower()]

    def decrypt_password(self, entry):
        try:
            return self._fernet.decrypt(entry.encrypted_password.encode("utf-8")).decode("utf-8")
        except InvalidToken:
            return None  # shouldn't normally happen unless the vault file was tampered with

    def delete_entry(self, entry):
        if entry in self.entries:
            self.entries.remove(entry)
            self._save()
            return True
        return False

    def update_entry(self, entry, new_username=None, new_password=None, new_notes=None):
        if new_username is not None:
            entry.username = new_username
        if new_password is not None:
            entry.encrypted_password = self._fernet.encrypt(new_password.encode("utf-8")).decode("utf-8")
        if new_notes is not None:
            entry.notes = new_notes
        self._save()

    # ----- Security audit (bonus feature) -----
    def audit(self):
        """Checks for weak or reused passwords across the whole vault."""
        import password_generator

        weak_entries = []
        password_to_websites = {}

        for entry in self.entries:
            plain = self.decrypt_password(entry)
            if plain is None:
                continue

            strength = password_generator.check_strength(plain)
            if strength in ("Weak", "Medium"):
                weak_entries.append((entry, strength))

            password_to_websites.setdefault(plain, []).append(entry.website)

        reused_passwords = {
            password: websites
            for password, websites in password_to_websites.items()
            if len(websites) > 1
        }

        return weak_entries, reused_passwords

    # ----- Master password change -----
    def change_master_password(self, new_master_password):
        """Re-encrypts every entry under a brand new master password."""
        decrypted_entries = [
            (entry.website, entry.username, self.decrypt_password(entry), entry.notes)
            for entry in self.entries
        ]

        salt = security.generate_salt()
        derived_key = security.derive_key(new_master_password, salt)
        verifier = security.compute_verifier(derived_key)
        self._fernet = Fernet(derived_key)

        self.entries = []
        for website, username, plain_password, notes in decrypted_entries:
            self.add_entry(website, username, plain_password, notes)

        vault_data = self._read_raw()
        vault_data["salt"] = base64.urlsafe_b64encode(salt).decode("utf-8")
        vault_data["verifier"] = verifier
        self._write_to_disk(vault_data)

    # ----- Persistence -----
    def _save(self):
        vault_data = self._read_raw()
        vault_data["entries"] = [e.to_dict() for e in self.entries]
        self._write_to_disk(vault_data)

    def _read_raw(self):
        with open(self.filepath, "r") as file:
            return json.load(file)

    def _write_to_disk(self, vault_data):
        with open(self.filepath, "w") as file:
            json.dump(vault_data, file, indent=4)

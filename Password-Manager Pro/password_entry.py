from datetime import datetime


class PasswordEntry:
    """Represents a single saved website/username/password entry.
    The password itself is stored ENCRYPTED (as a Fernet token string) -
    it's only ever decrypted in memory, briefly, when actually needed."""

    def __init__(self, website, username, encrypted_password, notes="", date_added=None):
        self.website = website
        self.username = username
        self.encrypted_password = encrypted_password  # stays encrypted at rest
        self.notes = notes
        self.date_added = date_added if date_added else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts this entry into a plain dict, ready for JSON storage."""
        return {
            "website": self.website,
            "username": self.username,
            "encrypted_password": self.encrypted_password,
            "notes": self.notes,
            "date_added": self.date_added,
        }

    @staticmethod
    def from_dict(data):
        """Rebuilds a PasswordEntry from a dict loaded out of the JSON file."""
        return PasswordEntry(
            website=data["website"],
            username=data["username"],
            encrypted_password=data["encrypted_password"],
            notes=data.get("notes", ""),
            date_added=data.get("date_added"),
        )

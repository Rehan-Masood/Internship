import base64
import hashlib
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PBKDF2_ITERATIONS = 390_000  # deliberately slow, to resist brute-force guessing


def generate_salt():
    """Generates a random 16-byte salt, unique per vault."""
    return os.urandom(16)


def derive_key(master_password, salt):
    """Turns your master password + salt into a 32-byte key suitable for Fernet
    encryption. This is deliberately slow (390,000 rounds) so that brute-forcing
    the master password is computationally expensive."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    key_bytes = kdf.derive(master_password.encode("utf-8"))
    return base64.urlsafe_b64encode(key_bytes)  # Fernet needs this exact format


def compute_verifier(derived_key):
    """Creates a one-way fingerprint of the derived key, used to check the master
    password is correct WITHOUT ever storing the key or password itself.
    (You can't reverse a SHA-256 hash to recover the key.)"""
    return hashlib.sha256(derived_key).hexdigest()


def verify_master_password(master_password, salt, stored_verifier):
    """Checks a master password attempt against the stored verifier.
    Returns the derived key if correct, or None if incorrect."""
    derived_key = derive_key(master_password, salt)
    candidate_verifier = compute_verifier(derived_key)

    # constant-time comparison - prevents timing attacks that could otherwise
    # leak information about the correct verifier byte by byte
    import hmac
    if hmac.compare_digest(candidate_verifier, stored_verifier):
        return derived_key
    return None

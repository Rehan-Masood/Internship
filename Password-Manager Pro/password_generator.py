import secrets
import string


def generate_password(length=16, use_symbols=True):
    """Generates a cryptographically strong random password.
    Uses the 'secrets' module (not 'random') because 'random' is NOT
    safe for anything security-related - it's predictable."""
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*()-_=+" if use_symbols else ""

    all_characters = letters + digits + symbols

    # guarantee at least one of each character type, for a genuinely strong password
    password_chars = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(digits),
    ]
    if use_symbols:
        password_chars.append(secrets.choice(symbols))

    remaining_length = length - len(password_chars)
    password_chars += [secrets.choice(all_characters) for _ in range(remaining_length)]

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def check_strength(password):
    """Gives a simple strength rating: Weak, Medium, Strong, or Very Strong."""
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    elif score == 5:
        return "Strong"
    else:
        return "Very Strong"

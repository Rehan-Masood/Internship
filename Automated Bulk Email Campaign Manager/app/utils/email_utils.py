from email_validator import validate_email, EmailNotValidError

def normalize_email(value):
    value = (value or "").strip().lower()
    try:
        result = validate_email(value, check_deliverability=False)
        return result.normalized
    except EmailNotValidError:
        return None

def personalize(text, contact):
    return (
        text.replace("{{name}}", contact.name or "")
            .replace("{{email}}", contact.email or "")
    )

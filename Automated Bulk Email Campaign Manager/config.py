import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-in-production"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{INSTANCE_DIR / 'mailflow.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = str(UPLOAD_DIR)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    SMTP_HOST = os.getenv(
        "SMTP_HOST",
        "smtp.gmail.com"
    )

    SMTP_PORT = int(
        os.getenv("SMTP_PORT", "587")
    )

    SMTP_USERNAME = os.getenv(
        "SMTP_USERNAME",
        ""
    )

    SMTP_PASSWORD = os.getenv(
        "SMTP_PASSWORD",
        ""
    )

    SMTP_USE_TLS = (
        os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    )

    SMTP_FROM_NAME = os.getenv(
        "SMTP_FROM_NAME",
        "MailFlow"
    )

    RATE_LIMIT_PER_HOUR = int(
        os.getenv("RATE_LIMIT_PER_HOUR", "50")
    )
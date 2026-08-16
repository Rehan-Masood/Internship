import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    PORT = int(os.getenv("PORT", "5000"))
    DEBUG = os.getenv("FLASK_ENV", "development").lower() == "development"
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    APP_ENV = os.getenv("APP_ENV", "Development")

    DB_PATH = Path(os.getenv("DB_PATH", str(BASE_DIR / "instance" / "dockflow.db")))
    LOG_PATH = Path(os.getenv("LOG_PATH", str(BASE_DIR / "logs" / "app.log")))

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_OWNER = os.getenv("GITHUB_OWNER", "")
    GITHUB_REPO = os.getenv("GITHUB_REPO", "")
    GITHUB_WORKFLOW = os.getenv("GITHUB_WORKFLOW", "ci-cd.yml")
    GITHUB_REF = os.getenv("GITHUB_REF", "main")

    DEPLOYMENT_PROVIDER = os.getenv("DEPLOYMENT_PROVIDER", "")
    DEPLOYMENT_WEBHOOK_URL = os.getenv("DEPLOYMENT_WEBHOOK_URL", "")
    EXTERNAL_HEALTH_URL = os.getenv("EXTERNAL_HEALTH_URL", "")

    HEALTH_POLL_SECONDS = int(os.getenv("HEALTH_POLL_SECONDS", "10"))
    METRICS_POLL_SECONDS = int(os.getenv("METRICS_POLL_SECONDS", "10"))
    LOGS_POLL_SECONDS = int(os.getenv("LOGS_POLL_SECONDS", "5"))

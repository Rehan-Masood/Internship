import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def _database_url():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        sqlite_path = os.path.join(BASE_DIR, "app", "site.db").replace("\\", "/")
        return "sqlite:///" + sqlite_path

    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)

    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    return database_url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-me"
    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER_PROFILE = os.path.join(BASE_DIR, "app", "static", "profile_pics")
    UPLOAD_FOLDER_COVER = os.path.join(BASE_DIR, "app", "static", "post_covers")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload size

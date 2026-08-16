import pytest
from app import create_app

@pytest.fixture()
def app(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test",
        "DB_PATH": tmp_path / "test.db",
        "LOG_PATH": tmp_path / "test.log",
        "APP_ENV": "Test",
        "GITHUB_TOKEN": "",
        "GITHUB_OWNER": "",
        "GITHUB_REPO": "",
        "DEPLOYMENT_PROVIDER": "",
        "DEPLOYMENT_WEBHOOK_URL": "",
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

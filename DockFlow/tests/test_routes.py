import pytest

@pytest.mark.parametrize("path", [
    "/dashboard/","/services/","/containers/","/cicd/","/deployments/",
    "/logs/","/monitoring/","/settings/","/documentation/"
])
def test_pages(client, path):
    r = client.get(path)
    assert r.status_code == 200

def test_api_dashboard(client):
    r = client.get("/api/dashboard")
    assert r.status_code == 200
    assert "metrics" in r.get_json()

def test_missing_page(client):
    assert client.get("/does-not-exist").status_code == 404

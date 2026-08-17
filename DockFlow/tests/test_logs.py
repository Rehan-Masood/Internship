def test_logs_api_returns_entries(client):
    response = client.get("/api/logs")
    assert response.status_code == 200
    data = response.get_json()
    assert "logs" in data
    assert isinstance(data["logs"], list)
    assert data["logs"]


def test_logs_page_loads(client):
    response = client.get("/logs/")
    assert response.status_code == 200
    assert b"Logs" in response.data

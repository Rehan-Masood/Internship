def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["service"] == "DockFlow"
    assert data["status"] in {"healthy","degraded"}

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/")
    # Depending on TestClient follow_redirects behavior, we may see a redirect or the final page
    assert response.status_code in (200, 302, 307)
    if response.status_code in (302, 307):
        assert response.headers["location"].endswith("/static/index.html")
    else:
        # httpx Response has a URL attribute
        assert str(response.url).endswith("/static/index.html")


def test_get_activities_shape():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # spot-check the known seed keys/fields
    assert "Chess Club" in data
    chess = data["Chess Club"]
    assert "description" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_ai_status_endpoint_reports_disabled_when_no_key():
    response = client.get("/ai/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["ai_enabled"] is False
    assert "Set ANTHROPIC_API_KEY" in payload["message"]

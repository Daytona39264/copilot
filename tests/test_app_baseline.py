from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    resp = client.get("/")
    # Depending on TestClient follow_redirects behavior, we may see a redirect or the final page
    assert resp.status_code in (200, 302, 307)
    if resp.status_code in (302, 307):
        assert resp.headers["location"].endswith("/static/index.html")
    else:
        # httpx Response has a URL attribute
        assert str(resp.url).endswith("/static/index.html")


def test_get_activities_shape():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # spot-check the known seed keys/fields
    assert "Chess Club" in data
    chess = data["Chess Club"]
    assert "description" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_ai_status_endpoint_reports_disabled_when_no_key():
    resp = client.get("/ai/status")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["ai_enabled"] is False
    assert "Set ANTHROPIC_API_KEY" in payload["message"]


def test_get_activity_availability():
    resp = client.get("/activities/Chess Club/availability")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload == {
        "activity_name": "Chess Club",
        "total_slots": 12,
        "taken_slots": 2,
        "available_slots": 10,
    }


def test_get_activity_availability_missing():
    resp = client.get("/activities/Unknown Club/availability")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Activity not found"}

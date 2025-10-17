from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    resp = client.get("/", allow_redirects=False)
    assert resp.status_code in (302, 307)
    assert resp.headers["location"].endswith("/static/index.html")


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

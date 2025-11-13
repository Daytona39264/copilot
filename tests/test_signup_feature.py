import urllib.parse
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def signup(activity: str, email: str):
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    return client.post(url)


def test_404_when_activity_not_found():
    response = signup("Nonexistent Activity", "student@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_happy_path_adds_participant():
    # Get count before
    before = len(client.get("/activities").json()["Chess Club"]["participants"])
    response = signup("Chess Club", "newstudent@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")
    after = len(client.get("/activities").json()["Chess Club"]["participants"])
    assert after == before + 1


def test_duplicate_signup_returns_409_and_does_not_change_count():
    activity = "Gym Class"
    email = "john@mergington.edu"  # already in seed data
    before = len(client.get("/activities").json()[activity]["participants"])
    response = signup(activity, email)
    assert response.status_code == 409
    assert response.json()["detail"].lower().startswith("already")
    after = len(client.get("/activities").json()[activity]["participants"])
    assert after == before


def test_capacity_limit_returns_409_when_full():
    # Fill Programming Class to max capacity
    activities = client.get("/activities").json()
    activity = "Programming Class"
    max_cap = activities[activity]["max_participants"]

    # Calculate how many more we need to add to reach capacity
    existing = len(activities[activity]["participants"])
    to_add = max_cap - existing

    # Add until full
    for i in range(to_add):
        email = f"captest{i}@mergington.edu"
        response = signup(activity, email)
        assert response.status_code == 200

    # Next one should fail
    response_full = signup(activity, "another@mergington.edu")
    assert response_full.status_code == 409
    assert "full" in response_full.json()["detail"].lower()


def test_invalid_email_returns_400_and_no_change():
    activity = "Programming Class"
    before = len(client.get("/activities").json()[activity]["participants"])

    # invalid format
    response_invalid_format = signup(activity, "not-an-email")
    assert response_invalid_format.status_code == 400

    # wrong domain
    response_wrong_domain = signup(activity, "student@example.com")
    assert response_wrong_domain.status_code == 400

    # empty
    response_empty = signup(activity, " ")
    assert response_empty.status_code == 400

    after = len(client.get("/activities").json()[activity]["participants"])
    assert after == before

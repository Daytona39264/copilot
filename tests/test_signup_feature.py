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
    participants_count_before = len(client.get("/activities").json()["Chess Club"]["participants"])
    response = signup("Chess Club", "newstudent@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")
    participants_count_after = len(client.get("/activities").json()["Chess Club"]["participants"])
    assert participants_count_after == participants_count_before + 1


def test_duplicate_signup_returns_409_and_does_not_change_count():
    activity = "Gym Class"
    email = "john@mergington.edu"  # already in seed data
    participants_count_before = len(client.get("/activities").json()[activity]["participants"])
    response = signup(activity, email)
    assert response.status_code == 409
    assert response.json()["detail"].lower().startswith("already")
    participants_count_after = len(client.get("/activities").json()[activity]["participants"])
    assert participants_count_after == participants_count_before


def test_capacity_limit_returns_409_when_full():
    # Fill Programming Class to max capacity
    activities = client.get("/activities").json()
    activity = "Programming Class"
    max_capacity = activities[activity]["max_participants"]

    # Calculate how many more we need to add to reach capacity
    existing_participants_count = len(activities[activity]["participants"])
    participants_to_add = max_capacity - existing_participants_count

    # Add until full
    for index in range(participants_to_add):
        email = f"captest{index}@mergington.edu"
        response = signup(activity, email)
        assert response.status_code == 200

    # Next one should fail
    response = signup(activity, "another@mergington.edu")
    assert response.status_code == 409
    assert "full" in response.json()["detail"].lower()


def test_invalid_email_returns_400_and_no_change():
    activity = "Programming Class"
    participants_count_before = len(client.get("/activities").json()[activity]["participants"])

    # invalid format
    response1 = signup(activity, "not-an-email")
    assert response1.status_code == 400

    # wrong domain
    response2 = signup(activity, "student@example.com")
    assert response2.status_code == 400

    # empty
    response3 = signup(activity, " ")
    assert response3.status_code == 400

    participants_count_after = len(client.get("/activities").json()[activity]["participants"])
    assert participants_count_after == participants_count_before

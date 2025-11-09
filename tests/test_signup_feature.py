import urllib.parse
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def signup(activity: str, email: str):
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    return client.post(url)


def test_404_when_activity_not_found():
    resp = signup("Nonexistent Activity", "student@mergington.edu")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_happy_path_adds_participant():
    # Get count before
    before = len(client.get("/activities").json()["Chess Club"]["participants"])
    resp = signup("Chess Club", "newstudent@mergington.edu")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")
    after = len(client.get("/activities").json()["Chess Club"]["participants"])
    assert after == before + 1


def test_duplicate_signup_returns_409_and_does_not_change_count():
    activity = "Gym Class"
    email = "john@mergington.edu"  # already in seed data
    before = len(client.get("/activities").json()[activity]["participants"])
    resp = signup(activity, email)
    assert resp.status_code == 409
    assert resp.json()["detail"].lower().startswith("already")
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
        r = signup(activity, email)
        assert r.status_code == 200

    # Next one should fail
    resp = signup(activity, "another@mergington.edu")
    assert resp.status_code == 409
    assert "full" in resp.json()["detail"].lower()


def test_invalid_email_returns_400_and_no_change():
    activity = "Programming Class"
    before = len(client.get("/activities").json()[activity]["participants"])

    # invalid format
    r1 = signup(activity, "not-an-email")
    assert r1.status_code == 400

    # wrong domain
    r2 = signup(activity, "student@example.com")
    assert r2.status_code == 400

    # empty
    r3 = signup(activity, " ")
    assert r3.status_code == 400

    after = len(client.get("/activities").json()[activity]["participants"])
    assert after == before


def test_email_case_is_preserved_in_storage():
    """Test that email case is preserved when stored in participants list.
    
    When a user signs up with 'NewStudent@mergington.edu', that exact string
    (preserving case) should be stored, not 'newstudent@mergington.edu'.
    This matches what the API response message shows.
    """
    activity = "Drama Club"
    email_with_caps = "NewStudent@mergington.edu"
    
    # Sign up with mixed case email
    resp = signup(activity, email_with_caps)
    assert resp.status_code == 200
    
    # Verify response message shows original case
    assert email_with_caps in resp.json()["message"], \
        "Response should show original case"
    
    # Get the stored participants
    activities = client.get("/activities").json()
    participants = activities[activity]["participants"]
    
    # Find the matching email (case-insensitive search)
    matching_emails = [p for p in participants if p.lower() == email_with_caps.lower()]
    assert len(matching_emails) == 1, "Should have exactly one matching email"
    
    # Verify the email case is preserved (not converted to lowercase)
    assert matching_emails[0] == email_with_caps, \
        f"Email case should be preserved. Expected '{email_with_caps}', got '{matching_emails[0]}'"

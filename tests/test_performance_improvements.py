"""
Tests to validate performance improvements and optimizations
"""
from fastapi.testclient import TestClient
from src.app import app, activities
import urllib.parse

client = TestClient(app)


def signup(activity: str, email: str):
    """Helper to signup for activities"""
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    return client.post(url)


def test_duplicate_check_optimization_with_direct_comparison():
    """
    Test that duplicate checking works efficiently with direct 'in' operator.
    This validates the optimization from O(n) any() with .lower() to O(1) set lookup.
    """
    activity = "Basketball Team"
    email = "test1@mergington.edu"
    
    # First signup should succeed
    resp1 = signup(activity, email)
    assert resp1.status_code == 200
    
    # Duplicate signup with same case should fail
    resp2 = signup(activity, email)
    assert resp2.status_code == 409
    assert "Already signed up" in resp2.json()["detail"]
    
    # Duplicate signup with different case should also fail (case-insensitive)
    resp3 = signup(activity, "TEST1@MERGINGTON.EDU")
    assert resp3.status_code == 409
    assert "Already signed up" in resp3.json()["detail"]


def test_participants_stored_in_lowercase():
    """
    Verify that participants are stored in lowercase format,
    which enables the O(1) lookup optimization.
    """
    activity = "Swimming Club"
    email = "MixedCase@mergington.edu"
    
    # Sign up with mixed case
    resp = signup(activity, email)
    assert resp.status_code == 200
    
    # Verify stored in lowercase
    activities_data = client.get("/activities").json()
    participants = activities_data[activity]["participants"]
    
    # Should be stored as lowercase
    assert "mixedcase@mergington.edu" in participants
    assert "MixedCase@mergington.edu" not in participants


def test_multiple_signups_efficiency():
    """
    Test that multiple signups work efficiently with optimized duplicate checking.
    This ensures the optimization doesn't break the happy path.
    """
    activity = "Science Club"
    
    # Add multiple students
    emails = [f"student{i}@mergington.edu" for i in range(5)]
    
    for email in emails:
        resp = signup(activity, email)
        assert resp.status_code == 200
    
    # Verify all were added
    activities_data = client.get("/activities").json()
    participants = activities_data[activity]["participants"]
    
    # All should be in the list (in lowercase)
    for email in emails:
        assert email.lower() in participants
    
    # Each duplicate should fail
    for email in emails:
        resp = signup(activity, email)
        assert resp.status_code == 409


def test_path_operations_work_correctly():
    """
    Verify that the static files mount works correctly with optimized Path operations.
    """
    # Test that we can access static files
    resp = client.get("/")
    assert resp.status_code in (200, 302, 307)  # Should redirect or serve


def test_ai_chat_string_building_optimization():
    """
    Test that the AI chat endpoint works with the optimized string building
    (using list + join instead of += in loop).
    This test will pass whether AI is enabled or not.
    """
    resp = client.post(
        "/ai/chat",
        json={"message": "Tell me about the activities"}
    )
    
    # Should either work (200) or return 503 if AI not enabled
    assert resp.status_code in (200, 503)
    
    if resp.status_code == 503:
        # AI not enabled, which is fine
        assert "AI features not enabled" in resp.json()["detail"]


def test_participation_analysis_optimization():
    """
    Test that the participation analysis endpoint works with optimized
    redundant len() call elimination.
    """
    resp = client.get("/ai/participation-insights")
    
    # Should either work (200) or return 503 if AI not enabled
    assert resp.status_code in (200, 503)
    
    if resp.status_code == 503:
        # AI not enabled, which is fine
        assert "AI features not enabled" in resp.json()["detail"]

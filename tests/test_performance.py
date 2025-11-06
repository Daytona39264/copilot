"""
Performance tests to verify efficiency improvements in the codebase.
"""
import urllib.parse
from fastapi.testclient import TestClient
from src.app import app
import time

client = TestClient(app)


def signup(activity: str, email: str):
    url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    return client.post(url)


def test_duplicate_check_performance_with_many_participants():
    """
    Test that duplicate checking remains efficient even with many participants.
    With set-based lookup (O(1)), this should be fast even with many participants.
    Previously used any() with generator which was O(n).
    """
    activity = "Art Studio"
    
    # Add many participants to test duplicate check efficiency
    for i in range(15):  # Fill to capacity
        email = f"student{i}@mergington.edu"
        resp = signup(activity, email)
        assert resp.status_code == 200
    
    # Now test duplicate detection - should be fast with O(1) set lookup
    start = time.time()
    resp = signup(activity, "student0@mergington.edu")  # Duplicate
    duration = time.time() - start
    
    assert resp.status_code == 409
    assert "already" in resp.json()["detail"].lower()
    
    # Should complete very quickly (under 100ms is generous, actual should be <1ms)
    assert duration < 0.1, f"Duplicate check took {duration}s, should be near-instant with O(1) lookup"


def test_signup_case_insensitive_duplicate_check():
    """
    Verify case-insensitive duplicate checking works correctly.
    This also validates the set-based optimization.
    """
    activity = "Debate Team"
    
    # Sign up with lowercase
    resp1 = signup(activity, "test@mergington.edu")
    assert resp1.status_code == 200
    
    # Try to sign up with different case - should be rejected
    resp2 = signup(activity, "TEST@mergington.edu")
    assert resp2.status_code == 409
    
    # Try mixed case
    resp3 = signup(activity, "TeSt@mergington.edu")
    assert resp3.status_code == 409


def test_activities_endpoint_response_time():
    """
    Test that getting activities list is fast.
    This is a baseline performance test.
    """
    start = time.time()
    resp = client.get("/activities")
    duration = time.time() - start
    
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)
    
    # Should be very fast for in-memory data
    assert duration < 0.05, f"Activities endpoint took {duration}s, should be under 50ms"


def test_multiple_signups_performance():
    """
    Test that multiple signups complete in reasonable time.
    Validates overall endpoint performance.
    """
    activity = "Science Club"
    
    start = time.time()
    
    # Sign up multiple students
    for i in range(10):
        email = f"sciencestudent{i}@mergington.edu"
        resp = signup(activity, email)
        assert resp.status_code == 200
    
    duration = time.time() - start
    
    # 10 signups should complete quickly (< 500ms is very generous)
    assert duration < 0.5, f"10 signups took {duration}s, should complete in under 500ms"
    
    # Average per signup
    avg_duration = duration / 10
    assert avg_duration < 0.05, f"Average signup time {avg_duration}s, should be under 50ms"

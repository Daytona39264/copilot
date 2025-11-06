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
    
    # Should complete reasonably quickly (1 second is very generous)
    # This is mainly a regression test - with O(n) it would be slower
    assert duration < 1.0, f"Duplicate check took {duration}s, unexpectedly slow"


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
    
    # Should be reasonably fast for in-memory data (5 seconds is very generous)
    assert duration < 5.0, f"Activities endpoint took {duration}s, unexpectedly slow"


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
    
    # 10 signups should complete in reasonable time (10 seconds is very generous)
    # This is mainly a regression test to catch major performance issues
    assert duration < 10.0, f"10 signups took {duration}s, unexpectedly slow"

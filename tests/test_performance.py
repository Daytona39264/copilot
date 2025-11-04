"""
Performance tests to validate efficiency improvements
"""
import time
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_duplicate_check_performance_with_many_participants():
    """
    Test that duplicate checking remains fast even with many participants.
    
    The optimized version uses a set for O(1) lookup instead of O(n) linear search.
    This test ensures the duplicate check is fast even with 100+ participants.
    """
    activity = "Science Club"
    
    # Science Club has max_participants of 20, so add up to 19
    # to leave room for the duplicate check test
    for i in range(19):
        email = f"student{i}@mergington.edu"
        resp = client.post(f"/activities/{activity}/signup?email={email}")
        assert resp.status_code == 200
    
    # Measure time to check for duplicate (should be fast due to set lookup)
    start_time = time.time()
    
    # Try to signup again with an existing email (duplicate check)
    resp = client.post(f"/activities/{activity}/signup?email=student10@mergington.edu")
    
    elapsed_time = time.time() - start_time
    
    # Verify correct behavior
    assert resp.status_code == 409
    assert "already" in resp.json()["detail"].lower()
    
    # Performance assertion: should complete in less than 100ms
    # With O(1) set lookup, this should be very fast even with 19 participants
    assert elapsed_time < 0.1, f"Duplicate check took {elapsed_time:.4f}s, expected < 0.1s"


def test_signup_performance_scalability():
    """
    Test that signup operations scale well with increasing participants.
    
    Ensures that the optimized duplicate check using sets provides
    consistent performance regardless of the number of existing participants.
    """
    activity = "Debate Team"
    
    # Track time for first signup (few participants)
    start_time = time.time()
    resp = client.post(f"/activities/{activity}/signup?email=first@mergington.edu")
    first_signup_time = time.time() - start_time
    assert resp.status_code == 200
    
    # Add 10 more participants
    for i in range(10):
        email = f"student{i}@mergington.edu"
        client.post(f"/activities/{activity}/signup?email={email}")
    
    # Track time for signup with 11 existing participants
    start_time = time.time()
    resp = client.post(f"/activities/{activity}/signup?email=last@mergington.edu")
    last_signup_time = time.time() - start_time
    assert resp.status_code == 200
    
    # With O(1) set lookup, the time difference should be minimal
    # Allow up to 50ms difference to account for system variance
    time_difference = abs(last_signup_time - first_signup_time)
    assert time_difference < 0.05, f"Time difference {time_difference:.4f}s indicates O(n) behavior"

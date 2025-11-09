"""
Performance tests to validate efficiency improvements
"""
import time
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_with_many_participants_is_efficient():
    """Test that duplicate checking scales reasonably with participant count"""
    # Add many participants to an activity
    activity = "Basketball Team"
    
    # Add 100 participants
    start = time.time()
    for i in range(100):
        email = f"student{i}@mergington.edu"
        resp = client.post(f"/activities/{activity}/signup?email={email}")
        # Stop if activity is full
        if resp.status_code == 409 and "full" in resp.json()["detail"].lower():
            break
    
    # Try to add a duplicate - should be fast even with many participants
    duplicate_start = time.time()
    resp = client.post(f"/activities/{activity}/signup?email=student0@mergington.edu")
    duplicate_time = time.time() - duplicate_start
    
    # Should complete in under 100ms even with many participants
    assert duplicate_time < 0.1, f"Duplicate check took {duplicate_time}s, should be < 0.1s"
    assert resp.status_code == 409
    assert "already" in resp.json()["detail"].lower()


def test_get_activities_response_is_consistent():
    """Test that get_activities returns consistent data structure"""
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    
    # Verify structure is consistent for all activities
    for name, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)


def test_path_operations_are_efficient():
    """Test that path operations don't cause performance issues"""
    # The static file mount should work correctly
    start = time.time()
    resp = client.get("/")
    elapsed = time.time() - start
    
    # Should redirect quickly
    assert elapsed < 0.1, f"Redirect took {elapsed}s, should be < 0.1s"
    assert resp.status_code in (200, 302, 307)


def test_activity_list_operations_are_efficient():
    """Test that operations on the activities dict are efficient"""
    # Get activities multiple times
    times = []
    for _ in range(10):
        start = time.time()
        resp = client.get("/activities")
        elapsed = time.time() - start
        times.append(elapsed)
        assert resp.status_code == 200
    
    # Average time should be fast
    avg_time = sum(times) / len(times)
    assert avg_time < 0.05, f"Average request time {avg_time}s, should be < 0.05s"

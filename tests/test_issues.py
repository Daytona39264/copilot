from fastapi.testclient import TestClient
from src.app import app, issues

client = TestClient(app)


def test_create_issue_success():
    """Test creating a valid issue"""
    # Clear issues before test
    issues.clear()
    
    issue_data = {
        "title": "Activity signup not working",
        "description": "I tried to sign up for Chess Club but got an error",
        "category": "bug",
        "related_activity": "Chess Club",
        "reporter_email": "student@mergington.edu"
    }
    
    resp = client.post("/issues", json=issue_data)
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == issue_data["title"]
    assert data["description"] == issue_data["description"]
    assert data["category"] == "bug"
    assert data["related_activity"] == "Chess Club"
    assert data["reporter_email"] == "student@mergington.edu"
    assert data["status"] == "open"
    assert "created_at" in data


def test_create_issue_invalid_email():
    """Test that invalid email is rejected"""
    issues.clear()
    
    issue_data = {
        "title": "Test issue",
        "description": "Test description",
        "category": "bug",
        "reporter_email": "invalid@example.com"  # Wrong domain
    }
    
    resp = client.post("/issues", json=issue_data)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid email"


def test_create_issue_invalid_activity():
    """Test that invalid activity reference is rejected"""
    issues.clear()
    
    issue_data = {
        "title": "Test issue",
        "description": "Test description",
        "category": "bug",
        "related_activity": "Nonexistent Club",
        "reporter_email": "student@mergington.edu"
    }
    
    resp = client.post("/issues", json=issue_data)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Related activity not found"


def test_create_issue_invalid_category():
    """Test that invalid category is rejected"""
    issues.clear()
    
    issue_data = {
        "title": "Test issue",
        "description": "Test description",
        "category": "invalid_category",
        "reporter_email": "student@mergington.edu"
    }
    
    resp = client.post("/issues", json=issue_data)
    assert resp.status_code == 400
    assert "Invalid category" in resp.json()["detail"]


def test_get_all_issues():
    """Test retrieving all issues"""
    issues.clear()
    
    # Create multiple issues
    issue1 = {
        "title": "Bug report",
        "description": "Something is broken",
        "category": "bug",
        "reporter_email": "student1@mergington.edu"
    }
    issue2 = {
        "title": "Feature request",
        "description": "Add new feature",
        "category": "feature_request",
        "reporter_email": "student2@mergington.edu"
    }
    
    client.post("/issues", json=issue1)
    client.post("/issues", json=issue2)
    
    resp = client.get("/issues")
    assert resp.status_code == 200
    
    data = resp.json()
    assert len(data) == 2
    assert data[0]["title"] == "Bug report"
    assert data[1]["title"] == "Feature request"


def test_get_issues_filtered_by_category():
    """Test filtering issues by category"""
    issues.clear()
    
    # Create issues with different categories
    client.post("/issues", json={
        "title": "Bug 1",
        "description": "Bug description",
        "category": "bug",
        "reporter_email": "student@mergington.edu"
    })
    client.post("/issues", json={
        "title": "Feature 1",
        "description": "Feature description",
        "category": "feature_request",
        "reporter_email": "student@mergington.edu"
    })
    
    # Filter by bug category
    resp = client.get("/issues?category=bug")
    assert resp.status_code == 200
    
    data = resp.json()
    assert len(data) == 1
    assert data[0]["category"] == "bug"


def test_get_issues_filtered_by_status():
    """Test filtering issues by status"""
    issues.clear()
    
    # Create an issue and update its status
    client.post("/issues", json={
        "title": "Test issue",
        "description": "Test",
        "category": "bug",
        "reporter_email": "student@mergington.edu"
    })
    
    client.patch("/issues/1/status?status=resolved")
    
    # Filter by open status (should be empty)
    resp = client.get("/issues?status=open")
    assert resp.status_code == 200
    assert len(resp.json()) == 0
    
    # Filter by resolved status
    resp = client.get("/issues?status=resolved")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_get_issue_by_id():
    """Test retrieving a specific issue"""
    issues.clear()
    
    client.post("/issues", json={
        "title": "Specific issue",
        "description": "Test description",
        "category": "question",
        "reporter_email": "student@mergington.edu"
    })
    
    resp = client.get("/issues/1")
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == "Specific issue"


def test_get_issue_not_found():
    """Test retrieving non-existent issue"""
    issues.clear()
    
    resp = client.get("/issues/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Issue not found"


def test_update_issue_status():
    """Test updating issue status"""
    issues.clear()
    
    client.post("/issues", json={
        "title": "Test issue",
        "description": "Test",
        "category": "bug",
        "reporter_email": "student@mergington.edu"
    })
    
    # Update to in_progress
    resp = client.patch("/issues/1/status?status=in_progress")
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["status"] == "in_progress"
    
    # Verify it was updated
    resp = client.get("/issues/1")
    assert resp.json()["status"] == "in_progress"


def test_update_issue_status_invalid():
    """Test updating issue with invalid status"""
    issues.clear()
    
    client.post("/issues", json={
        "title": "Test issue",
        "description": "Test",
        "category": "bug",
        "reporter_email": "student@mergington.edu"
    })
    
    resp = client.patch("/issues/1/status?status=invalid_status")
    assert resp.status_code == 400
    assert "Invalid status" in resp.json()["detail"]


def test_update_issue_status_not_found():
    """Test updating non-existent issue"""
    issues.clear()
    
    resp = client.patch("/issues/999/status?status=resolved")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Issue not found"


def test_create_issue_without_activity():
    """Test creating issue without related activity"""
    issues.clear()
    
    issue_data = {
        "title": "General feedback",
        "description": "The system is great overall",
        "category": "feedback",
        "reporter_email": "student@mergington.edu"
    }
    
    resp = client.post("/issues", json=issue_data)
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["related_activity"] is None


def test_ai_issues_summary_disabled():
    """Test AI issues summary when AI is disabled"""
    resp = client.get("/ai/issues-summary")
    assert resp.status_code == 503
    assert "AI features not enabled" in resp.json()["detail"]

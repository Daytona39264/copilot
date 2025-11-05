"""
Tests for AI features in the main application

These tests verify the AI endpoints work correctly both with and without
an ANTHROPIC_API_KEY set.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app

client = TestClient(app)


class TestAIEndpoints:
    """Test AI-powered endpoints"""

    def test_ai_status_endpoint(self):
        """Test AI status endpoint"""
        response = client.get("/ai/status")
        assert response.status_code == 200
        data = response.json()
        assert "ai_enabled" in data
        assert "message" in data

    def test_suggest_activities_without_api_key(self):
        """Test activity suggestions endpoint without API key"""
        response = client.post("/ai/suggest-activities", json={
            "student_interests": ["programming", "problem solving"],
            "grade_level": 10
        })

        # Should return 503 if AI not enabled
        if response.status_code == 503:
            assert "AI features not enabled" in response.json()["detail"]
        # Or 200 if API key is set
        elif response.status_code == 200:
            data = response.json()
            assert "suggestions" in data
            assert "student_interests" in data
            assert "grade_level" in data

    def test_chat_endpoint_without_api_key(self):
        """Test chat endpoint without API key"""
        response = client.post("/ai/chat", json={
            "message": "What activities meet on Fridays?"
        })

        if response.status_code == 503:
            assert "AI features not enabled" in response.json()["detail"]
        elif response.status_code == 200:
            data = response.json()
            assert "response" in data
            assert "message" in data

    def test_activity_summary_without_api_key(self):
        """Test activity summary endpoint without API key"""
        response = client.get("/ai/activity-summary/Chess Club")

        if response.status_code == 503:
            assert "AI features not enabled" in response.json()["detail"]
        elif response.status_code == 200:
            data = response.json()
            assert "activity_name" in data
            assert "original_description" in data
            assert "ai_enhanced_summary" in data

    def test_activity_summary_not_found(self):
        """Test activity summary with non-existent activity"""
        response = client.get("/ai/activity-summary/NonExistent Activity")

        # Should be 404 or 503 depending on AI status
        assert response.status_code in [404, 503]

    def test_participation_insights_without_api_key(self):
        """Test participation insights endpoint without API key"""
        response = client.get("/ai/participation-insights")

        if response.status_code == 503:
            assert "AI features not enabled" in response.json()["detail"]
        elif response.status_code == 200:
            data = response.json()
            assert "participation_data" in data
            assert "ai_insights" in data

    def test_suggest_activities_validation(self):
        """Test activity suggestions with invalid data"""
        # Missing required fields
        response = client.post("/ai/suggest-activities", json={})
        assert response.status_code == 422  # Validation error

    def test_chat_endpoint_validation(self):
        """Test chat endpoint with invalid data"""
        # Missing required fields
        response = client.post("/ai/chat", json={})
        assert response.status_code == 422  # Validation error


class TestExistingEndpoints:
    """Verify existing endpoints still work"""

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200

    def test_get_activities(self):
        """Test get activities endpoint"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data

    def test_signup_endpoint(self):
        """Test signup endpoint"""
        response = client.post(
            "/activities/Chess Club/signup?email=test@mergington.edu"
        )
        # May succeed or return 409 if already signed up
        assert response.status_code in [200, 409]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

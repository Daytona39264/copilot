import types
import pytest

import src.app as app_module


@pytest.fixture
def enable_ai(monkeypatch):
    """Enable AI features in src.app with a stubbed anthropic client."""

    def _enable(return_text="stubbed response", error=None):
        class DummyMessage:
            def __init__(self, text):
                self.text = text

        class DummyResponse:
            def __init__(self, text):
                self.content = [DummyMessage(text)]

        class DummyMessages:
            def __init__(self):
                self.calls = []

            def create(self, **kwargs):
                self.calls.append(kwargs)
                if error is not None:
                    raise error
                return DummyResponse(return_text)

        dummy_client = types.SimpleNamespace(messages=DummyMessages())
        monkeypatch.setattr(app_module, "AI_ENABLED", True)
        monkeypatch.setattr(app_module, "anthropic_client", dummy_client, raising=False)
        return dummy_client.messages

    return _enable


def test_ai_status_disabled_message(client):
    response = client.get("/ai/status")
    assert response.status_code == 200
    data = response.json()
    assert data["ai_enabled"] is False
    assert "enable AI features" in data["message"]


def test_ai_suggest_requires_api_key(client, monkeypatch):
    monkeypatch.setattr(app_module, "AI_ENABLED", False)
    response = client.post(
        "/ai/suggest-activities",
        json={"student_interests": ["robotics"], "grade_level": 10},
    )
    assert response.status_code == 503
    assert "not enabled" in response.json()["detail"]


def test_ai_suggest_returns_stubbed_response(client, enable_ai):
    enable_ai(return_text="Activity 1")
    response = client.post(
        "/ai/suggest-activities",
        json={"student_interests": ["robotics", "art"], "grade_level": 9},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["suggestions"] == "Activity 1"
    assert payload["student_interests"] == ["robotics", "art"]


def test_ai_chat_returns_message(client, enable_ai):
    enable_ai(return_text="Hello from AI")
    response = client.post(
        "/ai/chat",
        json={"message": "Tell me more", "context": "student"},
    )
    assert response.status_code == 200
    assert response.json()["response"] == "Hello from AI"


def test_ai_activity_summary_404_when_missing(client, enable_ai):
    enable_ai(return_text="summary")
    response = client.get("/ai/activity-summary/Unknown Club")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_ai_activity_summary_returns_summary(client, enable_ai):
    enable_ai(return_text="Great activity")
    response = client.get("/ai/activity-summary/Chess Club")
    assert response.status_code == 200
    data = response.json()
    assert data["activity_name"] == "Chess Club"
    assert data["ai_enhanced_summary"] == "Great activity"


def test_ai_participation_insights_returns_payload(client, enable_ai):
    enable_ai(return_text="Insightful analysis")
    response = client.get("/ai/participation-insights")
    assert response.status_code == 200
    payload = response.json()
    assert payload["ai_insights"] == "Insightful analysis"
    assert isinstance(payload["participation_data"], list)
    assert any(item["activity"] == "Chess Club" for item in payload["participation_data"])


def test_ai_participation_errors_return_500(client, enable_ai):
    enable_ai(error=RuntimeError("boom"))
    response = client.get("/ai/participation-insights")
    assert response.status_code == 500
    assert "AI Error" in response.json()["detail"]
    assert "boom" in response.json()["detail"]

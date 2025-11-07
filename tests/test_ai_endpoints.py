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
    resp = client.get("/ai/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ai_enabled"] is False
    assert "enable AI features" in data["message"]


def test_ai_suggest_requires_api_key(client, monkeypatch):
    monkeypatch.setattr(app_module, "AI_ENABLED", False)
    resp = client.post(
        "/ai/suggest-activities",
        json={"student_interests": ["robotics"], "grade_level": 10},
    )
    assert resp.status_code == 503
    assert "not enabled" in resp.json()["detail"]


def test_ai_suggest_returns_stubbed_response(client, enable_ai):
    enable_ai(return_text="Activity 1")
    resp = client.post(
        "/ai/suggest-activities",
        json={"student_interests": ["robotics", "art"], "grade_level": 9},
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["suggestions"] == "Activity 1"
    assert payload["student_interests"] == ["robotics", "art"]


def test_ai_chat_returns_message(client, enable_ai):
    enable_ai(return_text="Hello from AI")
    resp = client.post(
        "/ai/chat",
        json={"message": "Tell me more", "context": "student"},
    )
    assert resp.status_code == 200
    assert resp.json()["response"] == "Hello from AI"


def test_ai_activity_summary_404_when_missing(client, enable_ai):
    enable_ai(return_text="summary")
    resp = client.get("/ai/activity-summary/Unknown Club")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_ai_activity_summary_returns_summary(client, enable_ai):
    enable_ai(return_text="Great activity")
    resp = client.get("/ai/activity-summary/Chess Club")
    assert resp.status_code == 200
    data = resp.json()
    assert data["activity_name"] == "Chess Club"
    assert data["ai_enhanced_summary"] == "Great activity"


def test_ai_participation_insights_returns_payload(client, enable_ai):
    enable_ai(return_text="Insightful analysis")
    resp = client.get("/ai/participation-insights")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["ai_insights"] == "Insightful analysis"
    assert isinstance(payload["participation_data"], list)
    assert any(item["activity"] == "Chess Club" for item in payload["participation_data"])


def test_ai_participation_errors_return_500(client, enable_ai):
    enable_ai(error=RuntimeError("boom"))
    resp = client.get("/ai/participation-insights")
    assert resp.status_code == 500
    assert "AI Error" in resp.json()["detail"]
    assert "boom" in resp.json()["detail"]

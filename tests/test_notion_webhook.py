"""
Tests for Notion Webhook Integration (API v2025-09-03)
Tests for multi-source database support with new data_source events
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import hmac
import hashlib
import json

from src.app import app
from src.notion_webhook import (
    NotionWebhookEvent,
    NotionEventType,
    ParentObject,
    WebhookEventData,
    webhook_event_logs,
    is_data_source_event,
    is_legacy_event,
    verify_webhook_signature
)


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_webhook_logs():
    """Clear webhook logs before each test"""
    webhook_event_logs.clear()
    yield
    webhook_event_logs.clear()


# ============================================================================
# Test Data Source Event Types (New in API v2025-09-03)
# ============================================================================

def test_data_source_content_updated_event(client):
    """Test handling of data_source.content_updated event"""
    event_payload = {
        "type": "data_source.content_updated",
        "event_id": "evt_123456",
        "created_at": "2025-09-03T10:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "database",
            "id": "db_789xyz",
            "parent": {
                "type": "workspace",
                "workspace": True,
                "data_source_id": "ds_multi_001"
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["event_type"] == "data_source.content_updated"
    assert data["data_source_id"] == "ds_multi_001"
    assert data["is_data_source_event"] is True
    assert data["is_legacy_event"] is False


def test_data_source_schema_updated_event(client):
    """Test handling of data_source.schema_updated event"""
    event_payload = {
        "type": "data_source.schema_updated",
        "event_id": "evt_234567",
        "created_at": "2025-09-03T11:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "database",
            "id": "db_789xyz",
            "parent": {
                "type": "workspace",
                "workspace": True,
                "data_source_id": "ds_multi_002"
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["event_type"] == "data_source.schema_updated"
    assert data["data_source_id"] == "ds_multi_002"


def test_data_source_created_event(client):
    """Test handling of data_source.created event"""
    event_payload = {
        "type": "data_source.created",
        "event_id": "evt_345678",
        "created_at": "2025-09-03T12:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "database",
            "id": "db_new_001",
            "parent": {
                "type": "workspace",
                "workspace": True,
                "data_source_id": "ds_multi_003"
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["event_type"] == "data_source.created"
    assert data["data_source_id"] == "ds_multi_003"


def test_data_source_moved_event(client):
    """Test handling of data_source.moved event"""
    event_payload = {
        "type": "data_source.moved",
        "event_id": "evt_456789",
        "created_at": "2025-09-03T13:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "database",
            "id": "db_moved_001",
            "parent": {
                "type": "page",
                "page_id": "page_123",
                "data_source_id": "ds_multi_004"
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["event_type"] == "data_source.moved"
    assert data["data_source_id"] == "ds_multi_004"


def test_data_source_deleted_event(client):
    """Test handling of data_source.deleted event"""
    event_payload = {
        "type": "data_source.deleted",
        "event_id": "evt_567890",
        "created_at": "2025-09-03T14:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "database",
            "id": "db_deleted_001",
            "parent": {
                "type": "workspace",
                "workspace": True,
                "data_source_id": "ds_multi_005"
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["event_type"] == "data_source.deleted"
    assert data["data_source_id"] == "ds_multi_005"


def test_data_source_undeleted_event(client):
    """Test handling of data_source.undeleted event"""
    event_payload = {
        "type": "data_source.undeleted",
        "event_id": "evt_678901",
        "created_at": "2025-09-03T15:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "database",
            "id": "db_undeleted_001",
            "parent": {
                "type": "workspace",
                "workspace": True,
                "data_source_id": "ds_multi_006"
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["event_type"] == "data_source.undeleted"
    assert data["data_source_id"] == "ds_multi_006"


# ============================================================================
# Test Legacy Event Compatibility
# ============================================================================

def test_legacy_database_updated_event(client):
    """Test backward compatibility with legacy database.updated event"""
    event_payload = {
        "type": "database.updated",
        "event_id": "evt_legacy_001",
        "created_at": "2024-01-01T10:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "database",
            "id": "db_legacy_001",
            "parent": {
                "type": "workspace",
                "workspace": True
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["event_type"] == "database.updated"
    assert data["is_legacy_event"] is True
    assert data["is_data_source_event"] is False
    assert data["data_source_id"] is None


def test_legacy_page_created_event(client):
    """Test backward compatibility with legacy page.created event"""
    event_payload = {
        "type": "page.created",
        "event_id": "evt_legacy_002",
        "created_at": "2024-01-01T11:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "page",
            "id": "page_legacy_001",
            "parent": {
                "type": "database",
                "database_id": "db_123"
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["event_type"] == "page.created"
    assert data["is_legacy_event"] is True


# ============================================================================
# Test Migration Scenario: Legacy to New Format
# ============================================================================

def test_migration_scenario_both_formats(client):
    """Test handling both legacy and new event formats during migration"""
    # Send legacy event
    legacy_event = {
        "type": "database.updated",
        "event_id": "evt_migration_001",
        "created_at": "2024-12-01T10:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "database",
            "id": "db_migration_001",
            "parent": {"type": "workspace", "workspace": True}
        }
    }
    
    response1 = client.post("/webhooks/notion", json=legacy_event)
    assert response1.status_code == 200
    
    # Send new data_source event
    new_event = {
        "type": "data_source.content_updated",
        "event_id": "evt_migration_002",
        "created_at": "2025-09-03T10:00:00Z",
        "workspace_id": "ws_abc123",
        "data": {
            "object": "database",
            "id": "db_migration_001",
            "parent": {
                "type": "workspace",
                "workspace": True,
                "data_source_id": "ds_multi_007"
            }
        }
    }
    
    response2 = client.post("/webhooks/notion", json=new_event)
    assert response2.status_code == 200
    
    # Verify both events were logged
    assert len(webhook_event_logs) == 2
    assert webhook_event_logs[0].event_type == "database.updated"
    assert webhook_event_logs[1].event_type == "data_source.content_updated"


# ============================================================================
# Test data_source_id in Parent Object
# ============================================================================

def test_data_source_id_extracted_correctly(client):
    """Test that data_source_id is correctly extracted from parent object"""
    event_payload = {
        "type": "data_source.content_updated",
        "event_id": "evt_parent_001",
        "created_at": "2025-09-03T16:00:00Z",
        "workspace_id": "ws_test",
        "data": {
            "object": "database",
            "id": "db_test_001",
            "parent": {
                "type": "page",
                "page_id": "page_parent_001",
                "data_source_id": "ds_test_001"
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    # Verify in response
    data = response.json()
    assert data["data_source_id"] == "ds_test_001"
    
    # Verify in log
    assert len(webhook_event_logs) == 1
    assert webhook_event_logs[0].data_source_id == "ds_test_001"


def test_missing_data_source_id_handled_gracefully(client):
    """Test that events without data_source_id are handled correctly"""
    event_payload = {
        "type": "page.updated",
        "event_id": "evt_no_ds_001",
        "created_at": "2025-09-03T17:00:00Z",
        "workspace_id": "ws_test",
        "data": {
            "object": "page",
            "id": "page_no_ds_001",
            "parent": {
                "type": "database",
                "database_id": "db_123"
            }
        }
    }
    
    response = client.post("/webhooks/notion", json=event_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["data_source_id"] is None
    
    assert webhook_event_logs[0].data_source_id is None


# ============================================================================
# Test Webhook Event Log Endpoints
# ============================================================================

def test_get_webhook_events_empty(client):
    """Test getting webhook events when none exist"""
    response = client.get("/webhooks/events")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 0
    assert data["events"] == []


def test_get_webhook_events_with_data(client):
    """Test getting webhook events after receiving webhooks"""
    # Send a few events
    for i in range(3):
        event_payload = {
            "type": "data_source.content_updated",
            "event_id": f"evt_test_{i}",
            "created_at": "2025-09-03T18:00:00Z",
            "workspace_id": "ws_test",
            "data": {
                "object": "database",
                "id": f"db_test_{i}",
                "parent": {
                    "type": "workspace",
                    "workspace": True,
                    "data_source_id": f"ds_test_{i}"
                }
            }
        }
        client.post("/webhooks/notion", json=event_payload)
    
    response = client.get("/webhooks/events")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 3


def test_get_webhook_events_filter_by_type(client):
    """Test filtering webhook events by event type"""
    # Send different event types
    event1 = {
        "type": "data_source.created",
        "event_id": "evt_filter_001",
        "created_at": "2025-09-03T19:00:00Z",
        "workspace_id": "ws_test",
        "data": {
            "object": "database",
            "id": "db_filter_001",
            "parent": {"type": "workspace", "workspace": True, "data_source_id": "ds_001"}
        }
    }
    
    event2 = {
        "type": "data_source.deleted",
        "event_id": "evt_filter_002",
        "created_at": "2025-09-03T19:01:00Z",
        "workspace_id": "ws_test",
        "data": {
            "object": "database",
            "id": "db_filter_002",
            "parent": {"type": "workspace", "workspace": True, "data_source_id": "ds_002"}
        }
    }
    
    client.post("/webhooks/notion", json=event1)
    client.post("/webhooks/notion", json=event2)
    
    # Filter by created
    response = client.get("/webhooks/events?event_type=data_source.created")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["events"][0]["event_type"] == "data_source.created"


def test_get_webhook_events_limit(client):
    """Test limiting number of returned webhook events"""
    # Send 10 events
    for i in range(10):
        event_payload = {
            "type": "data_source.content_updated",
            "event_id": f"evt_limit_{i}",
            "created_at": "2025-09-03T20:00:00Z",
            "workspace_id": "ws_test",
            "data": {
                "object": "database",
                "id": f"db_limit_{i}",
                "parent": {"type": "workspace", "workspace": True, "data_source_id": f"ds_{i}"}
            }
        }
        client.post("/webhooks/notion", json=event_payload)
    
    # Request only 5
    response = client.get("/webhooks/events?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5


# ============================================================================
# Test Webhook Statistics Endpoint
# ============================================================================

def test_get_webhook_stats_empty(client):
    """Test getting webhook statistics when no events exist"""
    response = client.get("/webhooks/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_events"] == 0
    assert data["data_source_events"] == 0
    assert data["legacy_events"] == 0
    assert data["events_with_data_source_id"] == 0


def test_get_webhook_stats_with_mixed_events(client):
    """Test webhook statistics with mixed event types"""
    # Send data_source events
    for i in range(3):
        event = {
            "type": "data_source.content_updated",
            "event_id": f"evt_stats_ds_{i}",
            "created_at": "2025-09-03T21:00:00Z",
            "workspace_id": "ws_test",
            "data": {
                "object": "database",
                "id": f"db_stats_{i}",
                "parent": {"type": "workspace", "workspace": True, "data_source_id": f"ds_stats_{i}"}
            }
        }
        client.post("/webhooks/notion", json=event)
    
    # Send legacy events
    for i in range(2):
        event = {
            "type": "database.updated",
            "event_id": f"evt_stats_legacy_{i}",
            "created_at": "2024-01-01T10:00:00Z",
            "workspace_id": "ws_test",
            "data": {
                "object": "database",
                "id": f"db_legacy_{i}",
                "parent": {"type": "workspace", "workspace": True}
            }
        }
        client.post("/webhooks/notion", json=event)
    
    response = client.get("/webhooks/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_events"] == 5
    assert data["data_source_events"] == 3
    assert data["legacy_events"] == 2
    assert data["events_with_data_source_id"] == 3
    assert data["by_event_type"]["data_source.content_updated"] == 3
    assert data["by_event_type"]["database.updated"] == 2


# ============================================================================
# Test Webhook Signature Verification
# ============================================================================

def test_webhook_signature_verification():
    """Test HMAC-SHA256 signature verification"""
    secret = "test_secret_key"
    timestamp = "1234567890"
    body = b'{"test": "data"}'
    
    # Generate valid signature
    signed_content = f"{timestamp}:{body.decode('utf-8')}"
    valid_signature = hmac.new(
        secret.encode('utf-8'),
        signed_content.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Test valid signature
    assert verify_webhook_signature(valid_signature, timestamp, body, secret) is True
    
    # Test invalid signature
    assert verify_webhook_signature("invalid_signature", timestamp, body, secret) is False
    
    # Test wrong timestamp
    assert verify_webhook_signature(valid_signature, "wrong_timestamp", body, secret) is False


def test_invalid_webhook_payload(client):
    """Test handling of invalid webhook payload"""
    invalid_payload = {
        "invalid": "data",
        "missing": "required_fields"
    }
    
    response = client.post("/webhooks/notion", json=invalid_payload)
    assert response.status_code == 400
    assert "Invalid webhook payload" in response.json()["detail"]


# ============================================================================
# Test Helper Functions
# ============================================================================

def test_is_data_source_event():
    """Test is_data_source_event helper function"""
    assert is_data_source_event("data_source.content_updated") is True
    assert is_data_source_event("data_source.schema_updated") is True
    assert is_data_source_event("data_source.created") is True
    assert is_data_source_event("data_source.moved") is True
    assert is_data_source_event("data_source.deleted") is True
    assert is_data_source_event("data_source.undeleted") is True
    assert is_data_source_event("database.updated") is False
    assert is_data_source_event("page.created") is False


def test_is_legacy_event():
    """Test is_legacy_event helper function"""
    assert is_legacy_event("database.updated") is True
    assert is_legacy_event("page.created") is True
    assert is_legacy_event("page.updated") is True
    assert is_legacy_event("page.deleted") is True
    assert is_legacy_event("data_source.content_updated") is False
    assert is_legacy_event("data_source.created") is False

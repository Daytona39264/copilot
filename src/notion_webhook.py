"""
Notion Webhook Integration for API v2025-09-03

Supports multi-source database features with new data_source events
and data_source_id in parent objects.
"""

from enum import Enum
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime, UTC


class NotionEventType(str, Enum):
    """Webhook event types for Notion API"""
    # Legacy database events
    DATABASE_UPDATED = "database.updated"
    
    # New data_source events (API v2025-09-03)
    DATA_SOURCE_CONTENT_UPDATED = "data_source.content_updated"
    DATA_SOURCE_SCHEMA_UPDATED = "data_source.schema_updated"
    DATA_SOURCE_CREATED = "data_source.created"
    DATA_SOURCE_MOVED = "data_source.moved"
    DATA_SOURCE_DELETED = "data_source.deleted"
    DATA_SOURCE_UNDELETED = "data_source.undeleted"
    
    # Page events
    PAGE_CREATED = "page.created"
    PAGE_UPDATED = "page.updated"
    PAGE_DELETED = "page.deleted"


class ParentObject(BaseModel):
    """Parent object in webhook payload"""
    type: str
    database_id: Optional[str] = None
    page_id: Optional[str] = None
    workspace: Optional[bool] = None
    # New field for multi-source database support
    data_source_id: Optional[str] = None


class WebhookEventData(BaseModel):
    """Data object in webhook event"""
    object: str
    id: str
    parent: Optional[ParentObject] = None
    created_time: Optional[str] = None
    last_edited_time: Optional[str] = None
    # Additional properties can be added as needed
    properties: Optional[Dict[str, Any]] = None


class NotionWebhookEvent(BaseModel):
    """Complete Notion webhook event structure"""
    event_type: NotionEventType = Field(..., alias="type")
    event_id: str
    created_at: str
    workspace_id: str
    data: WebhookEventData
    
    model_config = {"populate_by_name": True}


class WebhookEventLog(BaseModel):
    """Internal log entry for processed webhook events"""
    event_id: str
    event_type: str
    workspace_id: str
    data_source_id: Optional[str] = None
    object_id: str
    received_at: datetime
    processed: bool = False
    error: Optional[str] = None


# In-memory storage for webhook events (for demo purposes)
webhook_event_logs: List[WebhookEventLog] = []


def is_data_source_event(event_type: str) -> bool:
    """Check if event is a new data_source event type"""
    data_source_events = [
        NotionEventType.DATA_SOURCE_CONTENT_UPDATED,
        NotionEventType.DATA_SOURCE_SCHEMA_UPDATED,
        NotionEventType.DATA_SOURCE_CREATED,
        NotionEventType.DATA_SOURCE_MOVED,
        NotionEventType.DATA_SOURCE_DELETED,
        NotionEventType.DATA_SOURCE_UNDELETED,
    ]
    return event_type in [e.value for e in data_source_events]


def is_legacy_event(event_type: str) -> bool:
    """Check if event is a legacy event type"""
    legacy_events = [
        NotionEventType.DATABASE_UPDATED,
        NotionEventType.PAGE_CREATED,
        NotionEventType.PAGE_UPDATED,
        NotionEventType.PAGE_DELETED,
    ]
    return event_type in [e.value for e in legacy_events]


def process_webhook_event(event: NotionWebhookEvent) -> WebhookEventLog:
    """
    Process a webhook event and create a log entry
    
    Handles both legacy and new event formats, including:
    - New data_source events
    - data_source_id in parent object
    """
    # Extract data_source_id if present
    data_source_id = None
    if event.data.parent and event.data.parent.data_source_id:
        data_source_id = event.data.parent.data_source_id
    
    # Create log entry
    log_entry = WebhookEventLog(
        event_id=event.event_id,
        event_type=event.event_type.value,
        workspace_id=event.workspace_id,
        data_source_id=data_source_id,
        object_id=event.data.id,
        received_at=datetime.now(UTC),
        processed=True
    )
    
    # Store in memory
    webhook_event_logs.append(log_entry)
    
    return log_entry


def verify_webhook_signature(
    signature: str, 
    timestamp: str, 
    body: bytes, 
    secret: str
) -> bool:
    """
    Verify Notion webhook signature
    
    Notion uses HMAC-SHA256 for webhook signature verification.
    The signature is computed as: HMAC(secret, timestamp + ":" + body)
    """
    import hmac
    import hashlib
    
    # Construct the signed content
    signed_content = f"{timestamp}:{body.decode('utf-8')}"
    
    # Compute HMAC
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        signed_content.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures (constant-time comparison)
    return hmac.compare_digest(signature, expected_signature)

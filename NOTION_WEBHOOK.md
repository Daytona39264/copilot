# Notion Webhook Integration

This document describes the Notion webhook integration that supports the new multi-source database features introduced in Notion API v2025-09-03.

## Overview

The webhook integration provides endpoints to receive and process Notion webhook events, with full support for:

- **New data_source events** introduced in API v2025-09-03
- **data_source_id** field in parent objects
- **Backward compatibility** with legacy event types during migration

## Supported Event Types

### New Data Source Events (API v2025-09-03)

- `data_source.content_updated` - Triggered when database content is updated
- `data_source.schema_updated` - Triggered when database schema changes
- `data_source.created` - Triggered when a new database is created
- `data_source.moved` - Triggered when a database is moved
- `data_source.deleted` - Triggered when a database is deleted
- `data_source.undeleted` - Triggered when a database is restored

### Legacy Events (Backward Compatible)

- `database.updated` - Legacy database update event
- `page.created` - Page creation event
- `page.updated` - Page update event
- `page.deleted` - Page deletion event

## Endpoints

### POST /webhooks/notion

Main webhook endpoint for receiving Notion events.

**Headers:**
- `notion-signature` (optional) - HMAC-SHA256 signature for verification
- `notion-timestamp` (optional) - Timestamp used in signature computation

**Request Body:**
```json
{
  "type": "data_source.content_updated",
  "event_id": "evt_123456",
  "created_at": "2025-09-03T10:00:00Z",
  "workspace_id": "ws_abc123",
  "data": {
    "object": "database",
    "id": "db_789xyz",
    "parent": {
      "type": "workspace",
      "workspace": true,
      "data_source_id": "ds_multi_001"
    }
  }
}
```

**Response:**
```json
{
  "status": "success",
  "event_id": "evt_123456",
  "event_type": "data_source.content_updated",
  "data_source_id": "ds_multi_001",
  "is_data_source_event": true,
  "is_legacy_event": false
}
```

### GET /webhooks/events

Retrieve webhook event logs.

**Query Parameters:**
- `event_type` (optional) - Filter by specific event type
- `limit` (optional, default: 50) - Maximum number of events to return

**Response:**
```json
{
  "total": 3,
  "events": [
    {
      "event_id": "evt_123456",
      "event_type": "data_source.content_updated",
      "workspace_id": "ws_abc123",
      "data_source_id": "ds_multi_001",
      "object_id": "db_789xyz",
      "received_at": "2025-09-03T10:00:00.000000",
      "processed": true,
      "error": null
    }
  ]
}
```

### GET /webhooks/stats

Get webhook event statistics.

**Response:**
```json
{
  "total_events": 10,
  "data_source_events": 6,
  "legacy_events": 4,
  "events_with_data_source_id": 6,
  "by_event_type": {
    "data_source.content_updated": 3,
    "data_source.schema_updated": 2,
    "data_source.created": 1,
    "database.updated": 4
  }
}
```

## Configuration

### Environment Variables

- `NOTION_WEBHOOK_SECRET` - Secret key for webhook signature verification (optional but recommended)

If not set, signature verification is skipped. For production deployments, always configure this secret.

## Webhook Signature Verification

The integration supports Notion's HMAC-SHA256 signature verification to ensure webhook authenticity.

**Algorithm:**
```
signature = HMAC-SHA256(secret, timestamp + ":" + body)
```

The signature is provided in the `notion-signature` header, and the timestamp in the `notion-timestamp` header.

## Migration Guide

### Supporting Both Legacy and New Events

During the migration period, the webhook handler supports both legacy and new event formats:

**Legacy Event (database.updated):**
```json
{
  "type": "database.updated",
  "event_id": "evt_legacy_001",
  "created_at": "2024-01-01T10:00:00Z",
  "workspace_id": "ws_abc123",
  "data": {
    "object": "database",
    "id": "db_legacy_001",
    "parent": {
      "type": "workspace",
      "workspace": true
    }
  }
}
```

**New Event (data_source.content_updated):**
```json
{
  "type": "data_source.content_updated",
  "event_id": "evt_new_001",
  "created_at": "2025-09-03T10:00:00Z",
  "workspace_id": "ws_abc123",
  "data": {
    "object": "database",
    "id": "db_new_001",
    "parent": {
      "type": "workspace",
      "workspace": true,
      "data_source_id": "ds_multi_001"
    }
  }
}
```

Both formats are accepted and processed correctly.

### Transition Steps

1. **Deploy the new webhook handler** (this implementation)
2. **Test with both event formats** to ensure compatibility
3. **Update Notion webhook subscriptions** to API version 2025-09-03
4. **Monitor event logs** using `/webhooks/stats` to verify new events are being received
5. **Optional: Remove legacy event handling** after confirmation that only new events are received

## Testing

The integration includes comprehensive tests covering:

- All 6 new data_source event types
- Legacy event compatibility
- data_source_id extraction and handling
- Webhook signature verification
- Event filtering and statistics
- Migration scenarios

Run tests with:
```bash
pytest tests/test_notion_webhook.py -v
```

## Example Usage

### Setting Up a Webhook

1. Configure your Notion integration to send webhooks to `https://your-domain.com/webhooks/notion`
2. Set the `NOTION_WEBHOOK_SECRET` environment variable with your webhook secret
3. Subscribe to the desired event types (recommend subscribing to all data_source.* events)

### Monitoring Webhooks

Check webhook statistics:
```bash
curl https://your-domain.com/webhooks/stats
```

View recent events:
```bash
curl https://your-domain.com/webhooks/events?limit=10
```

Filter by event type:
```bash
curl https://your-domain.com/webhooks/events?event_type=data_source.content_updated
```

## Data Source ID

The `data_source_id` field in the parent object identifies the data source for multi-source databases. This field is:

- Present in all new data_source.* events
- Available in the parent object when databases are associated with specific data sources
- Extracted and stored in event logs for tracking and analysis
- Optional (not present in legacy events or events without data source associations)

## Security Considerations

1. **Always use HTTPS** in production for webhook endpoints
2. **Configure webhook secret** (`NOTION_WEBHOOK_SECRET`) and verify signatures
3. **Validate event data** before processing (already implemented in the webhook handler)
4. **Monitor for unusual activity** using the statistics endpoint
5. **Rate limit** webhook endpoints if needed (can be added via middleware)

## Troubleshooting

### Invalid Signature Error (401)

- Verify `NOTION_WEBHOOK_SECRET` matches the secret configured in Notion
- Check that timestamp is current (within acceptable time window)
- Ensure the request body hasn't been modified

### Invalid Payload Error (400)

- Verify the webhook is sending properly formatted JSON
- Check that all required fields are present
- Review Notion API documentation for correct event structure

### No Events Being Received

- Verify webhook URL is correctly configured in Notion
- Check firewall/network settings
- Ensure the endpoint is accessible from Notion's servers
- Review Notion webhook delivery logs

## References

- [Notion API Changelog - Multi-source Databases](https://developers.notion.com/changelog/multi-source-databases)
- [Notion API Documentation](https://developers.notion.com/)
- [Webhook Security Best Practices](https://developers.notion.com/docs/webhooks-security)

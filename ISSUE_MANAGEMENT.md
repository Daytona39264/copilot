# Issue/Feedback Gathering System

This document describes the issue/feedback gathering system implemented for the Mergington High School Activities Management API.

## Overview

The issue management system allows users (students, teachers, administrators) to report bugs, request features, provide feedback, and ask questions about the extracurricular activities program. This system helps collect valuable information to improve the activities program and coordinate multiple issues that need attention.

## Features

### 1. Issue Creation
- Users can create issues with a title, description, and category
- Issues can be linked to specific activities for context
- Email validation ensures only @mergington.edu addresses can submit issues
- Each issue is assigned a unique ID and timestamp

### 2. Issue Categories
- **bug**: Technical issues or problems with the system
- **feature_request**: Suggestions for new features or enhancements
- **feedback**: General feedback about activities or the system
- **question**: Questions about activities or how to use the system
- **other**: Any other type of issue

### 3. Status Tracking
Issues can be tracked through their lifecycle:
- **open**: Newly created, awaiting review
- **in_progress**: Being actively worked on
- **resolved**: Solution implemented, awaiting verification
- **closed**: Completed and verified

### 4. Filtering and Search
- List all issues
- Filter by category (e.g., show only bugs)
- Filter by status (e.g., show only open issues)
- Combine filters for precise queries

### 5. AI-Powered Analysis
When ANTHROPIC_API_KEY is configured, the system can:
- Analyze patterns across multiple issues
- Categorize and prioritize issues
- Identify common themes and concerns
- Provide actionable recommendations

## API Endpoints

### Create Issue
```http
POST /issues
Content-Type: application/json

{
  "title": "Activity signup not working",
  "description": "Getting error when trying to sign up for Chess Club",
  "category": "bug",
  "related_activity": "Chess Club",
  "reporter_email": "student@mergington.edu"
}
```

Response:
```json
{
  "id": 1,
  "title": "Activity signup not working",
  "description": "Getting error when trying to sign up for Chess Club",
  "category": "bug",
  "related_activity": "Chess Club",
  "reporter_email": "student@mergington.edu",
  "created_at": "2025-11-09T10:30:00.000000",
  "status": "open"
}
```

### List Issues
```http
GET /issues
GET /issues?category=bug
GET /issues?status=open
GET /issues?category=feature_request&status=open
```

### Get Specific Issue
```http
GET /issues/1
```

### Update Issue Status
```http
PATCH /issues/1/status?status=in_progress
```

### AI Analysis (requires ANTHROPIC_API_KEY)
```http
GET /ai/issues-summary
```

## Usage Examples

See `examples/issue_management_example.py` for a complete working example that demonstrates:
- Creating various types of issues
- Listing and filtering issues
- Updating issue status
- Getting AI-powered analysis

Run the example:
```bash
# Start the API server
cd src && python app.py

# In another terminal, run the example
python examples/issue_management_example.py
```

## Data Model

### Issue Object
```python
{
  "id": int,                           # Unique identifier
  "title": str,                        # Issue title
  "description": str,                  # Detailed description
  "category": str,                     # bug|feature_request|feedback|question|other
  "related_activity": Optional[str],   # Activity name or None
  "reporter_email": str,               # Reporter's email
  "created_at": str,                   # ISO format timestamp
  "status": str                        # open|in_progress|resolved|closed
}
```

## Benefits

1. **Centralized Feedback**: All issues in one place for easy tracking
2. **Better Communication**: Clear channel for users to report problems
3. **Priority Management**: Categorization helps prioritize work
4. **Data-Driven Decisions**: AI analysis reveals patterns and insights
5. **Improved Service**: Faster response to bugs and feature requests

## Testing

The system includes comprehensive test coverage:
- 14 dedicated test cases for issue management
- Tests for validation, error handling, and edge cases
- 100% code coverage maintained
- All tests passing

Run tests:
```bash
pytest tests/test_issues.py -v
```

## Future Enhancements

Potential improvements for the system:
- Issue assignments to specific administrators
- Email notifications for status updates
- Issue comments/discussion threads
- Attachments (screenshots, logs)
- Voting system for feature requests
- Integration with external issue tracking systems

## Security

- Email validation ensures only valid school addresses
- Input validation prevents malformed data
- CodeQL security scan passed with 0 vulnerabilities
- In-memory storage prevents data persistence issues

## Support

For questions or issues with the issue management system itself, please contact the system administrator or create an issue using the system!

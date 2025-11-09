# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- Report issues and provide feedback about activities
- Track and manage issues with status updates
- AI-powered issue analysis and summarization

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

### Activities Management
| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| GET    | `/activities/{activity_name}/availability`                        | Get capacity information for a specific activity                    |

### Issue/Feedback Management
| Method | Endpoint                      | Description                                          |
| ------ | ----------------------------- | ---------------------------------------------------- |
| POST   | `/issues`                     | Create a new issue or feedback item                  |
| GET    | `/issues`                     | Get all issues (supports filtering by category/status)|
| GET    | `/issues/{issue_id}`          | Get a specific issue by ID                           |
| PATCH  | `/issues/{issue_id}/status`   | Update the status of an issue                        |

### AI-Powered Features
| Method | Endpoint                      | Description                                          |
| ------ | ----------------------------- | ---------------------------------------------------- |
| GET    | `/ai/status`                  | Check if AI features are enabled                     |
| GET    | `/ai/issues-summary`          | Get AI-powered analysis of all issues                |
| POST   | `/ai/suggest-activities`      | Get personalized activity suggestions                |
| POST   | `/ai/chat`                    | Chat with AI about activities                        |
| GET    | `/ai/activity-summary/{name}` | Generate enhanced activity description               |
| GET    | `/ai/participation-insights`  | Analyze participation patterns                       |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

3. **Issues** - Uses numeric ID as identifier:
   - Title
   - Description
   - Category (bug, feature_request, feedback, question, other)
   - Related activity (optional)
   - Reporter email
   - Created timestamp
   - Status (open, in_progress, resolved, closed)

All data is stored in memory, which means data will be reset when the server restarts.

## Issue Management

The issue management system allows users to report bugs, request features, provide feedback, and ask questions about activities. Each issue includes:

- **Categories**: bug, feature_request, feedback, question, other
- **Status Tracking**: open → in_progress → resolved → closed
- **Activity Linking**: Issues can be associated with specific activities
- **Email Validation**: All reporters must use valid @mergington.edu email addresses

AI-powered analysis can categorize, summarize, and provide insights about submitted issues to help prioritize improvements.

"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

Enhanced with AI capabilities powered by Anthropic's Claude.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional, Callable
import os
import re
from pathlib import Path
from functools import wraps

# AI Integration (optional - only enabled if ANTHROPIC_API_KEY is set)
anthropic_client = None
try:  # pragma: no cover - optional dependency
    from anthropic import Anthropic
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    if ANTHROPIC_API_KEY:
        anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
        AI_ENABLED = True
    else:
        AI_ENABLED = False
except ImportError:  # pragma: no cover - optional dependency
    AI_ENABLED = False

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# AI configuration constants
AI_MODEL = "claude-sonnet-4-5-20250929"

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Swimming Club": {
        "description": "Swimming training and water sports",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Art Studio": {
        "description": "Express creativity through painting and drawing",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Theater arts and performance training",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": []
    },
    "Debate Team": {
        "description": "Learn public speaking and argumentation skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Science Club": {
        "description": "Hands-on experiments and scientific exploration",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    }
}


# ============================================================================
# AI Helper Functions
# ============================================================================

def require_ai_enabled(func: Callable):
    """Decorator to check if AI features are enabled before executing endpoint"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not AI_ENABLED:
            raise HTTPException(
                status_code=503,
                detail="AI features not enabled. Set ANTHROPIC_API_KEY environment variable."
            )
        return func(*args, **kwargs)
    return wrapper


def call_anthropic_api(prompt: str, max_tokens: int = 500, system_prompt: Optional[str] = None):
    """
    Call Anthropic API with consistent error handling
    
    Args:
        prompt: The user prompt to send
        max_tokens: Maximum tokens in response (default 500)
        system_prompt: Optional system prompt
        
    Returns:
        The text content from the API response
        
    Raises:
        HTTPException: 500 error if API call fails
    """
    try:
        kwargs = {
            "model": AI_MODEL,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system_prompt:
            kwargs["system"] = system_prompt
            
        response = anthropic_client.messages.create(**kwargs)
        return response.content[0].text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")


def build_activities_context() -> str:
    """Build a formatted string describing all available activities"""
    context = "Available extracurricular activities:\n\n"
    for name, details in activities.items():
        participants_count = len(details["participants"])
        max_participants = details["max_participants"]
        context += f"- {name}:\n"
        context += f"  Description: {details['description']}\n"
        context += f"  Schedule: {details['schedule']}\n"
        context += f"  Capacity: {participants_count}/{max_participants}\n\n"
    return context


def get_participation_data() -> List[dict]:
    """Get participation statistics for all activities"""
    data = []
    for name, details in activities.items():
        capacity_percentage = (len(details["participants"]) / details["max_participants"]) * 100
        data.append({
            "activity": name,
            "participants": len(details["participants"]),
            "capacity": details["max_participants"],
            "fill_rate": f"{capacity_percentage:.1f}%"
        })
    return data


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


EMAIL_RE = re.compile(r"^[^@\s]+@mergington\.edu$", re.IGNORECASE)


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity

    Validations (subject to acceptance criteria):
    - 404 if activity not found
    - 400 if email is invalid or wrong domain
    - 409 if already signed up (case-insensitive)
    - 409 if activity is full
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Normalize and validate email
    normalized = (email or "").strip()
    if not normalized or not EMAIL_RE.match(normalized):
        raise HTTPException(status_code=400, detail="Invalid email")

    # Get the specific activity
    activity = activities[activity_name]

    # Prevent duplicate signups (case-insensitive)
    norm_lower = normalized.lower()
    if any(p.lower() == norm_lower for p in activity["participants"]):
        raise HTTPException(status_code=409, detail="Already signed up")

    # Enforce capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=409, detail="Activity is full")

    # Add student
    activity["participants"].append(norm_lower)
    return {"message": f"Signed up {normalized} for {activity_name}"}


def _availability_for(activity_name: str) -> dict:
    """Return availability details for a given activity."""
    activity = activities[activity_name]
    total_slots = activity["max_participants"]
    taken_slots = len(activity["participants"])
    return {
        "activity_name": activity_name,
        "total_slots": total_slots,
        "taken_slots": taken_slots,
        "available_slots": max(total_slots - taken_slots, 0),
    }


@app.get("/activities/{activity_name}/availability")
def get_activity_availability(activity_name: str):
    """Return capacity information for a single activity."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    return _availability_for(activity_name)


# ============================================================================
# AI-Powered Endpoints (require ANTHROPIC_API_KEY environment variable)
# ============================================================================

class ActivitySuggestionRequest(BaseModel):
    student_interests: List[str]
    grade_level: int


class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None


@app.get("/ai/status")
def ai_status():
    """Check if AI features are enabled"""
    return {
        "ai_enabled": AI_ENABLED,
        "message": "AI features are enabled" if AI_ENABLED else "Set ANTHROPIC_API_KEY to enable AI features"
    }


@app.post("/ai/suggest-activities")
@require_ai_enabled
def suggest_activities(request: ActivitySuggestionRequest):  # pragma: no cover - requires external AI service
    """
    AI-powered activity suggestions based on student interests
    Requires ANTHROPIC_API_KEY environment variable
    """
    interests_str = ", ".join(request.student_interests)
    available_activities = list(activities.keys())

    prompt = f"""Based on the following student information, suggest the top 3 activities from this list
that would be the best fit, and explain why:

Available Activities: {", ".join(available_activities)}

Student Profile:
- Grade Level: {request.grade_level}
- Interests: {interests_str}

For each suggestion, provide:
1. Activity name
2. Why it's a good fit (2-3 sentences)
3. What the student might enjoy about it

Keep the response concise and encouraging."""

    suggestions = call_anthropic_api(prompt, max_tokens=600)
    
    return {
        "suggestions": suggestions,
        "student_interests": request.student_interests,
        "grade_level": request.grade_level
    }


@app.post("/ai/chat")
@require_ai_enabled
def chat_about_activities(request: ChatRequest):  # pragma: no cover - requires external AI service
    """
    Chat with AI about activities and the school program
    Requires ANTHROPIC_API_KEY environment variable
    """
    activities_context = build_activities_context()
    
    system_prompt = f"""You are a helpful assistant for Mergington High School's
extracurricular activities program. Answer questions about activities, schedules,
and help students find activities that match their interests.

{activities_context}

Be friendly, encouraging, and informative."""

    response_text = call_anthropic_api(request.message, max_tokens=500, system_prompt=system_prompt)
    
    return {
        "response": response_text,
        "message": request.message
    }


@app.get("/ai/activity-summary/{activity_name}")
@require_ai_enabled
def generate_activity_summary(activity_name: str):  # pragma: no cover - requires external AI service
    """
    Generate an enhanced description for an activity using AI
    Requires ANTHROPIC_API_KEY environment variable
    """
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    prompt = f"""Create an engaging, student-friendly summary for this extracurricular activity:

Activity: {activity_name}
Current Description: {activity['description']}
Schedule: {activity['schedule']}

Write a compelling 3-4 sentence description that would excite high school students
to join. Focus on benefits, skills they'll learn, and the fun they'll have."""

    ai_summary = call_anthropic_api(prompt, max_tokens=300)
    
    return {
        "activity_name": activity_name,
        "original_description": activity["description"],
        "ai_enhanced_summary": ai_summary
    }


@app.get("/ai/participation-insights")
@require_ai_enabled
def analyze_participation():  # pragma: no cover - requires external AI service
    """
    Analyze participation patterns across activities using AI
    Requires ANTHROPIC_API_KEY environment variable
    """
    analysis_data = get_participation_data()

    prompt = f"""Analyze the following participation data for Mergington High School's
extracurricular activities:

{analysis_data}

Provide:
1. Key observations about participation patterns
2. Which activities are most/least popular
3. 2-3 actionable recommendations to improve overall participation

Keep the analysis concise and practical."""

    ai_insights = call_anthropic_api(prompt, max_tokens=600)
    
    return {
        "participation_data": analysis_data,
        "ai_insights": ai_insights
    }

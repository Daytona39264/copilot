"""
FastAPI Integration with Anthropic SDK

This example demonstrates how to integrate Claude AI
into a FastAPI application for various use cases.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from anthropic import Anthropic, AsyncAnthropic
import os
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(title="AI-Powered API with Claude")

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here"))
async_client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here"))


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    max_tokens: int = 1000


class ChatResponse(BaseModel):
    response: str
    model: str
    input_tokens: int
    output_tokens: int


class ActivitySuggestionRequest(BaseModel):
    student_interests: List[str]
    grade_level: int


class ActivitySuggestion(BaseModel):
    suggestion: str


# Endpoints

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_claude(request: ChatRequest):
    """
    Simple chat endpoint that sends a message to Claude
    """
    try:
        kwargs = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": request.max_tokens,
            "messages": [{"role": "user", "content": request.message}]
        }

        if request.system_prompt:
            kwargs["system"] = request.system_prompt

        response = await async_client.messages.create(**kwargs)

        return ChatResponse(
            response=response.content[0].text,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")


@app.post("/api/suggest-activities", response_model=ActivitySuggestion)
async def suggest_activities(request: ActivitySuggestionRequest):
    """
    Generate personalized activity suggestions based on student interests
    """
    try:
        interests_str = ", ".join(request.student_interests)

        prompt = f"""Based on the following student information, suggest 2-3 extracurricular
activities that would be a good fit:

- Grade Level: {request.grade_level}
- Interests: {interests_str}

Provide specific, actionable suggestions with brief explanations."""

        response = await async_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        return ActivitySuggestion(suggestion=response.content[0].text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")


@app.get("/api/summarize-activity/{activity_name}")
async def summarize_activity(activity_name: str):
    """
    Generate a compelling summary for an activity using AI
    """
    try:
        prompt = f"""Create a brief, engaging description for a high school
extracurricular activity called "{activity_name}".
Make it appealing to students in 2-3 sentences."""

        response = await async_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        return {"activity_name": activity_name, "summary": response.content[0].text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")


@app.post("/api/analyze-participation")
async def analyze_participation(activity_data: dict):
    """
    Analyze activity participation patterns using AI
    """
    try:
        prompt = f"""Analyze the following activity participation data and provide insights:

{activity_data}

Provide:
1. Key trends
2. Popular activities
3. Recommendations for improving participation"""

        response = await async_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )

        return {"analysis": response.content[0].text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")


# Streaming endpoint example
from fastapi.responses import StreamingResponse
import json


@app.post("/api/chat-stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint that returns responses as they're generated
    """
    async def generate():
        try:
            kwargs = {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": request.max_tokens,
                "messages": [{"role": "user", "content": request.message}]
            }

            if request.system_prompt:
                kwargs["system"] = request.system_prompt

            async with async_client.messages.stream(**kwargs) as stream:
                async for text in stream.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

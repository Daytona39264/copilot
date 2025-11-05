# Anthropic SDK Examples

Comprehensive examples for using the Anthropic Python SDK to integrate Claude AI into your applications.

## 📋 Examples Overview

| File | Description | Difficulty |
|------|-------------|------------|
| `01_basic_usage.py` | SDK fundamentals and basic messages | Beginner |
| `02_conversations.py` | Multi-turn conversations and context | Beginner |
| `03_advanced_features.py` | Streaming, tools, vision, async | Advanced |
| `04_fastapi_integration.py` | Web API integration with FastAPI | Intermediate |

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Run Examples

```bash
# Navigate to examples directory
cd examples/anthropic_sdk

# Run each example
python 01_basic_usage.py
python 02_conversations.py
python 03_advanced_features.py

# Run FastAPI integration (in separate terminal)
python 04_fastapi_integration.py
# Then test at http://localhost:8000/docs
```

## 📖 Detailed Guide

### Example 1: Basic Usage

**What you'll learn:**
- Initializing the Anthropic client
- Sending simple messages
- Using system prompts
- Adjusting parameters (temperature, max_tokens)
- Understanding token usage

**Key code:**
```python
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.content[0].text)
```

**Try modifying:**
- Change the model to `claude-sonnet-4-5-20250929` for faster responses
- Adjust `temperature` (0.0-1.0) to control randomness
- Add a `system` prompt to set behavior

### Example 2: Conversations

**What you'll learn:**
- Managing conversation history
- Building context-aware applications
- Creating a conversation manager
- Interactive chat loops

**Key feature - ConversationManager:**
```python
conversation = ConversationManager()

# Turn 1
conversation.add_user_message("What's the capital of France?")
response, _ = conversation.get_response()

# Turn 2 - Claude remembers context
conversation.add_user_message("What's the population?")
response, _ = conversation.get_response()
```

**Use cases:**
- Chatbots
- Coding assistants
- Customer support
- Interactive tutorials

### Example 3: Advanced Features

**What you'll learn:**
- Streaming responses for real-time output
- Tool use (function calling)
- Vision capabilities with images
- Error handling patterns
- Async operations

**Streaming example:**
```python
with client.messages.stream(
    model="claude-opus-4-1-20250805",
    max_tokens=500,
    messages=[{"role": "user", "content": "Write a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**Tool use example:**
```python
tools = [{
    "name": "calculator",
    "description": "Perform calculations",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {"type": "string"}
        }
    }
}]

response = client.messages.create(
    model="claude-opus-4-1-20250805",
    tools=tools,
    messages=[{"role": "user", "content": "What's 15 * 27?"}]
)
```

### Example 4: FastAPI Integration

**What you'll learn:**
- Building AI-powered web APIs
- Async request handling
- Streaming over HTTP
- Pydantic models for requests
- Production-ready patterns

**Example endpoint:**
```python
@app.post("/api/chat")
async def chat(request: ChatRequest):
    response = await async_client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=request.max_tokens,
        messages=[{"role": "user", "content": request.message}]
    )
    return {"response": response.content[0].text}
```

**Run the server:**
```bash
python 04_fastapi_integration.py
```

**Test endpoints:**
```bash
# Simple chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Activity suggestions
curl -X POST http://localhost:8000/api/suggest-activities \
  -H "Content-Type: application/json" \
  -d '{"student_interests": ["coding"], "grade_level": 10}'
```

## 🎯 Use Cases

### 1. Chatbots & Assistants

Use `02_conversations.py` as a starting point:
- Customer support bots
- Educational assistants
- Personal productivity helpers

### 2. Content Generation

Use `01_basic_usage.py` with appropriate prompts:
- Writing assistance
- Code generation
- Documentation creation

### 3. Data Analysis

Use `03_advanced_features.py` with tool use:
- Automated insights
- Report generation
- Pattern recognition

### 4. Web Applications

Use `04_fastapi_integration.py` as a template:
- AI-powered features in existing apps
- Real-time AI interactions
- Scalable AI services

## 🔧 Configuration

### Models

Choose the right model for your use case:

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `claude-opus-4-1-20250805` | Complex reasoning, coding | Slow | High |
| `claude-sonnet-4-5-20250929` | Balanced performance | Medium | Medium |
| `claude-haiku-4-0-20250305` | Simple tasks, speed | Fast | Low |

### Parameters

**Temperature (0.0 - 1.0)**
- `0.0` - Deterministic, focused responses
- `0.7` - Balanced creativity
- `1.0` - Maximum creativity

**Max Tokens**
- Limits response length
- 1 token ≈ 4 characters
- Consider costs vs. needs

**System Prompt**
- Sets AI behavior and context
- Define role and constraints
- Provide background information

## 🔐 Security Best Practices

### 1. API Key Management

```python
# ✅ Good - Use environment variables
api_key = os.environ.get("ANTHROPIC_API_KEY")

# ❌ Bad - Hardcoded keys
api_key = "sk-ant-api03-..."  # NEVER DO THIS
```

### 2. Input Validation

```python
# ✅ Good - Validate user input
def chat(message: str):
    if len(message) > 10000:
        raise ValueError("Message too long")
    # ... process message

# ❌ Bad - No validation
def chat(message: str):
    # Directly use unvalidated input
    response = client.messages.create(...)
```

### 3. Rate Limiting

```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)  # 10 calls per minute
def call_claude(message):
    return client.messages.create(...)
```

### 4. Error Handling

```python
from anthropic import APIError, RateLimitError

try:
    response = client.messages.create(...)
except RateLimitError:
    # Handle rate limit
    time.sleep(60)
except APIError as e:
    # Handle other API errors
    log_error(e)
```

## 📊 Monitoring & Optimization

### Track Token Usage

```python
response = client.messages.create(...)

print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Total cost: ${calculate_cost(response.usage)}")
```

### Caching Responses

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_ai_response(message: str) -> str:
    response = client.messages.create(...)
    return response.content[0].text
```

### Optimize Prompts

- Be specific and clear
- Provide examples when needed
- Use system prompts for context
- Keep prompts concise

## 🐛 Common Issues

### Issue: "API key not found"

**Solution:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
# Or add to .env file
```

### Issue: Rate limit errors

**Solution:**
```python
import time
from anthropic import RateLimitError

try:
    response = client.messages.create(...)
except RateLimitError:
    time.sleep(60)  # Wait before retrying
```

### Issue: Slow responses

**Solutions:**
1. Use a faster model (`claude-haiku-4-0-20250305`)
2. Reduce `max_tokens`
3. Use streaming for perceived speed
4. Implement caching

### Issue: Unexpected responses

**Solutions:**
1. Adjust temperature (lower for consistency)
2. Improve prompt clarity
3. Add examples to system prompt
4. Use conversation history for context

## 🎓 Next Steps

1. **Experiment** - Modify the examples
2. **Build** - Create your own application
3. **Integrate** - Add AI to existing projects
4. **Optimize** - Monitor and improve performance
5. **Scale** - Deploy to production

## 📚 Resources

- [Anthropic Documentation](https://docs.anthropic.com)
- [API Reference](https://docs.anthropic.com/en/api)
- [Python SDK GitHub](https://github.com/anthropics/anthropic-sdk-python)
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/prompt-engineering)
- [Rate Limits](https://docs.anthropic.com/en/api/rate-limits)

## 💡 Tips

1. **Start simple** - Begin with `01_basic_usage.py`
2. **Test iteratively** - Modify and re-run examples
3. **Read responses** - Understand what Claude returns
4. **Check logs** - Monitor token usage and costs
5. **Use streaming** - For better UX in applications
6. **Handle errors** - Always implement error handling
7. **Secure keys** - Never commit API keys

---

Ready to build with Claude? Start with `01_basic_usage.py`! 🚀

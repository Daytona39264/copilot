# MCP Server Examples

Model Context Protocol (MCP) server implementations for providing tools and resources to Claude AI.

## 🤔 What is MCP?

**Model Context Protocol (MCP)** is a standard protocol that allows AI models like Claude to:
- **Use tools** - Call functions to perform actions
- **Access resources** - Fetch data from external sources
- **Maintain context** - Keep track of state and information

Think of MCP as a way for AI to interact with your application's data and functionality in a structured, reliable way.

## 📋 Files

| File | Description | Use Case |
|------|-------------|----------|
| `simple_mcp_server.py` | Basic MCP implementation | Learning & development |
| `http_mcp_server.py` | Production HTTP server | Deployment & integration |

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install fastapi uvicorn
```

### Run the Servers

```bash
# Run simple MCP server (demo mode)
python simple_mcp_server.py

# Run HTTP MCP server
python http_mcp_server.py

# Server will be available at http://localhost:5000
```

### Test the Server

```bash
# Check health
curl http://localhost:5000/health

# List available tools
curl http://localhost:5000/tools

# List available resources
curl http://localhost:5000/resources

# Call a tool
curl -X POST http://localhost:5000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "get_activities", "arguments": {}}'

# Get a resource
curl -X POST http://localhost:5000/resources/get \
  -H "Content-Type: application/json" \
  -d '{"uri": "activities://stats"}'
```

## 📖 Simple MCP Server

### Overview

`simple_mcp_server.py` provides a basic MCP server implementation demonstrating core concepts.

### Features

**Tools:**
- `get_activities` - List all available activities
- `get_activity_details` - Get detailed info about an activity
- `check_availability` - Check if an activity has open spots

**Resources:**
- `activities://catalog` - Complete activities catalog
- `activities://stats` - Participation statistics

### Usage Example

```python
from simple_mcp_server import SchoolActivitiesMCPServer

# Initialize server
server = SchoolActivitiesMCPServer()

# List available tools
tools = server.list_tools()
print(f"Available tools: {[t['name'] for t in tools]}")

# Call a tool
result = await server.call_tool("get_activities", {})
print(f"Activities: {result['result']}")

# Get activity details
result = await server.call_tool(
    "get_activity_details",
    {"activity_name": "Chess Club"}
)
print(f"Details: {result['result']}")

# Access a resource
result = await server.get_resource("activities://stats")
print(f"Stats: {result['content']}")
```

### Extending the Server

Add your own tools:

```python
class MyMCPServer(SchoolActivitiesMCPServer):
    def __init__(self):
        super().__init__()
        self._register_custom_tools()

    def _register_custom_tools(self):
        self.register_tool(
            name="my_custom_tool",
            description="Description of what this tool does",
            parameters={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param1"]
            },
            handler=self._handle_my_custom_tool
        )

    async def _handle_my_custom_tool(self, args):
        param1 = args.get("param1")
        # Your logic here
        return {"result": "success"}
```

## 🌐 HTTP MCP Server

### Overview

`http_mcp_server.py` provides a production-ready HTTP interface for the MCP server using FastAPI.

### Features

- RESTful API endpoints
- Health checks
- Comprehensive error handling
- OpenAPI documentation
- Convenience API endpoints

### API Endpoints

**Core MCP Endpoints:**
```
GET  /                  - Server info
GET  /health            - Health check
GET  /tools             - List all tools
GET  /resources         - List all resources
POST /tools/call        - Execute a tool
POST /resources/get     - Fetch a resource
```

**Convenience Endpoints:**
```
GET  /api/activities                        - List activities
GET  /api/activities/{name}                 - Get activity details
GET  /api/activities/{name}/availability    - Check availability
GET  /api/stats                             - Get participation stats
```

### Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

### Usage in Applications

#### Python Client

```python
import requests

BASE_URL = "http://localhost:5000"

# Call a tool
response = requests.post(f"{BASE_URL}/tools/call", json={
    "tool_name": "get_activities",
    "arguments": {}
})
activities = response.json()["result"]

# Get activity details
response = requests.post(f"{BASE_URL}/tools/call", json={
    "tool_name": "get_activity_details",
    "arguments": {"activity_name": "Chess Club"}
})
details = response.json()["result"]

# Access a resource
response = requests.post(f"{BASE_URL}/resources/get", json={
    "uri": "activities://stats"
})
stats = response.json()["content"]
```

#### JavaScript/TypeScript

```javascript
const BASE_URL = 'http://localhost:5000';

// Call a tool
const response = await fetch(`${BASE_URL}/tools/call`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    tool_name: 'get_activities',
    arguments: {}
  })
});
const data = await response.json();
console.log(data.result);
```

#### cURL

```bash
# Call a tool
curl -X POST http://localhost:5000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_activity_details",
    "arguments": {"activity_name": "Chess Club"}
  }'
```

## 🔧 Integration with Claude

### Configuration

Configure Claude to use your MCP server:

```json
{
  "mcpServers": {
    "school-activities": {
      "url": "http://localhost:5000",
      "type": "http"
    }
  }
}
```

### Using Tools in Prompts

Once configured, Claude can use the tools:

```
User: What activities are available at the school?

Claude: Let me check the available activities.
[Calls get_activities tool]
Here are the available activities:
- Chess Club
- Programming Class
- Gym Class
...
```

### Resource Access

Claude can also access resources:

```
User: Show me the participation statistics

Claude: Let me fetch the latest statistics.
[Accesses activities://stats resource]
Here are the current statistics:
- Total activities: 9
- Total capacity: 168
- Current participants: 6
...
```

## 🔨 Development

### Adding New Tools

1. **Define the tool** in `_register_tools()`:

```python
self.register_tool(
    name="signup_for_activity",
    description="Sign up a student for an activity",
    parameters={
        "type": "object",
        "properties": {
            "activity_name": {"type": "string"},
            "student_email": {"type": "string"}
        },
        "required": ["activity_name", "student_email"]
    },
    handler=self._handle_signup
)
```

2. **Implement the handler**:

```python
async def _handle_signup(self, args):
    activity_name = args.get("activity_name")
    student_email = args.get("student_email")

    # Validation
    if activity_name not in self.activities:
        raise ValueError("Activity not found")

    # Logic
    activity = self.activities[activity_name]
    if len(activity["participants"]) >= activity["max_participants"]:
        raise ValueError("Activity is full")

    activity["participants"].append(student_email)

    return {
        "success": True,
        "message": f"Signed up {student_email} for {activity_name}"
    }
```

### Adding New Resources

1. **Define the resource** in `_register_resources()`:

```python
self.register_resource(
    uri="activities://schedules",
    name="Activity Schedules",
    description="Schedule information for all activities",
    handler=self._resource_schedules
)
```

2. **Implement the handler**:

```python
async def _resource_schedules(self):
    schedules = {}
    for name, details in self.activities.items():
        schedules[name] = {
            "activity": name,
            "schedule": details["schedule"]
        }
    return schedules
```

### Testing

```python
import asyncio
import pytest

async def test_get_activities():
    server = SchoolActivitiesMCPServer()
    result = await server.call_tool("get_activities", {})
    assert "result" in result
    assert isinstance(result["result"], list)

async def test_activity_details():
    server = SchoolActivitiesMCPServer()
    result = await server.call_tool(
        "get_activity_details",
        {"activity_name": "Chess Club"}
    )
    assert result["result"]["name"] == "Chess Club"

# Run tests
asyncio.run(test_get_activities())
asyncio.run(test_activity_details())
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build
docker build -f ../docker/Dockerfile.mcp -t mcp-server ../..

# Run
docker run -d --name mcp-server -p 5000:5000 mcp-server

# Check logs
docker logs -f mcp-server

# Test
curl http://localhost:5000/health
```

### Docker Compose

See `../docker/docker-compose.yml` for a complete setup including the MCP server.

## 📊 Monitoring

### Health Checks

```bash
# Basic health check
curl http://localhost:5000/health

# Check server info
curl http://localhost:5000/

# List available tools
curl http://localhost:5000/tools
```

### Logging

Add logging to your handlers:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def _handle_get_activities(self, args):
    logger.info("Getting activities list")
    activities = list(self.activities.keys())
    logger.info(f"Returned {len(activities)} activities")
    return activities
```

### Metrics

Track usage metrics:

```python
from collections import Counter

class MetricsMCPServer(SchoolActivitiesMCPServer):
    def __init__(self):
        super().__init__()
        self.call_counts = Counter()

    async def call_tool(self, tool_name, arguments):
        self.call_counts[tool_name] += 1
        return await super().call_tool(tool_name, arguments)

    def get_metrics(self):
        return {
            "total_calls": sum(self.call_counts.values()),
            "calls_by_tool": dict(self.call_counts)
        }
```

## 🔐 Security

### Authentication

Add authentication to the HTTP server:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "your-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return credentials.credentials

@app.post("/tools/call")
async def call_tool(request: ToolCallRequest, token: str = Depends(verify_token)):
    # ... your code
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/tools/call")
@limiter.limit("10/minute")
async def call_tool(request: ToolCallRequest):
    # ... your code
```

### Input Validation

Always validate tool arguments:

```python
async def _handle_get_activity_details(self, args):
    activity_name = args.get("activity_name")

    # Validation
    if not activity_name:
        raise ValueError("activity_name is required")

    if not isinstance(activity_name, str):
        raise ValueError("activity_name must be a string")

    if activity_name not in self.activities:
        raise ValueError(f"Activity '{activity_name}' not found")

    # ... rest of logic
```

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Anthropic Documentation](https://docs.anthropic.com)

## 💡 Best Practices

1. **Clear tool descriptions** - Help AI understand what tools do
2. **Validate inputs** - Always check arguments before processing
3. **Handle errors gracefully** - Return helpful error messages
4. **Document resources** - Explain what data resources provide
5. **Keep tools focused** - One tool = one clear purpose
6. **Use async** - For better performance
7. **Add logging** - Track usage and debug issues
8. **Implement health checks** - Monitor server status

## 🐛 Troubleshooting

### Server won't start

- Check port 5000 isn't already in use: `lsof -i :5000`
- Verify dependencies are installed: `pip install -r requirements.txt`
- Check for Python errors in the console

### Tools not working

- Verify tool registration in `_register_tools()`
- Check handler function exists and has correct signature
- Validate tool parameters match schema
- Review error messages in server logs

### Resource access fails

- Confirm resource URI is registered
- Check resource handler returns correct data type
- Verify resource handler is async

## 🎯 Use Cases

- **AI Assistants** - Give Claude access to your data
- **Automation** - Allow AI to perform actions
- **Data Access** - Provide structured data to AI
- **Integration** - Connect multiple systems
- **Development** - Build AI-powered applications

---

**Start building with MCP! 🚀**

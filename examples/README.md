# Examples: Anthropic SDK & MCP Server Integration

This directory contains comprehensive examples and implementations for integrating Anthropic's Claude AI and Model Context Protocol (MCP) servers with the School Activities application.

## 📁 Directory Structure

```
examples/
├── anthropic_sdk/          # Anthropic Python SDK examples
│   ├── 01_basic_usage.py
│   ├── 02_conversations.py
│   ├── 03_advanced_features.py
│   └── 04_fastapi_integration.py
├── mcp_server/             # MCP Server implementations
│   ├── simple_mcp_server.py
│   └── http_mcp_server.py
└── docker/                 # Docker configurations
    ├── Dockerfile.app
    ├── Dockerfile.mcp
    ├── docker-compose.yml
    └── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables

```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env

# Or export directly
export ANTHROPIC_API_KEY="your_api_key_here"
```

### 3. Run Examples

```bash
# Run basic Anthropic SDK examples
python examples/anthropic_sdk/01_basic_usage.py

# Run conversation examples
python examples/anthropic_sdk/02_conversations.py

# Run advanced features
python examples/anthropic_sdk/03_advanced_features.py

# Run MCP server
python examples/mcp_server/simple_mcp_server.py

# Run HTTP MCP server
python examples/mcp_server/http_mcp_server.py
```

## 📚 Anthropic SDK Examples

### 01_basic_usage.py

Learn the fundamentals of using the Anthropic Python SDK:

- Initializing the client
- Sending basic messages
- Using system prompts
- Customizing parameters (temperature, max_tokens)
- Viewing token usage

**Key Concepts:**
```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 02_conversations.py

Master multi-turn conversations with Claude:

- Maintaining conversation history
- Context-aware responses
- Building a conversation manager
- Interactive chat sessions
- Coding assistant workflows

**Key Features:**
- `ConversationManager` class for easy conversation handling
- Examples of contextual follow-up questions
- Interactive mode for real-time conversations

### 03_advanced_features.py

Explore advanced capabilities:

- **Streaming responses** - Get responses token by token
- **Tool use** - Enable Claude to call functions
- **Vision** - Analyze images with Claude
- **Error handling** - Robust error management
- **Async operations** - Non-blocking API calls

**Advanced Patterns:**
```python
# Streaming
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="")

# Tool use
tools = [{
    "name": "get_weather",
    "description": "Get weather for a location",
    "input_schema": {...}
}]

response = client.messages.create(
    model="claude-opus-4-1-20250805",
    tools=tools,
    messages=[...]
)
```

### 04_fastapi_integration.py

Complete FastAPI integration examples:

- Building AI-powered API endpoints
- Async request handling
- Streaming responses over HTTP
- Request/response models with Pydantic
- Error handling in web applications

**Example Endpoints:**
- `POST /api/chat` - Simple chat interface
- `POST /api/suggest-activities` - AI-powered suggestions
- `POST /api/chat-stream` - Streaming responses
- `POST /api/analyze-participation` - Data analysis

## 🔧 MCP Server Examples

### simple_mcp_server.py

A basic MCP server implementation demonstrating:

- **Tools** - Callable functions that AI can use
- **Resources** - Data sources AI can access
- **Async operations** - Non-blocking handlers

**Available Tools:**
- `get_activities` - List all activities
- `get_activity_details` - Get details for a specific activity
- `check_availability` - Check if activity has open spots

**Available Resources:**
- `activities://catalog` - Complete activities catalog
- `activities://stats` - Participation statistics

**Usage:**
```python
from simple_mcp_server import SchoolActivitiesMCPServer

server = SchoolActivitiesMCPServer()

# Call a tool
result = await server.call_tool("get_activities", {})

# Access a resource
data = await server.get_resource("activities://stats")
```

### http_mcp_server.py

Production-ready HTTP MCP server:

- RESTful API interface
- FastAPI-based implementation
- Health checks and monitoring
- Convenience endpoints for common operations

**HTTP Endpoints:**
- `GET /tools` - List available tools
- `GET /resources` - List available resources
- `POST /tools/call` - Execute a tool
- `POST /resources/get` - Fetch a resource
- `GET /api/activities` - Convenience API
- `GET /health` - Health check

**Start the server:**
```bash
python examples/mcp_server/http_mcp_server.py
```

Access at: http://localhost:5000

## 🐳 Docker Deployment

### Quick Start with Docker

```bash
cd examples/docker

# Create .env file with your API keys
cat > .env << EOF
ANTHROPIC_API_KEY=your_anthropic_key
GITHUB_TOKEN=ghp_your_github_token
EOF

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Services

**Main Application (Port 8000)**
- FastAPI app with AI features
- Activity management
- AI-powered suggestions and chat

**MCP Server (Port 5000)**
- Tools and resources for AI agents
- RESTful API interface

**GitHub MCP (Port 5001, Optional)**
- GitHub integration
- Requires GITHUB_TOKEN

See [docker/README.md](docker/README.md) for detailed Docker documentation.

## 🎯 Integration with Main Application

The main application (`src/app.py`) has been enhanced with AI capabilities:

### AI Endpoints

**Check AI Status**
```bash
curl http://localhost:8000/ai/status
```

**Get Activity Suggestions**
```bash
curl -X POST http://localhost:8000/ai/suggest-activities \
  -H "Content-Type: application/json" \
  -d '{
    "student_interests": ["programming", "problem solving"],
    "grade_level": 10
  }'
```

**Chat about Activities**
```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Which activities meet on Fridays?"
  }'
```

**Get Enhanced Activity Summary**
```bash
curl http://localhost:8000/ai/activity-summary/Chess%20Club
```

**Analyze Participation**
```bash
curl http://localhost:8000/ai/participation-insights
```

## 📖 Learning Path

### Beginner

1. Start with `01_basic_usage.py` - Learn SDK basics
2. Try `02_conversations.py` - Understand conversation handling
3. Run the main app with AI features
4. Test the AI endpoints with curl or Postman

### Intermediate

1. Study `03_advanced_features.py` - Explore advanced patterns
2. Understand `04_fastapi_integration.py` - Web integration
3. Examine the enhanced `src/app.py` - Real-world usage
4. Run `simple_mcp_server.py` - Learn MCP concepts

### Advanced

1. Study `http_mcp_server.py` - Production MCP server
2. Deploy with Docker - Containerized deployment
3. Extend the MCP server with custom tools
4. Integrate multiple MCP servers
5. Build your own AI-powered endpoints

## 🔑 API Keys

### Anthropic API Key

Get your API key from: https://console.anthropic.com/

**Set the environment variable:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Or use .env file:**
```bash
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

### GitHub Token (Optional)

For GitHub MCP server integration:

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate a new token with appropriate permissions
3. Set the environment variable:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

## 🛠️ Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_app_baseline.py
```

### Adding New Examples

1. Create a new Python file in the appropriate directory
2. Follow the existing naming convention
3. Include comprehensive docstrings
4. Add error handling
5. Update this README with the new example

### Extending MCP Server

To add a new tool to the MCP server:

```python
# In simple_mcp_server.py or http_mcp_server.py

# Register the tool
self.register_tool(
    name="your_tool_name",
    description="What your tool does",
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Param description"}
        },
        "required": ["param1"]
    },
    handler=self._handle_your_tool
)

# Implement the handler
async def _handle_your_tool(self, args: Dict) -> Any:
    param1 = args.get("param1")
    # Your tool logic here
    return result
```

## 📝 Best Practices

### API Usage

1. **Always handle errors gracefully**
   ```python
   try:
       response = client.messages.create(...)
   except APIError as e:
       print(f"API Error: {e}")
   ```

2. **Use appropriate models**
   - `claude-opus-4-1-20250805` - Most capable, slower
   - `claude-sonnet-4-5-20250929` - Balanced performance
   - `claude-haiku-4-0-20250305` - Fastest, most efficient

3. **Manage token usage**
   - Monitor `input_tokens` and `output_tokens`
   - Set reasonable `max_tokens` limits
   - Use streaming for long responses

4. **Implement rate limiting**
   - Respect API rate limits
   - Implement exponential backoff
   - Cache responses when appropriate

### Security

1. **Never commit API keys** - Use environment variables
2. **Validate user input** - Sanitize before sending to AI
3. **Implement authentication** - For production endpoints
4. **Rate limit endpoints** - Prevent abuse
5. **Monitor usage** - Track API costs

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set"

**Solution:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### "Module 'anthropic' not found"

**Solution:**
```bash
pip install anthropic
```

### MCP Server won't start

**Common issues:**
- Port already in use: Change port in the code
- Missing dependencies: Run `pip install -r requirements.txt`
- Import errors: Ensure you're in the correct directory

### Docker issues

See [docker/README.md](docker/README.md) troubleshooting section.

## 📚 Additional Resources

- **Anthropic Documentation**: https://docs.anthropic.com
- **Claude API Reference**: https://docs.anthropic.com/en/api
- **MCP Documentation**: https://modelcontextprotocol.io
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Python SDK GitHub**: https://github.com/anthropics/anthropic-sdk-python

## 🤝 Contributing

To contribute examples or improvements:

1. Fork the repository
2. Create a feature branch
3. Add your examples with documentation
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 💡 Need Help?

- Check the example code comments
- Review the Anthropic documentation
- Test with simple examples first
- Use the interactive conversation mode in `02_conversations.py`
- Check Docker logs if using containers

---

**Happy coding with Claude! 🤖**

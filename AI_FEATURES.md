# AI Features & MCP Integration

This repository has been enhanced with comprehensive AI capabilities using Anthropic's Claude and Model Context Protocol (MCP) servers.

## 📋 What's New

### ✨ AI-Powered Features in Main Application

The FastAPI application (`src/app.py`) now includes AI endpoints:

- **Activity Suggestions** - Get personalized activity recommendations based on student interests
- **AI Chat** - Ask questions about activities and get intelligent responses
- **Enhanced Descriptions** - Generate compelling activity summaries
- **Participation Analysis** - Get AI-powered insights on participation patterns

### 🎓 Comprehensive Examples

Complete examples demonstrating Anthropic SDK usage and MCP server implementation:

- **Anthropic SDK Examples** - Basic to advanced usage patterns
- **MCP Server** - Custom server for activities data
- **Docker Deployment** - Production-ready containerization
- **FastAPI Integration** - Real-world web application patterns

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Key

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. Run the Enhanced Application

```bash
cd src
python app.py
```

The application will be available at http://localhost:8000

### 4. Test AI Features

```bash
# Check AI status
curl http://localhost:8000/ai/status

# Get activity suggestions
curl -X POST http://localhost:8000/ai/suggest-activities \
  -H "Content-Type: application/json" \
  -d '{
    "student_interests": ["programming", "problem solving"],
    "grade_level": 10
  }'

# Chat about activities
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What activities meet on Fridays?"}'
```

## 📚 Documentation

### Examples Directory Structure

```
examples/
├── README.md                          # Main examples documentation
├── anthropic_sdk/                     # Anthropic SDK examples
│   ├── README.md                      # SDK examples guide
│   ├── 01_basic_usage.py             # Basic SDK usage
│   ├── 02_conversations.py           # Multi-turn conversations
│   ├── 03_advanced_features.py       # Streaming, tools, vision
│   └── 04_fastapi_integration.py     # FastAPI integration
├── mcp_server/                        # MCP server examples
│   ├── README.md                      # MCP server guide
│   ├── simple_mcp_server.py          # Basic MCP implementation
│   └── http_mcp_server.py            # HTTP MCP server
├── docker/                            # Docker configurations
│   ├── README.md                      # Docker deployment guide
│   ├── Dockerfile.app                 # Main app Dockerfile
│   ├── Dockerfile.mcp                 # MCP server Dockerfile
│   └── docker-compose.yml             # Complete setup
└── mcp_config_example.json            # MCP configuration example
```

### Key Documentation

- **[Examples Overview](examples/README.md)** - Complete guide to all examples
- **[Anthropic SDK Guide](examples/anthropic_sdk/README.md)** - SDK usage and patterns
- **[MCP Server Guide](examples/mcp_server/README.md)** - MCP implementation details
- **[Docker Guide](examples/docker/README.md)** - Deployment with Docker

## 🎯 AI Endpoints

### GET /ai/status

Check if AI features are enabled.

**Response:**
```json
{
  "ai_enabled": true,
  "message": "AI features are enabled"
}
```

### POST /ai/suggest-activities

Get AI-powered activity suggestions based on student profile.

**Request:**
```json
{
  "student_interests": ["coding", "logic games"],
  "grade_level": 10
}
```

**Response:**
```json
{
  "suggestions": "Based on your interests in coding and logic games, here are the top 3 activities...",
  "student_interests": ["coding", "logic games"],
  "grade_level": 10
}
```

### POST /ai/chat

Chat with AI about activities and get contextual responses.

**Request:**
```json
{
  "message": "Which activities are available on Tuesdays?"
}
```

**Response:**
```json
{
  "response": "The following activities meet on Tuesdays: Programming Class (Tuesdays and Thursdays, 3:30 PM - 4:30 PM)...",
  "message": "Which activities are available on Tuesdays?"
}
```

### GET /ai/activity-summary/{activity_name}

Generate an enhanced, AI-powered description for an activity.

**Response:**
```json
{
  "activity_name": "Chess Club",
  "original_description": "Learn strategies and compete in chess tournaments",
  "ai_enhanced_summary": "Join Chess Club and unlock your strategic thinking potential! Master classical openings, develop tactical skills..."
}
```

### GET /ai/participation-insights

Get AI analysis of participation patterns across all activities.

**Response:**
```json
{
  "participation_data": [...],
  "ai_insights": "Key observations: 1. Programming Class and Chess Club show strong early adoption..."
}
```

## 🔧 Running Examples

### Anthropic SDK Examples

```bash
# Navigate to examples
cd examples/anthropic_sdk

# Set API key
export ANTHROPIC_API_KEY="your-key"

# Run examples
python 01_basic_usage.py        # Basic usage patterns
python 02_conversations.py      # Conversation management
python 03_advanced_features.py  # Advanced features
python 04_fastapi_integration.py # Web integration
```

### MCP Server

```bash
# Navigate to MCP examples
cd examples/mcp_server

# Run simple example
python simple_mcp_server.py

# Run HTTP server
python http_mcp_server.py

# Server will be at http://localhost:5000
```

### Docker Deployment

```bash
# Navigate to docker directory
cd examples/docker

# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your_key_here
GITHUB_TOKEN=ghp_your_token_here
EOF

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🌐 MCP Server

The Model Context Protocol server provides structured access to activities data for AI assistants.

### Starting the MCP Server

```bash
python examples/mcp_server/http_mcp_server.py
```

Server will be available at http://localhost:5000

### Available Tools

- `get_activities` - List all activities
- `get_activity_details` - Get detailed information about an activity
- `check_availability` - Check if an activity has available spots

### Available Resources

- `activities://catalog` - Complete activities catalog
- `activities://stats` - Participation statistics

### Testing MCP Server

```bash
# List tools
curl http://localhost:5000/tools

# Call a tool
curl -X POST http://localhost:5000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_activity_details",
    "arguments": {"activity_name": "Chess Club"}
  }'

# Get a resource
curl -X POST http://localhost:5000/resources/get \
  -H "Content-Type: application/json" \
  -d '{"uri": "activities://stats"}'
```

## 🐳 Docker Deployment

### Services

The Docker setup includes:

1. **Main Application** (Port 8000) - FastAPI app with AI features
2. **MCP Server** (Port 5000) - Activities data server
3. **GitHub MCP** (Port 5001, Optional) - GitHub integration

### Quick Start

```bash
cd examples/docker
docker-compose up -d
```

### Access Services

- Main App: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MCP Server: http://localhost:5000
- MCP Docs: http://localhost:5000/docs

## 🔑 Configuration

### Environment Variables

```bash
# Required for AI features
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Optional for GitHub integration
export GITHUB_TOKEN="ghp_your-github-token"
```

### MCP Configuration

See `examples/mcp_config_example.json` for Claude MCP configuration.

## 📊 Features Comparison

| Feature | Without AI | With AI |
|---------|-----------|---------|
| Activity Discovery | Manual browsing | Personalized suggestions |
| Questions | Check documentation | Ask natural language questions |
| Descriptions | Static text | Generated, engaging summaries |
| Insights | Manual analysis | AI-powered analytics |
| Integration | REST API only | REST API + MCP + AI |

## 🎓 Learning Resources

### For Beginners

1. Start with [examples/anthropic_sdk/01_basic_usage.py](examples/anthropic_sdk/01_basic_usage.py)
2. Try the conversation examples in [02_conversations.py](examples/anthropic_sdk/02_conversations.py)
3. Test the AI endpoints in the main application
4. Explore the [Examples README](examples/README.md)

### For Advanced Users

1. Study [advanced features](examples/anthropic_sdk/03_advanced_features.py)
2. Build custom [MCP servers](examples/mcp_server/)
3. Deploy with [Docker](examples/docker/)
4. Integrate AI into your own applications

## 🔧 Development

### Adding Custom AI Endpoints

1. Add endpoint to `src/app.py`:

```python
@app.post("/ai/my-custom-endpoint")
def my_custom_ai_feature(request: MyRequest):
    if not AI_ENABLED:
        raise HTTPException(status_code=503, detail="AI not enabled")

    response = anthropic_client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=500,
        messages=[{"role": "user", "content": request.message}]
    )

    return {"result": response.content[0].text}
```

### Extending MCP Server

Add tools to `examples/mcp_server/simple_mcp_server.py`:

```python
self.register_tool(
    name="my_tool",
    description="Tool description",
    parameters={...},
    handler=self._handle_my_tool
)
```

## 🐛 Troubleshooting

### AI Features Not Working

1. Verify `ANTHROPIC_API_KEY` is set
2. Check `/ai/status` endpoint
3. Ensure `anthropic` package is installed
4. Review application logs

### MCP Server Issues

1. Check port 5000 is available
2. Verify dependencies installed
3. Review server logs
4. Test with curl commands

### Docker Problems

1. Ensure Docker is running
2. Check `.env` file exists
3. Review logs: `docker-compose logs`
4. Rebuild: `docker-compose build --no-cache`

## 📚 External Resources

- [Anthropic Documentation](https://docs.anthropic.com)
- [Claude API Reference](https://docs.anthropic.com/en/api)
- [MCP Protocol](https://modelcontextprotocol.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Docker Documentation](https://docs.docker.com)

## 🤝 Contributing

To contribute:

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🎉 What's Next?

- Explore all examples in `examples/`
- Try the AI-powered endpoints
- Build custom tools for MCP server
- Deploy with Docker
- Integrate AI into your projects

---

**Ready to build with AI? Start with the [Examples README](examples/README.md)!** 🚀

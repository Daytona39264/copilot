# Testing Guide for AI Features

This guide provides step-by-step instructions for testing all AI features and examples.

## 🚀 Quick Test

Run the comprehensive test suite:

```bash
python test_all.py
```

This will validate:
- ✅ File structure
- ✅ Python syntax
- ✅ Module imports
- ✅ MCP server functionality
- ✅ Pytest test suite
- ✅ Docker configuration

## 📋 Manual Testing Steps

### 1. Test Anthropic SDK Examples

#### Set up environment (if you have an API key):

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

#### Run examples:

```bash
# Example 1: Basic usage
cd examples/anthropic_sdk
python 01_basic_usage.py

# Example 2: Conversations
python 02_conversations.py

# Example 3: Advanced features
python 03_advanced_features.py

# Example 4: FastAPI integration
python 04_fastapi_integration.py &
# Test the endpoints at http://localhost:8000/docs
```

**Without API Key:**
The examples will show informative error messages about setting the API key.

### 2. Test AI Endpoints in Main Application

#### Start the application:

```bash
cd src
python app.py
```

The application will start on http://localhost:8000

#### Test AI status:

```bash
curl http://localhost:8000/ai/status
```

**Expected response:**
```json
{
  "ai_enabled": false,
  "message": "Set ANTHROPIC_API_KEY to enable AI features"
}
```

#### Test with API key (if available):

```bash
export ANTHROPIC_API_KEY="your-key"
cd src
python app.py
```

Then test the endpoints:

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

# Get enhanced activity summary
curl http://localhost:8000/ai/activity-summary/Chess%20Club

# Get participation insights
curl http://localhost:8000/ai/participation-insights
```

#### Test with interactive API docs:

Open http://localhost:8000/docs in your browser and try the endpoints interactively.

### 3. Test MCP Server

#### Start the MCP server:

```bash
cd examples/mcp_server
python http_mcp_server.py
```

Server will be available at http://localhost:5000

#### Test MCP endpoints:

```bash
# Check health
curl http://localhost:5000/health

# Check server info
curl http://localhost:5000/

# List available tools
curl http://localhost:5000/tools

# List available resources
curl http://localhost:5000/resources

# Call get_activities tool
curl -X POST http://localhost:5000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_activities",
    "arguments": {}
  }'

# Get activity details
curl -X POST http://localhost:5000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_activity_details",
    "arguments": {"activity_name": "Chess Club"}
  }'

# Check availability
curl -X POST http://localhost:5000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "check_availability",
    "arguments": {"activity_name": "Programming Class"}
  }'

# Get resource
curl -X POST http://localhost:5000/resources/get \
  -H "Content-Type: application/json" \
  -d '{"uri": "activities://stats"}'

# Convenience API endpoints
curl http://localhost:5000/api/activities
curl http://localhost:5000/api/activities/Chess%20Club
curl http://localhost:5000/api/activities/Chess%20Club/availability
curl http://localhost:5000/api/stats
```

#### Test with interactive docs:

Open http://localhost:5000/docs in your browser.

### 4. Test Docker Deployment

#### Prerequisites:

- Docker installed and running
- Docker Compose installed

#### Create environment file:

```bash
cd examples/docker

cat > .env << EOF
ANTHROPIC_API_KEY=your_api_key_here
GITHUB_TOKEN=ghp_your_github_token_here
EOF
```

#### Validate Docker configuration:

```bash
# Validate docker-compose configuration
docker-compose config

# Check for syntax errors
docker-compose config --quiet && echo "Configuration is valid"
```

#### Build images:

```bash
# Build all images
docker-compose build

# Or build individually
docker-compose build app
docker-compose build mcp-server
```

#### Start services:

```bash
# Start main app and MCP server
docker-compose up -d

# Or include GitHub MCP server
docker-compose --profile with-github up -d
```

#### Verify services are running:

```bash
# Check status
docker-compose ps

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Check specific service
docker-compose logs app
docker-compose logs mcp-server
```

#### Test services:

```bash
# Test main application
curl http://localhost:8000/activities
curl http://localhost:8000/ai/status

# Test MCP server
curl http://localhost:5000/health
curl http://localhost:5000/tools

# Test GitHub MCP (if enabled)
curl http://localhost:5001/health
```

#### Stop services:

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🧪 Running Automated Tests

### Run all tests:

```bash
python test_all.py
```

### Run specific test suites:

```bash
# Run AI features tests
python -m pytest tests/test_ai_features.py -v

# Run MCP server tests
python -m pytest tests/test_mcp_server.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov=examples/mcp_server --cov-report=html

# Run specific test
python -m pytest tests/test_ai_features.py::TestAIEndpoints::test_ai_status_endpoint -v
```

### Test output locations:

- Coverage report: `htmlcov/index.html`
- Test results: Terminal output

## 📊 Expected Results

### Without ANTHROPIC_API_KEY:

- ✅ All syntax validation passes
- ✅ File structure is correct
- ✅ MCP server works fully
- ✅ Main app works (AI endpoints return 503)
- ✅ Docker configuration is valid

### With ANTHROPIC_API_KEY:

- ✅ All of the above
- ✅ AI endpoints return actual responses
- ✅ Activity suggestions work
- ✅ AI chat responds
- ✅ Enhanced summaries generated
- ✅ Participation insights provided

## 🔍 Troubleshooting

### Tests fail due to import errors

```bash
# Install missing dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(fastapi|uvicorn|anthropic|pytest)"
```

### Port already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
PORT=8001 python src/app.py
```

### Docker tests fail

```bash
# Check Docker is running
docker ps

# Check Docker Compose version
docker-compose --version

# Rebuild without cache
cd examples/docker
docker-compose build --no-cache
```

### MCP server tests fail

```bash
# Ensure you're in the project root
cd /home/user/copilot

# Run with verbose output
python -m pytest tests/test_mcp_server.py -v -s

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

## 📈 Performance Testing

### Load testing MCP server:

```bash
# Install Apache Bench
apt-get install apache2-utils

# Test MCP server
ab -n 100 -c 10 http://localhost:5000/health

# Test tool call endpoint
ab -n 50 -c 5 -p post_data.json -T application/json \
   http://localhost:5000/api/activities
```

### Measure response times:

```bash
# Test AI endpoint response time
time curl http://localhost:8000/ai/status

# Test MCP server response time
time curl http://localhost:5000/tools
```

## 📝 Test Checklist

Use this checklist to verify all components:

- [ ] All Python files have valid syntax
- [ ] All required files exist
- [ ] All dependencies are installed
- [ ] MCP server starts successfully
- [ ] MCP server tools work correctly
- [ ] MCP server resources are accessible
- [ ] Main application starts successfully
- [ ] AI status endpoint responds
- [ ] AI endpoints gracefully handle missing API key
- [ ] Docker configuration is valid
- [ ] docker-compose builds successfully
- [ ] All services start in Docker
- [ ] Services are accessible via Docker ports
- [ ] Automated tests pass
- [ ] Documentation is complete

## 🎯 Next Steps After Testing

Once all tests pass:

1. **Set your API key** (if you have one):
   ```bash
   export ANTHROPIC_API_KEY="your-key"
   ```

2. **Start developing**:
   - Modify examples in `examples/anthropic_sdk/`
   - Add custom tools to MCP server
   - Create new AI endpoints in `src/app.py`

3. **Deploy to production**:
   - Use Docker Compose for deployment
   - Set up environment variables securely
   - Configure reverse proxy (nginx)
   - Enable HTTPS

4. **Monitor and optimize**:
   - Track API usage
   - Monitor response times
   - Optimize prompts
   - Cache frequent responses

## 📚 Additional Resources

- [AI_FEATURES.md](AI_FEATURES.md) - Overview of AI features
- [examples/README.md](examples/README.md) - Examples documentation
- [examples/docker/README.md](examples/docker/README.md) - Docker deployment guide
- [examples/mcp_server/README.md](examples/mcp_server/README.md) - MCP server guide

---

**Happy testing! 🧪**

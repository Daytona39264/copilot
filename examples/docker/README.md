# Docker Configuration for School Activities Application

This directory contains Docker configurations for running the School Activities application with AI features and MCP servers.

## Overview

The Docker setup includes:

1. **Main Application** - FastAPI app with AI-powered features
2. **MCP Server** - Model Context Protocol server for activities data
3. **GitHub MCP Server** (optional) - Integration with GitHub

## Prerequisites

- Docker installed and running
- Docker Compose installed
- Anthropic API key (for AI features)
- GitHub Personal Access Token (optional, for GitHub integration)

## Quick Start

### 1. Set up environment variables

Create a `.env` file in this directory:

```bash
# Required for AI features
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional - for GitHub MCP integration
GITHUB_TOKEN=ghp_your_github_token_here
```

### 2. Start all services

```bash
# Start main app and MCP server
docker-compose up -d

# Or, to include GitHub MCP server:
docker-compose --profile with-github up -d
```

### 3. Verify services are running

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Test the main application
curl http://localhost:8000/activities

# Test the MCP server
curl http://localhost:5000/health

# Test AI features (if ANTHROPIC_API_KEY is set)
curl http://localhost:8000/ai/status
```

## Services

### Main Application (Port 8000)

The FastAPI application with AI-powered features.

**Key Endpoints:**
- `GET /activities` - List all activities
- `POST /activities/{name}/signup` - Sign up for an activity
- `GET /ai/status` - Check if AI features are enabled
- `POST /ai/suggest-activities` - Get AI-powered activity suggestions
- `POST /ai/chat` - Chat with AI about activities
- `GET /ai/participation-insights` - Get AI analysis of participation

**Access:**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs

### MCP Server (Port 5000)

Model Context Protocol server providing structured access to activities data.

**Key Endpoints:**
- `GET /tools` - List available tools
- `GET /resources` - List available resources
- `POST /tools/call` - Call a tool
- `GET /api/activities` - Get all activities

**Access:**
- API: http://localhost:5000
- Health: http://localhost:5000/health

### GitHub MCP Server (Port 5001, Optional)

Provides GitHub integration capabilities.

**Requirements:**
- GitHub Personal Access Token with appropriate permissions
- Enable with `--profile with-github` flag

**Access:**
- API: http://localhost:5001

## Individual Service Management

### Build images

```bash
# Build all images
docker-compose build

# Build specific service
docker-compose build app
docker-compose build mcp-server
```

### Start/Stop services

```bash
# Start specific service
docker-compose up -d app

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### View logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f mcp-server
```

### Execute commands in containers

```bash
# Access app container
docker-compose exec app /bin/bash

# Run tests
docker-compose exec app pytest

# Check Python version
docker-compose exec app python --version
```

## Using Individual Dockerfiles

You can also build and run containers individually:

### Main Application

```bash
# Build
docker build -f Dockerfile.app -t school-activities-app ../..

# Run
docker run -d \
  --name school-app \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key_here \
  school-activities-app
```

### MCP Server

```bash
# Build
docker build -f Dockerfile.mcp -t school-activities-mcp ../..

# Run
docker run -d \
  --name school-mcp \
  -p 5000:5000 \
  school-activities-mcp
```

### GitHub MCP Server

```bash
# Pull and run
docker run -d \
  --name github-mcp \
  --restart unless-stopped \
  -p 5001:5000 \
  -e GITHUB_TOKEN=ghp_your_token_here \
  ghcr.io/klavis-ai/github-mcp-server:latest
```

## Troubleshooting

### Services won't start

```bash
# Check logs
docker-compose logs

# Ensure ports are not in use
lsof -i :8000
lsof -i :5000
lsof -i :5001

# Rebuild without cache
docker-compose build --no-cache
```

### AI features not working

1. Verify ANTHROPIC_API_KEY is set in `.env`
2. Check the key is valid
3. Restart the service: `docker-compose restart app`
4. Check logs: `docker-compose logs app`

### GitHub MCP not working

1. Verify GITHUB_TOKEN is set in `.env`
2. Check token has correct permissions
3. Ensure you used the `--profile with-github` flag
4. Check logs: `docker-compose logs github-mcp`

### Permission denied errors

```bash
# Fix permissions on Linux/Mac
sudo chown -R $USER:$USER .

# Or run Docker commands with sudo
sudo docker-compose up -d
```

## Health Checks

All services include health checks:

```bash
# Check health status
docker-compose ps

# Manual health checks
curl http://localhost:8000/activities  # Main app
curl http://localhost:5000/health      # MCP server
curl http://localhost:5001/health      # GitHub MCP (if enabled)
```

## Production Deployment

For production deployment, consider:

1. **Use secrets management** - Don't commit `.env` file
2. **Add reverse proxy** - Use Nginx or Traefik
3. **Enable HTTPS** - Use Let's Encrypt certificates
4. **Add monitoring** - Prometheus, Grafana
5. **Set resource limits** - Configure memory/CPU limits
6. **Use volume mounts** - For persistent data
7. **Enable logging** - Centralized logging solution

Example with resource limits:

```yaml
services:
  app:
    # ... other config ...
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Useful Commands

```bash
# Restart all services
docker-compose restart

# Pull latest images
docker-compose pull

# Remove stopped containers
docker-compose rm

# Show resource usage
docker stats

# Clean up unused images
docker image prune -a

# View container details
docker inspect <container_id>
```

## Integration with Claude

To use these services with Claude:

1. **Direct API calls** - Use the HTTP endpoints from your Claude application
2. **MCP Integration** - Configure Claude to use the MCP server at http://localhost:5000
3. **Tool use** - Claude can call the exposed tools through the MCP protocol

Example MCP configuration for Claude:

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

## Next Steps

- Explore the API documentation at http://localhost:8000/docs
- Try the AI features with your Anthropic API key
- Customize the MCP server tools for your needs
- Set up GitHub integration for enhanced capabilities

## Support

For issues or questions:
- Check container logs: `docker-compose logs`
- Review Docker documentation: https://docs.docker.com
- Check FastAPI documentation: https://fastapi.tiangolo.com
- Anthropic API docs: https://docs.anthropic.com

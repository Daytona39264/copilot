"""
HTTP-based MCP Server

This implementation provides an HTTP interface for the MCP server,
allowing it to be accessed by Claude and other AI assistants over the network.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import uvicorn
from simple_mcp_server import SchoolActivitiesMCPServer


# Request/Response Models
class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = {}


class ResourceRequest(BaseModel):
    uri: str


class MCPResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


# Create FastAPI app
app = FastAPI(
    title="School Activities MCP Server",
    description="MCP server providing access to school activities data and operations",
    version="1.0.0"
)

# Initialize MCP server
mcp_server = SchoolActivitiesMCPServer()


@app.get("/")
def root():
    """Root endpoint with server info"""
    return {
        "name": mcp_server.name,
        "version": mcp_server.version,
        "status": "running",
        "endpoints": {
            "tools": "/tools",
            "resources": "/resources",
            "call_tool": "/tools/call",
            "get_resource": "/resources/get"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/tools")
def list_tools():
    """List all available tools"""
    return {
        "tools": mcp_server.list_tools()
    }


@app.get("/resources")
def list_resources():
    """List all available resources"""
    return {
        "resources": mcp_server.list_resources()
    }


@app.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    """
    Call a tool with the specified arguments

    Example request:
    {
        "tool_name": "get_activities",
        "arguments": {}
    }
    """
    result = await mcp_server.call_tool(request.tool_name, request.arguments)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "success": True,
        "tool": request.tool_name,
        "result": result["result"]
    }


@app.post("/resources/get")
async def get_resource(request: ResourceRequest):
    """
    Get a resource by URI

    Example request:
    {
        "uri": "activities://catalog"
    }
    """
    result = await mcp_server.get_resource(request.uri)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return {
        "success": True,
        "uri": request.uri,
        "content": result["content"]
    }


# Convenience endpoints for common operations
@app.get("/api/activities")
async def get_activities():
    """Get list of all activities"""
    result = await mcp_server.call_tool("get_activities", {})
    return result["result"]


@app.get("/api/activities/{activity_name}")
async def get_activity_details(activity_name: str):
    """Get details for a specific activity"""
    result = await mcp_server.call_tool("get_activity_details", {"activity_name": activity_name})

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result["result"]


@app.get("/api/activities/{activity_name}/availability")
async def check_activity_availability(activity_name: str):
    """Check availability for a specific activity"""
    result = await mcp_server.call_tool("check_availability", {"activity_name": activity_name})

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result["result"]


@app.get("/api/stats")
async def get_participation_stats():
    """Get participation statistics"""
    result = await mcp_server.get_resource("activities://stats")
    return result["content"]


if __name__ == "__main__":
    print("Starting School Activities MCP Server...")
    print("Server will be available at http://localhost:5000")
    print("\nEndpoints:")
    print("  - GET  /          - Server info")
    print("  - GET  /health    - Health check")
    print("  - GET  /tools     - List available tools")
    print("  - GET  /resources - List available resources")
    print("  - POST /tools/call - Call a tool")
    print("  - POST /resources/get - Get a resource")
    print("\nConvenience API:")
    print("  - GET  /api/activities - List all activities")
    print("  - GET  /api/activities/{name} - Get activity details")
    print("  - GET  /api/activities/{name}/availability - Check availability")
    print("  - GET  /api/stats - Get participation stats")

    uvicorn.run(app, host="0.0.0.0", port=5000)

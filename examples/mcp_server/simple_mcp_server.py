"""
Simple MCP (Model Context Protocol) Server Implementation

This is a basic implementation of an MCP server that can be used
to provide tools and context to Claude AI applications.

MCP allows AI assistants to access external data and functionality
in a standardized way.
"""

from typing import Any, Dict, List
import json
import asyncio
from datetime import datetime


class MCPServer:
    """
    Simple MCP Server implementation

    MCP servers expose tools and resources that AI models can use.
    """

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools = {}
        self.resources = {}

    def register_tool(self, name: str, description: str, parameters: Dict, handler):
        """Register a tool that can be called by the AI"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "handler": handler
        }

    def register_resource(self, uri: str, name: str, description: str, handler):
        """Register a resource that can be accessed by the AI"""
        self.resources[uri] = {
            "uri": uri,
            "name": name,
            "description": description,
            "handler": handler
        }

    async def call_tool(self, tool_name: str, arguments: Dict) -> Dict[str, Any]:
        """Execute a tool with the given arguments"""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}

        tool = self.tools[tool_name]
        try:
            result = await tool["handler"](arguments)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

    async def get_resource(self, uri: str) -> Dict[str, Any]:
        """Retrieve a resource by URI"""
        if uri not in self.resources:
            return {"error": f"Resource '{uri}' not found"}

        resource = self.resources[uri]
        try:
            content = await resource["handler"]()
            return {"content": content}
        except Exception as e:
            return {"error": str(e)}

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
            for tool in self.tools.values()
        ]

    def list_resources(self) -> List[Dict[str, Any]]:
        """List all available resources"""
        return [
            {
                "uri": resource["uri"],
                "name": resource["name"],
                "description": resource["description"]
            }
            for resource in self.resources.values()
        ]


# Example: School Activities MCP Server
class SchoolActivitiesMCPServer(MCPServer):
    """
    MCP Server for the school activities application
    """

    def __init__(self):
        super().__init__("school-activities-mcp", "1.0.0")

        # In-memory activities database (same as main app)
        self.activities = {
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
            }
        }

        # Register tools
        self._register_tools()

        # Register resources
        self._register_resources()

    def _register_tools(self):
        """Register all available tools"""

        # Tool: Get activities list
        self.register_tool(
            name="get_activities",
            description="Get a list of all available extracurricular activities",
            parameters={
                "type": "object",
                "properties": {}
            },
            handler=self._handle_get_activities
        )

        # Tool: Get activity details
        self.register_tool(
            name="get_activity_details",
            description="Get detailed information about a specific activity",
            parameters={
                "type": "object",
                "properties": {
                    "activity_name": {
                        "type": "string",
                        "description": "Name of the activity"
                    }
                },
                "required": ["activity_name"]
            },
            handler=self._handle_get_activity_details
        )

        # Tool: Check availability
        self.register_tool(
            name="check_availability",
            description="Check if an activity has available spots",
            parameters={
                "type": "object",
                "properties": {
                    "activity_name": {
                        "type": "string",
                        "description": "Name of the activity"
                    }
                },
                "required": ["activity_name"]
            },
            handler=self._handle_check_availability
        )

    def _register_resources(self):
        """Register all available resources"""

        # Resource: Activities catalog
        self.register_resource(
            uri="activities://catalog",
            name="Activities Catalog",
            description="Complete catalog of extracurricular activities",
            handler=self._resource_activities_catalog
        )

        # Resource: Participation statistics
        self.register_resource(
            uri="activities://stats",
            name="Participation Statistics",
            description="Statistics about activity participation",
            handler=self._resource_participation_stats
        )

    # Tool Handlers
    async def _handle_get_activities(self, args: Dict) -> List[str]:
        """Handler for get_activities tool"""
        return list(self.activities.keys())

    async def _handle_get_activity_details(self, args: Dict) -> Dict:
        """Handler for get_activity_details tool"""
        activity_name = args.get("activity_name")

        if activity_name not in self.activities:
            raise ValueError(f"Activity '{activity_name}' not found")

        activity = self.activities[activity_name]
        return {
            "name": activity_name,
            "description": activity["description"],
            "schedule": activity["schedule"],
            "participants": len(activity["participants"]),
            "max_participants": activity["max_participants"],
            "available_spots": activity["max_participants"] - len(activity["participants"])
        }

    async def _handle_check_availability(self, args: Dict) -> Dict:
        """Handler for check_availability tool"""
        activity_name = args.get("activity_name")

        if activity_name not in self.activities:
            raise ValueError(f"Activity '{activity_name}' not found")

        activity = self.activities[activity_name]
        available_spots = activity["max_participants"] - len(activity["participants"])

        return {
            "activity": activity_name,
            "has_availability": available_spots > 0,
            "available_spots": available_spots,
            "total_capacity": activity["max_participants"]
        }

    # Resource Handlers
    async def _resource_activities_catalog(self) -> str:
        """Handler for activities catalog resource"""
        catalog = []
        for name, details in self.activities.items():
            catalog.append(f"{name}:\n{details['description']}\nSchedule: {details['schedule']}\n")

        return "\n".join(catalog)

    async def _resource_participation_stats(self) -> Dict:
        """Handler for participation statistics resource"""
        total_capacity = sum(a["max_participants"] for a in self.activities.values())
        total_participants = sum(len(a["participants"]) for a in self.activities.values())

        return {
            "timestamp": datetime.now().isoformat(),
            "total_activities": len(self.activities),
            "total_capacity": total_capacity,
            "total_participants": total_participants,
            "overall_fill_rate": f"{(total_participants / total_capacity * 100):.1f}%"
        }


# Example usage
async def main():
    """Example of using the MCP server"""

    # Create and start the MCP server
    server = SchoolActivitiesMCPServer()

    print("=== MCP Server Started ===\n")
    print(f"Server: {server.name} v{server.version}\n")

    # List available tools
    print("Available Tools:")
    for tool in server.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    print()

    # List available resources
    print("Available Resources:")
    for resource in server.list_resources():
        print(f"  - {resource['uri']}: {resource['name']}")
    print()

    # Example: Call a tool
    print("=== Example: Calling 'get_activities' tool ===")
    result = await server.call_tool("get_activities", {})
    print(f"Result: {json.dumps(result, indent=2)}\n")

    # Example: Get activity details
    print("=== Example: Getting activity details ===")
    result = await server.call_tool("get_activity_details", {"activity_name": "Chess Club"})
    print(f"Result: {json.dumps(result, indent=2)}\n")

    # Example: Check availability
    print("=== Example: Checking availability ===")
    result = await server.call_tool("check_availability", {"activity_name": "Programming Class"})
    print(f"Result: {json.dumps(result, indent=2)}\n")

    # Example: Access a resource
    print("=== Example: Accessing participation stats resource ===")
    result = await server.get_resource("activities://stats")
    print(f"Result: {json.dumps(result, indent=2)}\n")


if __name__ == "__main__":
    asyncio.run(main())

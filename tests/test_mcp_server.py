"""
Tests for MCP Server implementations

These tests verify the MCP server tools and resources work correctly.
"""

import pytest
import asyncio
import sys
import os

# Add examples to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples', 'mcp_server'))

from simple_mcp_server import SchoolActivitiesMCPServer


class TestMCPServer:
    """Test MCP Server functionality"""

    @pytest.fixture
    def server(self):
        """Create a test MCP server instance"""
        return SchoolActivitiesMCPServer()

    def test_server_initialization(self, server):
        """Test server initializes correctly"""
        assert server.name == "school-activities-mcp"
        assert server.version == "1.0.0"
        assert len(server.tools) > 0
        assert len(server.resources) > 0

    def test_list_tools(self, server):
        """Test listing available tools"""
        tools = server.list_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0

        tool_names = [tool["name"] for tool in tools]
        assert "get_activities" in tool_names
        assert "get_activity_details" in tool_names
        assert "check_availability" in tool_names

    def test_list_resources(self, server):
        """Test listing available resources"""
        resources = server.list_resources()
        assert isinstance(resources, list)
        assert len(resources) > 0

        resource_uris = [res["uri"] for res in resources]
        assert "activities://catalog" in resource_uris
        assert "activities://stats" in resource_uris

    @pytest.mark.asyncio
    async def test_get_activities_tool(self, server):
        """Test get_activities tool"""
        result = await server.call_tool("get_activities", {})

        assert "result" in result
        assert isinstance(result["result"], list)
        assert "Chess Club" in result["result"]
        assert "Programming Class" in result["result"]

    @pytest.mark.asyncio
    async def test_get_activity_details_tool(self, server):
        """Test get_activity_details tool"""
        result = await server.call_tool(
            "get_activity_details",
            {"activity_name": "Chess Club"}
        )

        assert "result" in result
        details = result["result"]
        assert details["name"] == "Chess Club"
        assert "description" in details
        assert "schedule" in details
        assert "participants" in details
        assert "max_participants" in details
        assert "available_spots" in details

    @pytest.mark.asyncio
    async def test_get_activity_details_not_found(self, server):
        """Test get_activity_details with non-existent activity"""
        result = await server.call_tool(
            "get_activity_details",
            {"activity_name": "NonExistent Activity"}
        )

        assert "error" in result

    @pytest.mark.asyncio
    async def test_check_availability_tool(self, server):
        """Test check_availability tool"""
        result = await server.call_tool(
            "check_availability",
            {"activity_name": "Chess Club"}
        )

        assert "result" in result
        availability = result["result"]
        assert "activity" in availability
        assert "has_availability" in availability
        assert "available_spots" in availability
        assert "total_capacity" in availability

    @pytest.mark.asyncio
    async def test_check_availability_not_found(self, server):
        """Test check_availability with non-existent activity"""
        result = await server.call_tool(
            "check_availability",
            {"activity_name": "NonExistent Activity"}
        )

        assert "error" in result

    @pytest.mark.asyncio
    async def test_call_nonexistent_tool(self, server):
        """Test calling a tool that doesn't exist"""
        result = await server.call_tool("nonexistent_tool", {})

        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_activities_catalog_resource(self, server):
        """Test activities catalog resource"""
        result = await server.get_resource("activities://catalog")

        assert "content" in result
        assert isinstance(result["content"], str)
        assert "Chess Club" in result["content"]

    @pytest.mark.asyncio
    async def test_participation_stats_resource(self, server):
        """Test participation statistics resource"""
        result = await server.get_resource("activities://stats")

        assert "content" in result
        stats = result["content"]
        assert "timestamp" in stats
        assert "total_activities" in stats
        assert "total_capacity" in stats
        assert "total_participants" in stats
        assert "overall_fill_rate" in stats

    @pytest.mark.asyncio
    async def test_nonexistent_resource(self, server):
        """Test accessing a resource that doesn't exist"""
        result = await server.get_resource("activities://nonexistent")

        assert "error" in result
        assert "not found" in result["error"].lower()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])

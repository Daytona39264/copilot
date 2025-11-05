#!/usr/bin/env python3
"""
Comprehensive Test Runner for AI Features

This script tests all components:
1. Anthropic SDK examples (demo mode)
2. AI endpoints in main application
3. MCP server functionality
4. Docker configuration validation

Run: python test_all.py
"""

import subprocess
import sys
import os
import time
import asyncio
from pathlib import Path

# ANSI color codes for pretty output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


def print_header(text):
    """Print a formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text:^70}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text):
    """Print error message"""
    print(f"{RED}✗ {text}{RESET}")


def print_info(text):
    """Print info message"""
    print(f"{YELLOW}ℹ {text}{RESET}")


def print_step(text):
    """Print step message"""
    print(f"\n{BOLD}► {text}{RESET}")


def run_command(cmd, description, check=True):
    """Run a shell command and report results"""
    print_step(description)
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print_success(f"{description} - SUCCESS")
            if result.stdout:
                print(result.stdout[:500])  # Print first 500 chars
            return True
        else:
            print_error(f"{description} - FAILED")
            if result.stderr:
                print(result.stderr[:500])
            return False
    except subprocess.TimeoutExpired:
        print_error(f"{description} - TIMEOUT")
        return False
    except Exception as e:
        print_error(f"{description} - ERROR: {e}")
        return False


def validate_file_structure():
    """Validate all required files exist"""
    print_header("FILE STRUCTURE VALIDATION")

    required_files = [
        "requirements.txt",
        "src/app.py",
        "AI_FEATURES.md",
        "examples/README.md",
        "examples/anthropic_sdk/01_basic_usage.py",
        "examples/anthropic_sdk/02_conversations.py",
        "examples/anthropic_sdk/03_advanced_features.py",
        "examples/anthropic_sdk/04_fastapi_integration.py",
        "examples/anthropic_sdk/README.md",
        "examples/mcp_server/simple_mcp_server.py",
        "examples/mcp_server/http_mcp_server.py",
        "examples/mcp_server/README.md",
        "examples/docker/Dockerfile.app",
        "examples/docker/Dockerfile.mcp",
        "examples/docker/docker-compose.yml",
        "examples/docker/README.md",
        "examples/mcp_config_example.json",
        "tests/test_ai_features.py",
        "tests/test_mcp_server.py"
    ]

    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"Found: {file_path}")
        else:
            print_error(f"Missing: {file_path}")
            all_exist = False

    return all_exist


def test_python_syntax():
    """Test Python syntax for all Python files"""
    print_header("PYTHON SYNTAX VALIDATION")

    python_files = [
        "src/app.py",
        "examples/anthropic_sdk/01_basic_usage.py",
        "examples/anthropic_sdk/02_conversations.py",
        "examples/anthropic_sdk/03_advanced_features.py",
        "examples/anthropic_sdk/04_fastapi_integration.py",
        "examples/mcp_server/simple_mcp_server.py",
        "examples/mcp_server/http_mcp_server.py",
        "tests/test_ai_features.py",
        "tests/test_mcp_server.py"
    ]

    all_valid = True
    for file_path in python_files:
        if run_command(
            f"python3 -m py_compile {file_path}",
            f"Validating {file_path}",
            check=False
        ):
            pass
        else:
            all_valid = False

    return all_valid


def test_imports():
    """Test that key modules can be imported"""
    print_header("MODULE IMPORT VALIDATION")

    imports_to_test = [
        ("fastapi", "FastAPI framework"),
        ("uvicorn", "ASGI server"),
        ("pytest", "Testing framework"),
        ("httpx", "HTTP client"),
    ]

    all_imported = True
    for module, description in imports_to_test:
        try:
            __import__(module)
            print_success(f"{description} ({module}) - OK")
        except ImportError:
            print_error(f"{description} ({module}) - NOT INSTALLED")
            all_imported = False

    # Test optional dependency
    try:
        __import__("anthropic")
        print_success("Anthropic SDK (anthropic) - OK")
    except ImportError:
        print_info("Anthropic SDK (anthropic) - Not installed (optional)")

    return all_imported


def test_mcp_server_functionality():
    """Test MCP server functionality"""
    print_header("MCP SERVER FUNCTIONALITY TEST")

    # Add path for imports
    sys.path.insert(0, 'examples/mcp_server')

    try:
        from simple_mcp_server import SchoolActivitiesMCPServer

        print_step("Creating MCP server instance")
        server = SchoolActivitiesMCPServer()
        print_success("Server created successfully")

        print_step("Listing available tools")
        tools = server.list_tools()
        print_success(f"Found {len(tools)} tools: {[t['name'] for t in tools]}")

        print_step("Listing available resources")
        resources = server.list_resources()
        print_success(f"Found {len(resources)} resources: {[r['uri'] for r in resources]}")

        print_step("Testing get_activities tool")
        result = asyncio.run(server.call_tool("get_activities", {}))
        if "result" in result:
            print_success(f"Tool returned: {result['result'][:3]}...")  # First 3 activities
        else:
            print_error(f"Tool failed: {result}")
            return False

        print_step("Testing activities://stats resource")
        result = asyncio.run(server.get_resource("activities://stats"))
        if "content" in result:
            print_success(f"Resource returned stats: {result['content']}")
        else:
            print_error(f"Resource failed: {result}")
            return False

        return True

    except Exception as e:
        print_error(f"MCP server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_pytest_tests():
    """Run pytest tests"""
    print_header("RUNNING PYTEST TESTS")

    # Run AI features tests
    print_step("Running AI features tests")
    result1 = run_command(
        "python3 -m pytest tests/test_ai_features.py -v --tb=short",
        "AI Features Tests",
        check=False
    )

    # Run MCP server tests
    print_step("Running MCP server tests")
    result2 = run_command(
        "python3 -m pytest tests/test_mcp_server.py -v --tb=short",
        "MCP Server Tests",
        check=False
    )

    return result1 and result2


def validate_docker_config():
    """Validate Docker configuration"""
    print_header("DOCKER CONFIGURATION VALIDATION")

    print_step("Validating docker-compose.yml")
    if Path("examples/docker/docker-compose.yml").exists():
        print_success("docker-compose.yml exists")

        # Check if docker-compose is available
        result = subprocess.run(
            "docker-compose --version",
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print_success(f"docker-compose is installed: {result.stdout.strip()}")

            # Validate docker-compose config
            original_dir = os.getcwd()
            os.chdir("examples/docker")
            result = run_command(
                "docker-compose config",
                "Validating docker-compose configuration",
                check=False
            )
            os.chdir(original_dir)

            return result
        else:
            print_info("docker-compose not installed (optional for deployment)")
            return True
    else:
        print_error("docker-compose.yml not found")
        return False


def create_summary_report(results):
    """Create a summary report"""
    print_header("TEST SUMMARY REPORT")

    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed

    print(f"\n{BOLD}Total Tests: {total}{RESET}")
    print(f"{GREEN}Passed: {passed}{RESET}")
    print(f"{RED}Failed: {failed}{RESET}")
    print(f"\nSuccess Rate: {(passed/total*100):.1f}%\n")

    print(f"{BOLD}Detailed Results:{RESET}")
    for test_name, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name:.<50} {status}")

    return passed == total


def main():
    """Main test runner"""
    print_header("COMPREHENSIVE TEST SUITE FOR AI FEATURES")
    print("Testing all components of the AI integration\n")

    results = {}

    # Run all tests
    results["File Structure"] = validate_file_structure()
    results["Python Syntax"] = test_python_syntax()
    results["Module Imports"] = test_imports()
    results["MCP Server"] = test_mcp_server_functionality()
    results["Pytest Suite"] = run_pytest_tests()
    results["Docker Config"] = validate_docker_config()

    # Generate summary
    all_passed = create_summary_report(results)

    if all_passed:
        print(f"\n{GREEN}{BOLD}🎉 ALL TESTS PASSED! 🎉{RESET}\n")
        print("The AI features implementation is complete and functional.")
        print("\nNext steps:")
        print("  1. Set ANTHROPIC_API_KEY to test AI features")
        print("  2. Run: python examples/mcp_server/http_mcp_server.py")
        print("  3. Run: cd src && python app.py")
        print("  4. Deploy: cd examples/docker && docker-compose up")
        return 0
    else:
        print(f"\n{RED}{BOLD}⚠️  SOME TESTS FAILED{RESET}\n")
        print("Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

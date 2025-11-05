"""
Advanced Features of the Anthropic Python SDK

This example demonstrates:
- Streaming responses
- Tool use (function calling)
- Vision capabilities
- Error handling
"""

from anthropic import Anthropic
import os
import json
import base64

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here"))


def streaming_response():
    """Stream responses token by token"""
    print("=== Streaming Response Example ===\n")

    print("Claude's response (streaming): ", end="", flush=True)

    with client.messages.stream(
        model="claude-opus-4-1-20250805",
        max_tokens=500,
        messages=[{"role": "user", "content": "Write a haiku about programming"}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n\n" + "="*50 + "\n")


def tool_use_example():
    """Demonstrate tool use (function calling)"""
    print("=== Tool Use Example ===\n")

    # Define tools that Claude can use
    tools = [
        {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature"
                    }
                },
                "required": ["location"]
            }
        },
        {
            "name": "calculator",
            "description": "Perform mathematical calculations",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    ]

    # Send a message that should trigger tool use
    response = client.messages.create(
        model="claude-opus-4-1-20250805",
        max_tokens=1000,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather like in San Francisco? Also, what's 15 * 27?"}
        ]
    )

    print("Claude's response:")
    for content in response.content:
        if content.type == "text":
            print(f"Text: {content.text}")
        elif content.type == "tool_use":
            print(f"\nTool Called: {content.name}")
            print(f"Tool Input: {json.dumps(content.input, indent=2)}")

    print("\n" + "="*50 + "\n")


def vision_example():
    """Demonstrate vision capabilities with images"""
    print("=== Vision Example ===\n")

    # Example with a URL (you would replace with a real image URL)
    response = client.messages.create(
        model="claude-opus-4-1-20250805",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Describe this image in detail"
                    }
                ]
            }
        ]
    )

    print("Image analysis:")
    print(response.content[0].text)
    print("\n" + "="*50 + "\n")


def vision_with_base64():
    """Example of using base64-encoded images"""
    print("=== Vision with Base64 Example ===\n")

    # Create a simple example (in practice, you'd read a real image file)
    example_usage = """
    # To use base64 images, read and encode your image:
    import base64

    with open("path/to/image.jpg", "rb") as image_file:
        image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")

    response = client.messages.create(
        model="claude-opus-4-1-20250805",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    }
                ]
            }
        ]
    )
    """

    print(example_usage)
    print("\n" + "="*50 + "\n")


def error_handling_example():
    """Demonstrate proper error handling"""
    print("=== Error Handling Example ===\n")

    from anthropic import APIError, APIConnectionError, RateLimitError

    try:
        # This might fail if rate limits are hit
        response = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1000,
            messages=[{"role": "user", "content": "Hello!"}]
        )
        print("Success!")

    except RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        print("Please wait and try again later")

    except APIConnectionError as e:
        print(f"Connection error: {e}")
        print("Check your internet connection")

    except APIError as e:
        print(f"API error: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Error type: {e.type}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    print("\n" + "="*50 + "\n")


def async_example_code():
    """Show async usage example"""
    print("=== Async Usage Example ===\n")

    example = """
    # For async usage, use AsyncAnthropic client:
    from anthropic import AsyncAnthropic
    import asyncio

    async def main():
        client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        response = await client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1000,
            messages=[{"role": "user", "content": "Hello!"}]
        )

        print(response.content[0].text)

    asyncio.run(main())
    """

    print(example)
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    try:
        # Run examples
        streaming_response()
        tool_use_example()
        vision_example()
        vision_with_base64()
        error_handling_example()
        async_example_code()

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set your ANTHROPIC_API_KEY environment variable:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")

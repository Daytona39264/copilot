"""
Basic Usage of the Anthropic Python SDK

This example demonstrates the fundamental way to use the Anthropic API
to send messages and receive responses from Claude.
"""

from anthropic import Anthropic
import os

# Initialize the client
# API key can be set via environment variable ANTHROPIC_API_KEY
# or passed directly to the constructor
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here")
)

def basic_message():
    """Send a basic message to Claude"""
    response = client.messages.create(
        model="claude-opus-4-1-20250805",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Hello! How can I use the Anthropic API?"}
        ]
    )

    print("Response:")
    print(response.content[0].text)
    print("\n" + "="*50 + "\n")

    return response


def message_with_system_prompt():
    """Send a message with a system prompt to set context"""
    response = client.messages.create(
        model="claude-opus-4-1-20250805",
        max_tokens=1000,
        system="You are a helpful coding assistant specializing in Python.",
        messages=[
            {"role": "user", "content": "Write a function to calculate fibonacci numbers"}
        ]
    )

    print("Response with system prompt:")
    print(response.content[0].text)
    print("\n" + "="*50 + "\n")

    return response


def message_with_parameters():
    """Demonstrate using different parameters"""
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",  # Using Sonnet for faster responses
        max_tokens=500,
        temperature=0.7,  # Control randomness (0.0 = deterministic, 1.0 = creative)
        messages=[
            {"role": "user", "content": "Explain quantum computing in simple terms"}
        ]
    )

    print("Response with custom parameters:")
    print(response.content[0].text)
    print("\n" + "="*50 + "\n")

    # Print metadata
    print(f"Model used: {response.model}")
    print(f"Tokens used - Input: {response.usage.input_tokens}, Output: {response.usage.output_tokens}")

    return response


if __name__ == "__main__":
    print("Anthropic SDK Basic Examples\n")

    try:
        # Example 1: Basic message
        basic_message()

        # Example 2: Message with system prompt
        message_with_system_prompt()

        # Example 3: Message with custom parameters
        message_with_parameters()

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set your ANTHROPIC_API_KEY environment variable:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")

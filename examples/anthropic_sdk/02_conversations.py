"""
Multi-turn Conversations with Claude

This example demonstrates how to maintain conversation history
and have back-and-forth interactions with Claude.
"""

from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here"))


class ConversationManager:
    """Helper class to manage conversation history"""

    def __init__(self, model="claude-opus-4-1-20250805", system_prompt=None):
        self.model = model
        self.system_prompt = system_prompt
        self.messages = []

    def add_user_message(self, content):
        """Add a user message to the conversation"""
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        """Add an assistant message to the conversation"""
        self.messages.append({"role": "assistant", "content": content})

    def get_response(self, max_tokens=1000, temperature=1.0):
        """Get Claude's response and add it to the conversation"""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": self.messages
        }

        if self.system_prompt:
            kwargs["system"] = self.system_prompt

        response = client.messages.create(**kwargs)

        # Extract the text response
        assistant_message = response.content[0].text

        # Add to conversation history
        self.add_assistant_message(assistant_message)

        return assistant_message, response

    def clear(self):
        """Clear the conversation history"""
        self.messages = []


def simple_conversation():
    """Example of a simple multi-turn conversation"""
    print("=== Simple Conversation Example ===\n")

    conversation = ConversationManager()

    # Turn 1
    conversation.add_user_message("What's the capital of France?")
    response, _ = conversation.get_response()
    print(f"User: What's the capital of France?")
    print(f"Claude: {response}\n")

    # Turn 2 - Claude remembers context
    conversation.add_user_message("What's the population of that city?")
    response, _ = conversation.get_response()
    print(f"User: What's the population of that city?")
    print(f"Claude: {response}\n")

    # Turn 3 - Continue the conversation
    conversation.add_user_message("Tell me an interesting fact about it")
    response, _ = conversation.get_response()
    print(f"User: Tell me an interesting fact about it")
    print(f"Claude: {response}\n")


def coding_assistant_conversation():
    """Example of a coding assistant conversation"""
    print("\n" + "="*50)
    print("=== Coding Assistant Example ===\n")

    conversation = ConversationManager(
        model="claude-sonnet-4-5-20250929",
        system_prompt="You are an expert Python developer. Provide clear, concise code examples."
    )

    # Request 1: Write initial code
    conversation.add_user_message("Write a Python function to check if a number is prime")
    response, _ = conversation.get_response()
    print(f"User: Write a Python function to check if a number is prime")
    print(f"Claude: {response}\n")

    # Request 2: Modify the code
    conversation.add_user_message("Now optimize it for large numbers")
    response, _ = conversation.get_response()
    print(f"User: Now optimize it for large numbers")
    print(f"Claude: {response}\n")

    # Request 3: Add tests
    conversation.add_user_message("Add unit tests for this function")
    response, _ = conversation.get_response()
    print(f"User: Add unit tests for this function")
    print(f"Claude: {response}\n")


def interactive_conversation():
    """Interactive conversation loop"""
    print("\n" + "="*50)
    print("=== Interactive Conversation ===")
    print("Type 'quit' to exit, 'clear' to start a new conversation\n")

    conversation = ConversationManager(
        system_prompt="You are a helpful and friendly AI assistant."
    )

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            conversation.clear()
            print("Conversation cleared. Starting fresh!\n")
            continue

        if not user_input:
            continue

        conversation.add_user_message(user_input)

        try:
            response, metadata = conversation.get_response()
            print(f"\nClaude: {response}\n")
            print(f"[Tokens - Input: {metadata.usage.input_tokens}, Output: {metadata.usage.output_tokens}]\n")
        except Exception as e:
            print(f"Error: {e}\n")
            break


if __name__ == "__main__":
    try:
        # Run examples
        simple_conversation()
        coding_assistant_conversation()

        # Uncomment to try interactive mode
        # interactive_conversation()

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set your ANTHROPIC_API_KEY environment variable:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")

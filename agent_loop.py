from tool_executor import execute_tool


def run_agent(task):
    """
    Simulated agent loop.

    This version demonstrates the architecture
    without making Gemini API calls.
    """

    print("User:", task)

    # Simulated AI decision
    tool_name = "calculate_expression"

    arguments = {
        "expression": task
    }

    print("\nAI decided to use:", tool_name)
    print("Arguments:", arguments)

    # Execute tool
    result = execute_tool(
        tool_name,
        arguments
    )

    print("\nTool result:", result)

    # Simulated second AI decision
    print("\nAI received the tool result.")

    print("Agent: The calculation result is", result)


# Test
run_agent("21*12")
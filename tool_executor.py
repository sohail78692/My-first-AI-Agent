from tools import calculate_expression
from text_tools import analyze_text
from memory import remember, recall, get_all_memories


def execute_tool(tool_name, arguments):
    """
    Execute a tool requested by the AI agent.
    """

    # ========================================================
    # Calculator
    # ========================================================

    if tool_name == "calculate_expression":

        expression = arguments["expression"]

        return calculate_expression(expression)


    # ========================================================
    # Text Analyzer
    # ========================================================

    elif tool_name == "analyze_text":

        text = arguments["text"]

        return analyze_text(text)


    # ========================================================
    # Remember
    # ========================================================

    elif tool_name == "remember":

        key = arguments["key"]
        value = arguments["value"]

        return remember(key, value)


    # ========================================================
    # Recall
    # ========================================================

    elif tool_name == "recall":

        key = arguments["key"]

        return recall(key)


    # ========================================================
    # Get All Memories
    # ========================================================

    elif tool_name == "get_all_memories":

        return get_all_memories()


    # ========================================================
    # Unknown Tool
    # ========================================================

    else:

        return {
            "error": f"Unknown tool: {tool_name}"
        }
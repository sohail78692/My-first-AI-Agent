from tools import calculate_expression
from text_tools import analyze_text
from memory import remember, recall


def execute_tool(tool_name, arguments):
    """
    Execute a tool requested by the AI agent.
    """

    if tool_name == "calculate_expression":

        expression = arguments["expression"]

        return calculate_expression(expression)


    elif tool_name == "analyze_text":

        text = arguments["text"]

        return analyze_text(text)


    elif tool_name == "remember":

        key = arguments["key"]
        value = arguments["value"]

        return remember(key, value)


    elif tool_name == "recall":

        key = arguments["key"]

        return recall(key)


    else:

        return {
            "error": f"Unknown tool: {tool_name}"
        }
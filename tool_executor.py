from tools import calculate_expression
from text_tools import analyze_text


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


    else:

        return {
            "error": f"Unknown tool: {tool_name}"
        }
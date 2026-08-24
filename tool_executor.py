from tools import calculate_expression
from text_tools import analyze_text
from memory import remember, recall, get_all_memories
from web_search import web_search
from fetch_webpage import fetch_webpage


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
    # Web Search
    # ========================================================

    elif tool_name == "web_search":

        query = arguments["query"]

        max_results = arguments.get(
            "max_results",
            5
        )

        return web_search(
            query,
            max_results
        )


    # ========================================================
    # Fetch Webpage
    # ========================================================

    elif tool_name == "fetch_webpage":

        url = arguments["url"]

        max_characters = arguments.get(
            "max_characters",
            5000
        )

        return fetch_webpage(
            url,
            max_characters
        )


    # ========================================================
    # Unknown Tool
    # ========================================================

    else:

        return {
            "error": f"Unknown tool: {tool_name}"
        }
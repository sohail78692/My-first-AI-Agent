from tool_executor import execute_tool


# Test calculator
result = execute_tool(
    "calculate_expression",
    {
        "expression": "21*12"
    }
)

print("Calculator:")
print(result)


# Test text analyzer
result = execute_tool(
    "analyze_text",
    {
        "text": "AI agents can use tools."
    }
)

print("\nText Analyzer:")
print(result)
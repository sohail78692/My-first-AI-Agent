import os

from google import genai
from google.genai import types

from tools import calculate_expression
from text_tools import analyze_text


# 1. Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key NOT found!")
    exit()

print("API key found!")


# 2. Create Gemini client
client = genai.Client(api_key=api_key)


# 3. Define calculator tool
calculator_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculate_expression",
            description=(
                "Safely evaluate a mathematical expression. "
                "Use this tool whenever the user asks for a "
                "mathematical calculation."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A complete mathematical expression, "
                            "such as 21*12, 454-12+22, "
                            "or (10+5)*3."
                        )
                    }
                },
                "required": ["expression"]
            }
        )
    ]
)


# 4. Define text analysis tool
text_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_text",
            description=(
                "Analyze text and return the number of words "
                "and characters."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze."
                    }
                },
                "required": ["text"]
            }
        )
    ]
)


# 5. Combine both tools
tools = [
    calculator_tool,
    text_tool
]


# 6. Create the AI agent
chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction="""
You are a helpful AI agent.

You have access to two tools:

1. calculate_expression
   Use this for mathematical calculations.

2. analyze_text
   Use this when the user asks you to analyze text,
   such as counting words or characters.

Choose the appropriate tool based on the user's request.

After receiving a tool result, provide a clear final answer.
""",
        tools=tools
    )
)


# 7. Start the agent
print("\nAI Agent is ready!")
print("Available tools:")
print("- Calculator")
print("- Text Analyzer")
print("\nType 'exit' to stop.\n")


while True:

    user_question = input("You: ")

    if user_question.lower() == "exit":
        print("Agent: Goodbye! 👋")
        break


    # 8. Send user request to Gemini
    response = chat.send_message(user_question)


    # 9. Check for tool calls
    tool_was_used = False

    for part in response.candidates[0].content.parts:

        if part.function_call:

            tool_was_used = True

            function_call = part.function_call

            print(
                "\nAgent decided to use:",
                function_call.name
            )

            print(
                "Arguments:",
                function_call.args
            )


            # 10. Calculator tool
            if function_call.name == "calculate_expression":

                expression = function_call.args["expression"]

                result = calculate_expression(expression)


            # 11. Text analyzer tool
            elif function_call.name == "analyze_text":

                text = function_call.args["text"]

                result = analyze_text(text)


            else:

                result = "Unknown tool"


            # 12. Show tool result
            print("Tool result:", result)


            # 13. Send result back to Gemini
            tool_response = types.Part.from_function_response(
                name=function_call.name,
                response={
                    "result": result
                }
            )

            final_response = chat.send_message(
                tool_response
            )


            # 14. Final answer
            print("\nAgent:", final_response.text)


    # 15. No tool required
    if not tool_was_used:

        print("\nAgent:", response.text)
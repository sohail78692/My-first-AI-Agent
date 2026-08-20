import os

from google import genai
from google.genai import types

from tools import calculate_expression


# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key NOT found!")
    exit()

print("API key found!")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Define calculator tool
calculator_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculate_expression",
            description=(
                "Safely evaluate a mathematical expression. "
                "Use this tool whenever the user asks for a calculation "
                "or enters a mathematical expression."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A mathematical expression such as "
                            "21*12, 454-12+22, or (10+5)*3."
                        )
                    }
                },
                "required": ["expression"]
            }
        )
    ]
)


# Create agent
chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction="""
You are a helpful AI agent.

Use the available calculator tool whenever the user
asks for a mathematical calculation.

The calculator can evaluate complete mathematical
expressions, including:

21*12
454-12+22
2+2*4
(10+5)*3

Always send the complete mathematical expression
to the calculator tool.

After receiving the calculator result, provide
a clear final answer to the user.
""",
        tools=[calculator_tool]
    )
)


# Start conversation
print("\nAI Agent is ready!")
print("Type 'exit' to stop.\n")


while True:

    user_question = input("You: ")

    if user_question.lower() == "exit":
        print("Agent: Goodbye! 👋")
        break


    # Send message to Gemini
    response = chat.send_message(user_question)


    # Look for tool calls
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


            # Execute calculator
            if function_call.name == "calculate_expression":

                expression = function_call.args["expression"]

                result = calculate_expression(expression)

                print("Tool result:", result)


                # Send result back to Gemini
                tool_response = types.Part.from_function_response(
                    name=function_call.name,
                    response={
                        "result": result
                    }
                )

                final_response = chat.send_message(
                    tool_response
                )

                print("\nAgent:", final_response.text)


    # No tool required
    if not tool_was_used:

        print("\nAgent:", response.text)
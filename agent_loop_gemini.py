import os

from google import genai
from google.genai import types

from tool_executor import execute_tool


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
                "Use this for mathematical calculations."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Complete mathematical expression."
                    }
                },
                "required": ["expression"]
            }
        )
    ]
)


# 4. Define text analyzer tool
text_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_text",
            description=(
                "Analyze text and return word count "
                "and character count."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze."
                    }
                },
                "required": ["text"]
            }
        )
    ]
)


# 5. Create chat
chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction="""
You are a helpful AI agent.

You have two tools:

1. calculate_expression
   Use for mathematical calculations.

2. analyze_text
   Use for analyzing text.

Choose the appropriate tool when needed.

After receiving a tool result, decide whether you
need another tool or whether you can provide the
final answer.
""",
        tools=[
            calculator_tool,
            text_tool
        ]
    )
)


# 6. Agent loop
def run_agent(user_message):

    response = chat.send_message(user_message)

    while True:

        function_calls = []

        # Find all function calls in the response
        for part in response.candidates[0].content.parts:

            if part.function_call:
                function_calls.append(part.function_call)


        # No function call = final answer
        if not function_calls:

            return response.text


        # Execute every requested tool
        tool_responses = []

        for function_call in function_calls:

            print(
                "\nAgent decided to use:",
                function_call.name
            )

            print(
                "Arguments:",
                function_call.args
            )


            # Execute through our central executor
            result = execute_tool(
                function_call.name,
                function_call.args
            )


            print(
                "Tool result:",
                result
            )


            # Prepare tool response
            tool_response = types.Part.from_function_response(
                name=function_call.name,
                response={
                    "result": result
                }
            )

            tool_responses.append(tool_response)


        # Send ALL tool results back to Gemini
        response = chat.send_message(
            tool_responses
        )


# 7. Interactive terminal
print("\nAI Agent is ready!")
print("Type 'exit' to stop.\n")


while True:

    user_message = input("You: ")

    if user_message.lower() == "exit":

        print("Agent: Goodbye! 👋")
        break


    try:

        answer = run_agent(user_message)

        print("\nAgent:", answer)


    except Exception as error:

        print("\nAgent error:", error)
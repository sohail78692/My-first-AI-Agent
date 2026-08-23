import os

from google import genai
from google.genai import types

from tool_executor import execute_tool


# ============================================================
# 1. Get API key
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key NOT found!")
    exit()

print("API key found!")


# ============================================================
# 2. Create Gemini client
# ============================================================

client = genai.Client(api_key=api_key)


# ============================================================
# 3. Calculator Tool
# ============================================================

calculator_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculate_expression",
            description=(
                "Safely evaluate a mathematical expression. "
                "Use this tool whenever the user asks for "
                "a mathematical calculation."
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


# ============================================================
# 4. Text Analyzer Tool
# ============================================================

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


# ============================================================
# 5. Persistent Memory Tools
# ============================================================

memory_tool = types.Tool(
    function_declarations=[

        # ----------------------------------------------------
        # Remember
        # ----------------------------------------------------

        types.FunctionDeclaration(
            name="remember",
            description=(
                "Store useful information in persistent memory. "
                "Use this when the user explicitly asks you to "
                "remember something or provides information that "
                "is clearly useful for future conversations."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": (
                            "A short name for the information, "
                            "for example favorite_language."
                        )
                    },
                    "value": {
                        "type": "string",
                        "description": (
                            "The information that should be remembered."
                        )
                    }
                },
                "required": [
                    "key",
                    "value"
                ]
            }
        ),

        # ----------------------------------------------------
        # Recall
        # ----------------------------------------------------

        types.FunctionDeclaration(
            name="recall",
            description=(
                "Retrieve previously stored information from "
                "persistent memory when it is relevant to the "
                "user's request."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": (
                            "The name or key of the information "
                            "to retrieve."
                        )
                    }
                },
                "required": [
                    "key"
                ]
            }
        ),

        # ----------------------------------------------------
        # Get All Memories
        # ----------------------------------------------------

        types.FunctionDeclaration(
            name="get_all_memories",
            description=(
                "Retrieve all information currently stored "
                "in persistent memory. Use this when the user "
                "asks what you remember about them or asks "
                "for a list of stored memories."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {}
            }
        )
    ]
)


# ============================================================
# 6. Create Gemini Chat
# ============================================================

chat = client.chats.create(
    model="gemini-3.6-flash",

    config=types.GenerateContentConfig(

        system_instruction="""
You are a helpful AI agent.

You have five tools:

1. calculate_expression
   Use this tool for mathematical calculations.

2. analyze_text
   Use this tool when the user asks you to analyze
   text, such as counting words or characters.

3. remember
   Use this tool when the user explicitly asks you
   to remember something or provides information that
   is clearly useful for future conversations.

4. recall
   Use this tool when information from persistent memory
   is needed to answer the user's request.

5. get_all_memories
   Use this tool when the user asks what you remember
   about them or requests a list of stored memories.

Choose the appropriate tool based on the user's request.

After receiving a tool result, decide whether you need
another tool or whether you can provide the final answer.

Do not invent memories.

Only use information returned by the recall or
get_all_memories tools when answering questions about
stored memories.
""",

        tools=[
            calculator_tool,
            text_tool,
            memory_tool
        ]
    )
)


# ============================================================
# 7. Reusable Agent Loop
# ============================================================

def run_agent(user_message):

    # Send the user's message to Gemini
    response = chat.send_message(user_message)

    # Continue until Gemini produces a final answer
    while True:

        function_calls = []

        # ----------------------------------------------------
        # Find all function calls in Gemini's response
        # ----------------------------------------------------

        for part in response.candidates[0].content.parts:

            if part.function_call:

                function_calls.append(
                    part.function_call
                )

        # ----------------------------------------------------
        # No tool call means Gemini has the final answer
        # ----------------------------------------------------

        if not function_calls:

            return response.text

        # ----------------------------------------------------
        # Execute requested tools
        # ----------------------------------------------------

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

            # Execute the tool
            result = execute_tool(
                function_call.name,
                function_call.args
            )

            print(
                "Tool result:",
                result
            )

            # ------------------------------------------------
            # Create tool response for Gemini
            # ------------------------------------------------

            tool_response = types.Part.from_function_response(
                name=function_call.name,
                response={
                    "result": result
                }
            )

            tool_responses.append(
                tool_response
            )

        # ----------------------------------------------------
        # Send tool results back to Gemini
        # ----------------------------------------------------

        response = chat.send_message(
            tool_responses
        )


# ============================================================
# 8. Start Interactive Agent
# ============================================================

print("\nAI Agent is ready!")

print("Available tools:")
print("- Calculator")
print("- Text Analyzer")
print("- Remember")
print("- Recall")
print("- Get All Memories")

print("\nType 'exit' to stop.\n")


while True:

    user_message = input("You: ")

    # --------------------------------------------------------
    # Exit
    # --------------------------------------------------------

    if user_message.lower() == "exit":

        print("Agent: Goodbye! 👋")

        break

    # --------------------------------------------------------
    # Run agent
    # --------------------------------------------------------

    try:

        answer = run_agent(
            user_message
        )

        print(
            "\nAgent:",
            answer
        )

    except Exception as error:

        print(
            "\nAgent error:",
            error
        )
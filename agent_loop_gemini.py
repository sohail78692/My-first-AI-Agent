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

client = genai.Client(
    api_key=api_key
)


# ============================================================
# 3. Calculator Tool
# ============================================================

calculator_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculate_expression",
            description=(
                "Calculate a mathematical expression. "
                "Use this tool whenever the user asks "
                "for a mathematical calculation."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A mathematical expression such as "
                            "21*12 or (10+5)*3."
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


# ============================================================
# 5. Memory Tools
# ============================================================

memory_tool = types.Tool(
    function_declarations=[

        # ----------------------------------------------------
        # Remember
        # ----------------------------------------------------

        types.FunctionDeclaration(
            name="remember",
            description=(
                "Store information in persistent memory "
                "when the user explicitly asks you to "
                "remember something."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "Memory key."
                    },
                    "value": {
                        "type": "string",
                        "description": "Information to remember."
                    }
                },
                "required": ["key", "value"]
            }
        ),

        # ----------------------------------------------------
        # Recall
        # ----------------------------------------------------

        types.FunctionDeclaration(
            name="recall",
            description=(
                "Retrieve a specific piece of information "
                "from persistent memory."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "Memory key to retrieve."
                    }
                },
                "required": ["key"]
            }
        ),

        # ----------------------------------------------------
        # Get All Memories
        # ----------------------------------------------------

        types.FunctionDeclaration(
            name="get_all_memories",
            description=(
                "Retrieve all stored memories when the "
                "user asks what you remember about them."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {}
            }
        )
    ]
)


# ============================================================
# 6. Web Search Tool
# ============================================================

web_search_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="web_search",
            description=(
                "Search the internet for current or external "
                "information. Use this when information is "
                "latest, recent, current, or up-to-date."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query."
                    },
                    "max_results": {
                        "type": "integer",
                        "description": (
                            "Maximum number of results. "
                            "Usually 3 to 5."
                        )
                    }
                },
                "required": ["query"]
            }
        )
    ]
)


# ============================================================
# 7. Fetch Webpage Tool
# ============================================================

fetch_webpage_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="fetch_webpage",
            description=(
                "Fetch and read the contents of a webpage. "
                "Use this after web_search when you need "
                "actual information from a search result. "
                "The URL must be a normal HTTP or HTTPS URL."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": (
                            "The URL of the webpage to read."
                        )
                    },
                    "max_characters": {
                        "type": "integer",
                        "description": (
                            "Maximum amount of webpage text "
                            "to retrieve. Usually 5000."
                        )
                    }
                },
                "required": ["url"]
            }
        )
    ]
)


# ============================================================
# 8. Create Gemini Chat
# ============================================================

chat = client.chats.create(
    model="gemini-3.6-flash",

    config=types.GenerateContentConfig(

        system_instruction="""
You are a helpful AI agent.

You have seven tools:

1. calculate_expression
   Use for mathematical calculations.

2. analyze_text
   Use for text analysis.

3. remember
   Use when the user explicitly asks you
   to remember information.

4. recall
   Use to retrieve a specific stored memory.

5. get_all_memories
   Use when the user asks what you remember
   about them.

6. web_search
   Use when the user needs current, recent,
   latest, or up-to-date information.

7. fetch_webpage
   Use to read the actual contents of a webpage.

WEB RESEARCH WORKFLOW:

When the user asks for current or web-based information:

1. Use web_search first.
2. Look at the search results.
3. Select the most relevant result.
4. Use fetch_webpage with that result's URL.
5. Read the returned webpage content.
6. Answer the user's question using the
   information from the webpage.

Do NOT repeatedly call web_search if you already
have a useful result.

If web_search returns a relevant official source,
prefer that source over less authoritative sources.

For example:

User:
"What is the latest Python version?"

Correct workflow:

web_search
    ↓
Find Python.org release page
    ↓
fetch_webpage
    ↓
Read release information
    ↓
Answer the user

Other rules:

- Use the appropriate tool for the user's request.
- Do not invent information.
- Do not invent memories.
- Only use memory tool results for stored memories.
- After receiving a tool result, decide whether
  another tool is actually necessary.
- If you have enough information, provide the
  final answer.
""",

        tools=[
            calculator_tool,
            text_tool,
            memory_tool,
            web_search_tool,
            fetch_webpage_tool
        ]
    )
)


# ============================================================
# 9. Agent Loop
# ============================================================

def run_agent(user_message):

    response = chat.send_message(
        user_message
    )

    # Safety limit
    max_tool_rounds = 5
    tool_round = 0

    while True:

        tool_round += 1

        # ----------------------------------------------------
        # Prevent endless tool calls
        # ----------------------------------------------------

        if tool_round > max_tool_rounds:

            return (
                "I reached the maximum number of tool calls "
                "for this request. Please try asking the "
                "question more specifically."
            )


        # ----------------------------------------------------
        # Find function calls
        # ----------------------------------------------------

        function_calls = []

        for part in response.candidates[0].content.parts:

            if part.function_call:

                function_calls.append(
                    part.function_call
                )


        # ----------------------------------------------------
        # No function call = final answer
        # ----------------------------------------------------

        if not function_calls:

            return response.text


        # ----------------------------------------------------
        # Execute tools
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


            # Execute tool
            result = execute_tool(
                function_call.name,
                function_call.args
            )


            print(
                "Tool result:",
                result
            )


            # Send result back to Gemini
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
        # Continue conversation
        # ----------------------------------------------------

        response = chat.send_message(
            tool_responses
        )


# ============================================================
# 10. Start Agent
# ============================================================

print("\nAI Agent is ready!")

print("Available tools:")
print("- Calculator")
print("- Text Analyzer")
print("- Remember")
print("- Recall")
print("- Get All Memories")
print("- Web Search")
print("- Fetch Webpage")

print("\nType 'exit' to stop.\n")


# ============================================================
# 11. Interactive Loop
# ============================================================

while True:

    user_message = input("You: ")


    if user_message.lower() == "exit":

        print("Agent: Goodbye! 👋")

        break


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
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
                "Use this for mathematical calculations."
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
                "Search the internet for current, recent, "
                "latest, or external information. "
                "Use this to discover relevant webpages."
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
                "Fetch and read the actual contents of a "
                "webpage. Use this after web_search when "
                "a useful URL has been found."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": (
                            "The webpage URL to read."
                        )
                    },
                    "max_characters": {
                        "type": "integer",
                        "description": (
                            "Maximum webpage content to read. "
                            "Usually 5000."
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

Available tools:

1. calculate_expression
   Use for mathematical calculations.

2. analyze_text
   Use for text analysis.

3. remember
   Use when the user explicitly asks you
   to remember something.

4. recall
   Use to retrieve a specific stored memory.

5. get_all_memories
   Use when the user asks what you remember
   about them.

6. web_search
   Use to discover webpages containing current
   or external information.

7. fetch_webpage
   Use to read the actual content of a webpage.

============================================================
WEB RESEARCH RULES
============================================================

When the user asks for current, latest, recent,
or web-based information:

STEP 1:
Use web_search.

STEP 2:
Look at the search results.

STEP 3:
Choose the most relevant result, preferably
an official or authoritative source.

STEP 4:
Use fetch_webpage on that result's URL.

STEP 5:
Read the returned webpage content.

STEP 6:
Answer the user using the webpage content.

IMPORTANT:

After fetch_webpage returns useful content,
do NOT perform another web search.

Do not repeatedly search for the same question.

Once a useful webpage has been fetched,
use that webpage content to answer.

If the webpage does not contain enough information,
you may use another tool only when necessary.

If web_search returns no useful results but you
already know a trustworthy URL from the conversation,
you may use fetch_webpage directly.

============================================================
GENERAL RULES
============================================================

- Use the appropriate tool for the user's request.
- Do not invent information.
- Do not invent memories.
- Only use memory tool results for memory questions.
- Use current web information when the user asks
  for current information.
- Avoid unnecessary tool calls.
- After obtaining enough information, answer directly.
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

    # --------------------------------------------------------
    # Send initial user message
    # --------------------------------------------------------

    response = chat.send_message(
        user_message
    )

    # --------------------------------------------------------
    # Safety limit
    # --------------------------------------------------------

    max_tool_rounds = 5
    tool_round = 0

    # --------------------------------------------------------
    # Web research state
    #
    # Once we successfully fetch useful webpage content,
    # we block additional web searches for this request.
    # --------------------------------------------------------

    webpage_fetched = False

    while True:

        tool_round += 1

        # ----------------------------------------------------
        # Safety protection
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

            tool_name = function_call.name
            tool_args = function_call.args

            print(
                "\nAgent decided to use:",
                tool_name
            )

            print(
                "Arguments:",
                tool_args
            )

            # =================================================
            # WEB SEARCH PROTECTION
            # =================================================

            if webpage_fetched and tool_name == "web_search":

                print(
                    "\nSkipping unnecessary web search "
                    "because a webpage was already fetched."
                )

                result = {
                    "success": False,
                    "error": (
                        "A useful webpage has already been "
                        "fetched for this request. "
                        "Do not perform another web search. "
                        "Use the webpage content already "
                        "provided."
                    )
                }

            else:

                # ------------------------------------------------
                # Execute selected tool
                # ------------------------------------------------

                result = execute_tool(
                    tool_name,
                    tool_args
                )

            # ----------------------------------------------------
            # Print tool result
            # ----------------------------------------------------

            print(
                "Tool result:",
                result
            )

            # =================================================
            # DETECT SUCCESSFUL WEBPAGE FETCH
            # =================================================

            if tool_name == "fetch_webpage":

                if isinstance(result, dict):

                    if result.get("success") is True:

                        content = result.get(
                            "content",
                            ""
                        )

                        if (
                            isinstance(content, str)
                            and len(content.strip()) > 100
                        ):

                            webpage_fetched = True

                            print(
                                "\nWebpage fetched successfully."
                            )

                            print(
                                "Further web searches are "
                                "blocked for this request."
                            )

            # ------------------------------------------------
            # Send tool result back to Gemini
            # ------------------------------------------------

            tool_response = types.Part.from_function_response(
                name=tool_name,
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

    if not user_message.strip():
        continue

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
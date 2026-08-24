# 🤖 My First AI Agent

A beginner-friendly AI agent built with Python and Google's Gemini API.

This project is being built step-by-step to understand how AI agents actually work under the hood.

Instead of creating a simple chatbot, this project focuses on giving an LLM access to multiple tools and allowing it to decide which tool should be used based on the user's request.

---

## 🚀 Project Overview

This AI agent can currently:

- Perform mathematical calculations
- Analyze text
- Remember information
- Recall stored information
- Retrieve all stored memories
- Search the web
- Fetch and read webpages
- Use multiple tools for a single request
- Perform sequential tool calls
- Handle tool errors
- Limit the number of tool calls to prevent infinite loops

The agent uses Gemini's function-calling capabilities to decide which tool should be executed.

---

## ✨ Features

### 🧮 1. Calculator

The calculator tool evaluates mathematical expressions.

Example:

    You: 21*12

    Agent decided to use: calculate_expression
    Arguments: {'expression': '21*12'}

    Tool result: 252

    Agent: 21 * 12 = 252

---

### 📝 2. Text Analyzer

The text analyzer can analyze text and return:

- Word count
- Character count

Example:

    You: Analyze this text: AI agents can use multiple tools.

    Agent decided to use: analyze_text

    Arguments:
    {
        'text': 'AI agents can use multiple tools.'
    }

    Tool result:
    {
        'word_count': 6,
        'character_count': 33
    }

---

### 🧠 3. Remember

The agent can store information in persistent memory.

Example:

    You: Remember that my favorite programming language is Python.

    Agent decided to use: remember

    Arguments:
    {
        'key': 'favorite_programming_language',
        'value': 'Python'
    }

    Tool result:
    {
        'success': True,
        'key': 'favorite_programming_language',
        'value': 'Python'
    }

    Agent: I've remembered that your favorite programming language is Python!

---

### 🔎 4. Recall

The agent can retrieve a specific stored memory.

Example:

    You: What is my favorite programming language?

    Agent decided to use: recall

    Arguments:
    {
        'key': 'favorite_programming_language'
    }

    Tool result:
    {
        'found': True,
        'key': 'favorite_programming_language',
        'value': 'Python'
    }

    Agent: Your favorite programming language is Python.

---

### 🗂️ 5. Get All Memories

The agent can retrieve all stored memories.

Example:

    You: What do you remember about me?

    Agent decided to use: get_all_memories

    Arguments:
    {}

    Tool result:
    {
        'count': 4,
        'memories': {
            'favorite_language': 'Python',
            'favorite_programming_language': 'Python',
            'favorite_editor': 'VS Code',
            'learning_topic': 'AI agents'
        }
    }

The agent can then summarize the stored information for the user.

---

### 🌐 6. Web Search

The web search tool allows the agent to search the internet.

It uses DuckDuckGo search results and returns useful webpage titles and URLs.

Example:

    You: Search for Python programming language.

    Agent decided to use: web_search

    Arguments:
    {
        'query': 'Python programming language'
    }

    Tool result:
    {
        'success': True,
        'query': 'Python programming language',
        'results': [
            {
                'title': 'Welcome to Python.org',
                'url': 'https://www.python.org/'
            }
        ]
    }

The search tool also filters unwanted DuckDuckGo advertisement and redirect URLs so that the agent receives cleaner URLs.

---

### 📄 7. Fetch Webpage

The webpage fetcher downloads a webpage and extracts readable text from it.

This is important because a search result only gives the agent a URL.

The webpage fetcher allows the agent to actually read the webpage.

Example workflow:

    Search result
          ↓
    https://www.python.org/downloads/
          ↓
    Fetch webpage
          ↓
    Extract webpage text
          ↓
    Gemini reads the content

For example, the agent successfully fetched the official Python downloads page and extracted information such as:

    Download Python 3.14.7

---

# 🧠 AI Agent Architecture

The current agent architecture looks like this:

    USER
      │
      ▼
    GEMINI
      │
      │ Understand the request
      ▼
    Choose appropriate tool
      │
      ├───────────────┬────────────────┐
      │               │                │
      ▼               ▼                ▼
    Calculator    Text Analyzer      Memory
                                       │
                                  ┌────┼────┐
                                  │    │    │
                                  ▼    ▼    ▼
                              Remember Recall Get All

                           Web Research
                                │
                         ┌──────┴──────┐
                         │             │
                         ▼             ▼
                    Web Search    Fetch Webpage
                         │             │
                         └──────┬──────┘
                                ▼
                              Gemini
                                │
                                ▼
                          Final Answer

---

# 🔄 How Tool Calling Works

The agent uses Gemini's function-calling system.

The user sends a message.

Gemini decides whether a tool is needed.

If a tool is required, Gemini generates a function call.

Python receives the function call.

The Python application executes the requested function.

The result is sent back to Gemini.

Gemini then decides whether:

- Another tool is needed
- Or enough information is available to answer

Finally, Gemini produces the response.

The basic loop is:

    User
      ↓
    Gemini
      ↓
    Function Call
      ↓
    Python Tool
      ↓
    Tool Result
      ↓
    Gemini
      ↓
    Another Tool OR Final Answer

---

# 🔁 Multi-Tool Execution

The agent can use multiple tools for a single request.

For example:

    You:
    Analyze this text and then calculate the number
    of words multiplied by 10:

    AI agents can use tools.

Gemini can first call:

    analyze_text

Result:

    word_count = 5

Then Gemini can call:

    calculate_expression

with:

    5 * 10

Result:

    50

The final answer can contain both results.

This demonstrates sequential multi-tool execution.

---

# 🌍 Web Research Workflow

The web research workflow is designed to work like this:

    User asks a current question
              │
              ▼
            Gemini
              │
              ▼
         web_search
              │
              ▼
       Search results
              │
              ▼
      Select useful webpage
              │
              ▼
        fetch_webpage
              │
              ▼
      Read webpage content
              │
              ▼
            Gemini
              │
              ▼
         Final answer

Example:

    You:
    What is the latest Python version?

The agent can:

    1. Search the web
    2. Find an appropriate source
    3. Fetch the webpage
    4. Read the webpage
    5. Extract the relevant information
    6. Give the final answer

---

# 🛡️ Tool Call Safety

The agent has a maximum tool-call limit.

Current limit:

    max_tool_rounds = 5

This prevents the model from getting stuck in an endless tool loop.

Without a limit, an agent could potentially do:

    Gemini
      ↓
    Search
      ↓
    Gemini
      ↓
    Search
      ↓
    Gemini
      ↓
    Search
      ↓
    ...

The safety limit prevents this.

If the maximum number of tool calls is reached, the agent returns:

    I reached the maximum number of tool calls
    for this request. Please try asking the
    question more specifically.

---

# 📁 Project Structure

    My-first-AI-Agent/
    │
    ├── agent.py
    ├── agent_loop_gemini.py
    │
    ├── tools.py
    ├── text_tools.py
    ├── memory.py
    ├── tool_executor.py
    ├── web_search.py
    ├── fetch_webpage.py
    │
    ├── test_key.py
    ├── test_tool.py
    ├── test_text_tool.py
    ├── test_web_search.py
    ├── test_fetch_webpage.py
    │
    ├── memories.json
    ├── requirements.txt
    ├── .gitignore
    └── README.md

---

# 📌 File Responsibilities

## agent_loop_gemini.py

This is the main AI agent program.

It is responsible for:

- Connecting to Gemini
- Defining the tools
- Sending messages to Gemini
- Receiving function calls
- Executing tools
- Sending tool results back
- Continuing the agent loop
- Producing the final answer
- Limiting tool calls

---

## tool_executor.py

This is the central tool router.

It receives the function name selected by Gemini and executes the correct Python function.

Architecture:

    Gemini
       │
       ▼
    tool_executor.py
       │
       ├── calculate_expression
       ├── analyze_text
       ├── remember
       ├── recall
       ├── get_all_memories
       ├── web_search
       └── fetch_webpage

---

## tools.py

Contains the calculator tool.

Responsible for evaluating mathematical expressions.

---

## text_tools.py

Contains the text-analysis functionality.

Responsible for:

- Word counting
- Character counting

---

## memory.py

Contains the persistent memory system.

Responsible for:

- Saving memories
- Reading memories
- Recalling memories
- Returning all memories

---

## memories.json

Stores persistent memory data.

Example:

    {
        "favorite_programming_language": "Python",
        "favorite_editor": "VS Code",
        "learning_topic": "AI agents"
    }

---

## web_search.py

Contains the internet search functionality.

Responsible for:

- Searching DuckDuckGo
- Extracting search results
- Cleaning search result URLs
- Filtering advertisement/redirect URLs
- Returning useful results

---

## fetch_webpage.py

Contains webpage-fetching functionality.

Responsible for:

- Downloading webpages
- Handling HTTP requests
- Extracting HTML text
- Removing unnecessary page elements
- Limiting returned content
- Returning readable webpage content

---

## test_key.py

Tests whether the Gemini API key is available.

---

## test_tool.py

Tests the calculator functionality.

---

## test_text_tool.py

Tests the text analyzer.

---

## test_web_search.py

Tests the web search tool independently from the AI agent.

---

## test_fetch_webpage.py

Tests the webpage fetcher independently.

---

# 🛠️ Technologies

This project currently uses:

- Python
- Google Gemini API
- Google GenAI Python SDK
- DuckDuckGo
- Requests
- HTML parsing
- JSON
- Git
- GitHub

---

# 📦 Installation

## 1. Clone the Repository

    git clone https://github.com/sohail78692/My-first-AI-Agent.git

Enter the project directory:

    cd My-first-AI-Agent

---

## 2. Create a Virtual Environment

Windows:

    python -m venv venv

Activate it:

    venv\Scripts\activate

---

## 3. Install Dependencies

    pip install -r requirements.txt

If required:

    pip install google-genai requests

---

# 🔑 Gemini API Key

The agent requires a Gemini API key.

Set your API key as an environment variable.

Windows PowerShell:

    $env:GEMINI_API_KEY="YOUR_API_KEY"

Then test it:

    python test_key.py

Expected output:

    API key found!

---

# 🔐 Security

Never put your API key directly into your Python source code.

Do not commit:

    .env

or any file containing your API key.

Your .gitignore should contain entries such as:

    .env
    venv/
    __pycache__/
    *.pyc

If an API key is accidentally uploaded to GitHub:

1. Revoke the exposed key
2. Generate a new key
3. Update your local environment
4. Make sure the secret is ignored by Git

---

# ▶️ Running the Agent

Start the agent with:

    python agent_loop_gemini.py

Expected startup:

    API key found!

    AI Agent is ready!
    Available tools:
    - Calculator
    - Text Analyzer
    - Remember
    - Recall
    - Get All Memories
    - Web Search
    - Fetch Webpage

    Type 'exit' to stop.

---

# 🧪 Testing Individual Tools

## Test API Key

    python test_key.py

---

## Test Calculator

    python test_tool.py

---

## Test Text Analyzer

    python test_text_tool.py

---

## Test Web Search

    python test_web_search.py

Example:

    {
        'success': True,
        'query': 'Python programming language',
        'results': [
            {
                'title': 'Welcome to Python.org',
                'url': 'https://www.python.org/'
            }
        ]
    }

---

## Test Webpage Fetcher

    python test_fetch_webpage.py

Example:

    {
        'success': True,
        'url': 'https://www.python.org/downloads/latest/',
        'content': 'Python Release Python 3.14.7 ...',
        'character_count': 5023
    }

---

# 💬 Example Agent Session

    PS C:\Projects\my-first-ai-agent> python agent_loop_gemini.py

    API key found!

    AI Agent is ready!
    Available tools:
    - Calculator
    - Text Analyzer
    - Remember
    - Recall
    - Get All Memories
    - Web Search
    - Fetch Webpage

    Type 'exit' to stop.

    You: 21*12

    Agent decided to use: calculate_expression
    Arguments: {'expression': '21*12'}

    Tool result: 252

    Agent: 21 * 12 = 252

---

# 🧠 Memory Example

    You: Remember my favorite editor is VS Code.

    Agent decided to use: remember

    Arguments:
    {
        'key': 'favorite_editor',
        'value': 'VS Code'
    }

    Tool result:
    {
        'success': True,
        'key': 'favorite_editor',
        'value': 'VS Code'
    }

    Agent: I've remembered that your favorite editor is VS Code!

Then:

    You: What is my favorite editor?

    Agent decided to use: recall

    Tool result:
    {
        'found': True,
        'key': 'favorite_editor',
        'value': 'VS Code'
    }

    Agent: Your favorite editor is VS Code.

---

# 🌐 Web Search Example

    You: What is the latest Python version?

    Agent decided to use: web_search

    Arguments:
    {
        'query': 'latest Python release version official'
    }

    Tool result:
    ...

If search results are unavailable, the agent can use a known trustworthy URL:

    Agent decided to use: fetch_webpage

    Arguments:
    {
        'url': 'https://www.python.org/downloads/'
    }

The webpage is fetched and read.

The agent can then produce:

    Latest stable version: Python 3.14.7

    Pre-release/development version: Python 3.15

---

# 🔄 Agent Decision Process

The agent does not have one fixed workflow for every request.

Instead, Gemini decides what is necessary.

### Simple calculation

    User
      ↓
    Gemini
      ↓
    Calculator
      ↓
    Gemini
      ↓
    Answer

### Memory request

    User
      ↓
    Gemini
      ↓
    Remember
      ↓
    Gemini
      ↓
    Answer

### Memory lookup

    User
      ↓
    Gemini
      ↓
    Recall
      ↓
    Gemini
      ↓
    Answer

### Web research

    User
      ↓
    Gemini
      ↓
    Web Search
      ↓
    Fetch Webpage
      ↓
    Gemini
      ↓
    Answer

### Multi-tool request

    User
      ↓
    Gemini
      ↓
    Tool 1
      ↓
    Result
      ↓
    Gemini
      ↓
    Tool 2
      ↓
    Result
      ↓
    Gemini
      ↓
    Answer

---

# 📈 Project Development

## Phase 1 — Basic AI Agent

Completed:

- [x] Python project setup
- [x] Gemini API connection
- [x] API key handling
- [x] Basic agent loop
- [x] Calculator tool
- [x] Text analyzer tool
- [x] Gemini function calling

---

## Phase 2 — Memory

Completed:

- [x] Remember tool
- [x] Recall tool
- [x] Get All Memories tool
- [x] Persistent memory
- [x] JSON-based memory storage
- [x] Memory testing

---

## Phase 3 — Web Capabilities

Completed:

- [x] Web search
- [x] Search result extraction
- [x] Search URL cleaning
- [x] Advertisement/redirect filtering
- [x] Webpage fetching
- [x] HTML text extraction
- [x] Web research workflow

---

## Phase 4 — Agent Improvements

Completed:

- [x] Multiple tool calls
- [x] Sequential tool execution
- [x] Tool result handling
- [x] Tool call safety limit
- [x] Error handling
- [x] Search → Fetch → Answer workflow

---

# 🚧 Future Improvements

Possible future improvements include:

- [ ] Better web search ranking
- [ ] Better search snippets
- [ ] Better webpage parsing
- [ ] Better handling of JavaScript-heavy websites
- [ ] Source citations in final responses
- [ ] Automatic source selection
- [ ] Better tool error recovery
- [ ] Better memory management
- [ ] Update memory tool
- [ ] Delete memory tool
- [ ] Conversation history
- [ ] File reading
- [ ] PDF reading
- [ ] Document analysis
- [ ] Image analysis
- [ ] More external APIs
- [ ] Streaming responses
- [ ] Better agent planning
- [ ] Tool execution logging
- [ ] Automated tests
- [ ] Web interface
- [ ] Deployment
- [ ] Authentication
- [ ] Database-backed memory

---

# 🎯 Long-Term Goal

The long-term goal of this project is to build a more capable general-purpose AI agent from the ground up.

The planned architecture is:

    AI AGENT
        │
        ▼
    Gemini LLM
        │
    Agent Planning
        │
        ├────────────────┬────────────────┐
        │                │                │
        ▼                ▼                ▼
      Tools           Memory            Web
        │                │                │
        ▼                ▼                ▼
    Calculations     Persistent        Search
    Text Analysis    Storage           Fetch
    Files            Recall            Research
    APIs
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                    LLM Reasoning
                         │
                         ▼
                    Final Answer

The purpose is to understand each layer rather than relying completely on an existing agent framework.

---

# 📚 What This Project Teaches

This project provides hands-on experience with:

- Python programming
- API integration
- Environment variables
- Gemini API
- LLM function calling
- Tool definitions
- Tool execution
- Agent loops
- Multi-tool agents
- Sequential reasoning
- Persistent memory
- JSON storage
- Web search
- HTTP requests
- HTML parsing
- Webpage extraction
- Error handling
- API quotas
- Safety limits
- Git
- GitHub
- Software project structure

---

# ⚠️ Gemini API Quota

The Gemini API may have request limits depending on the account and model being used.

If you receive:

    429 RESOURCE_EXHAUSTED

the API quota has been exceeded.

Possible solutions:

- Wait for the quota to reset
- Reduce unnecessary tool calls
- Reduce repeated searches
- Check the Gemini API usage
- Check the API plan and limits

The agent's tool-call limit also helps reduce unnecessary API usage.

---

# 🧩 Design Philosophy

This project is intentionally being developed incrementally.

Each feature is built and tested independently before being integrated into the main agent.

The development process is:

    Build
      ↓
    Test
      ↓
    Integrate
      ↓
    Test again
      ↓
    Commit
      ↓
    Improve

This makes it easier to understand the architecture and recover if a future change introduces a problem.

---

# 📊 Current Agent

Current version:

    AI Agent v0.2

Current tools:

    1. Calculator
    2. Text Analyzer
    3. Remember
    4. Recall
    5. Get All Memories
    6. Web Search
    7. Fetch Webpage

Status:

    Working ✅
    Active Development 🚧

---

# 🏆 Current Milestone

The project has successfully reached a functional multi-tool AI agent.

The agent can now:

    Understand user request
            ↓
    Choose a tool
            ↓
    Execute the tool
            ↓
    Read the result
            ↓
    Decide whether another tool is needed
            ↓
    Generate final response

The web research capability adds another important agent behavior:

    Search
      ↓
    Find source
      ↓
    Read source
      ↓
    Reason over source
      ↓
    Answer

---

# 👨‍💻 Author

**Sohail**

GitHub:

https://github.com/sohail78692

Project Repository:

https://github.com/sohail78692/My-first-AI-Agent

---

# ⭐ Project Status

    ┌─────────────────────────────────────────┐
    │          MY FIRST AI AGENT              │
    ├─────────────────────────────────────────┤
    │                                         │
    │  Calculator             ✅              │
    │  Text Analyzer          ✅              │
    │  Remember               ✅              │
    │  Recall                 ✅              │
    │  Get All Memories       ✅              │
    │  Web Search             ✅              │
    │  Fetch Webpage          ✅              │
    │  Multi-tool reasoning   ✅              │
    │  Tool safety limit      ✅              │
    │                                         │
    │  Status: Active Development             │
    │  Version: v0.2                          │
    │                                         │
    └─────────────────────────────────────────┘

---

# ⭐ Final Note

This project is primarily a learning project focused on understanding the fundamentals of AI agents.

The goal is not simply to create a chatbot.

The goal is to understand how an AI agent can:

    Think
      ↓
    Choose
      ↓
    Use tools
      ↓
    Observe results
      ↓
    Use more tools when necessary
      ↓
    Reason
      ↓
    Answer

Every feature is being built step-by-step to understand the underlying architecture of modern AI agents.

---

## 🚀 Built with Python + Gemini

**My First AI Agent — Learning how AI agents work, one tool at a time.**
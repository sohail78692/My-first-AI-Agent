# 🤖 My First AI Agent

A beginner-friendly AI agent built with **Python** and **Google Gemini**.

This project was created to understand how AI agents actually work under the hood.

Instead of building a simple chatbot, this project gives an LLM access to multiple tools and allows it to decide:

- Which tool should be used
- When a tool should be used
- Whether another tool is needed
- When enough information has been collected
- When to return the final answer

The project is intentionally built step-by-step without relying completely on an existing agent framework.

---

## 🚀 Project Overview

The current agent can:

- 🧮 Perform mathematical calculations
- 📝 Analyze text
- 🧠 Store information in persistent memory
- 🔎 Recall specific memories
- 🗂️ Retrieve all stored memories
- 🌐 Search the web
- 📄 Fetch and read webpages
- 🔄 Execute multiple tools sequentially
- 🛡️ Limit tool calls to prevent infinite loops
- 💬 Maintain short-term conversation context
- 📜 Display recent conversation history
- 🧹 Clear short-term conversation history
- ⚠️ Handle tool errors
- 🔍 Perform web research using Search → Fetch → Answer

The agent uses **Gemini function calling** to decide which tool to execute.

---

# ✨ Features

## 🧮 1. Calculator

The calculator tool evaluates mathematical expressions.

### Example

```text
You: 21*12

Agent decided to use: calculate_expression

Arguments:
{
    'expression': '21*12'
}

Tool result:
252

Agent: 21 * 12 = 252
```

---

## 📝 2. Text Analyzer

The text analyzer can analyze text and return:

- Word count
- Character count

### Example

```text
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
```

---

# 🧠 3. Persistent Memory

The agent has a persistent memory system.

Information is stored in:

```text
memories.json
```

The agent can:

- Remember information
- Recall specific information
- Retrieve all stored memories

---

## 💾 Remember

Use the `remember` tool when the user explicitly asks the agent to remember something.

### Example

```text
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
```

---

## 🔎 Recall

The `recall` tool retrieves a specific memory.

### Example

```text
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
```

---

## 🗂️ Get All Memories

The `get_all_memories` tool retrieves all stored memories.

### Example

```text
You: What do you remember about me?

Agent decided to use: get_all_memories

Arguments:
{}

Tool result:
{
    'count': 3,
    'memories': {
        'favorite_programming_language': 'Python',
        'favorite_editor': 'VS Code',
        'learning_topic': 'AI agents'
    }
}
```

The agent can then summarize the stored information.

---

# 💬 4. Short-Term Conversation Memory

The agent also maintains short-term conversation context during the current session.

This is different from persistent memory.

### Example

```text
You: What is the latest Python version?

Agent: The latest stable version is Python 3.14.7.

You: When was it released?

Agent: Python 3.14.7 was released on August 5, 2026.
```

The agent understands that:

```text
"It"
```

refers to:

```text
Python 3.14.7
```

because that information exists in the recent conversation.

---

## 📜 `/history`

Use:

```text
/history
```

to display recent short-term conversation history.

Example:

```text
===== SHORT-TERM CONVERSATION HISTORY =====

Turn 1
You: What is the latest Python version?
Agent: The latest stable version is Python 3.14.7.

Turn 2
You: When was it released?
Agent: Python 3.14.7 was released on August 5, 2026.

============================================
```

---

## 🧹 `/clear`

Use:

```text
/clear
```

to clear the current short-term conversation context.

This does **not** delete persistent memories.

For example:

```text
You: /clear

Short-term conversation history cleared.
```

After clearing the conversation, an ambiguous question such as:

```text
You: When was it released?
```

will not cause the agent to guess using persistent memories.

Instead, it asks the user for clarification.

This keeps short-term conversation context and persistent memory properly separated.

---

# 🌐 5. Web Search

The web search tool allows the agent to search the internet.

The project currently uses DuckDuckGo search results.

The search tool returns:

- Page title
- URL
- Search results
- Cleaned URLs

It also filters unwanted advertisement and redirect URLs.

### Example

```text
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
```

---

# 📄 6. Fetch Webpage

Searching the web only gives the agent search results.

The `fetch_webpage` tool allows the agent to actually read the contents of a webpage.

The basic workflow is:

```text
Search
   ↓
Search Result
   ↓
Select Useful URL
   ↓
Fetch Webpage
   ↓
Extract Text
   ↓
Gemini Reads Content
   ↓
Final Answer
```

### Example

The agent can fetch:

```text
https://www.python.org/downloads/
```

and extract information such as:

```text
Download Python 3.14.7
```

This allows Gemini to answer questions using the actual webpage content instead of relying only on search-result titles.

---

# 🌍 Web Research Workflow

For current information, the agent can perform a multi-step research process.

Example:

```text
You:
What is the latest Python version?
```

The agent can:

```text
1. Search the web
        ↓
2. Find relevant sources
        ↓
3. Select a useful source
        ↓
4. Fetch the webpage
        ↓
5. Read the webpage content
        ↓
6. Extract the relevant information
        ↓
7. Answer the user
```

For example, the agent successfully used the official Python downloads page to determine:

```text
Latest stable version: Python 3.14.7
Pre-release/development version: Python 3.15
```

---

# 🛡️ Web Search Protection

The agent contains protection against unnecessary repeated web searches.

Once a useful webpage has been successfully fetched, the agent avoids repeatedly searching the same request.

This helps:

- Reduce unnecessary API calls
- Reduce Gemini quota usage
- Prevent repetitive search loops
- Make the research workflow more efficient

The intended workflow is:

```text
Web Search
    ↓
Find Source
    ↓
Fetch Webpage
    ↓
Use Fetched Content
    ↓
Final Answer
```

Instead of:

```text
Search
 ↓
Search
 ↓
Search
 ↓
Search
 ↓
Search
```

---

# 🔄 Multi-Tool Execution

The agent can use multiple tools for a single request.

For example:

```text
You:
Analyze this text and then calculate the number
of words multiplied by 10:

AI agents can use tools.
```

Gemini can first call:

```text
analyze_text
```

Result:

```text
word_count = 5
```

Then Gemini can call:

```text
calculate_expression
```

with:

```text
5 * 10
```

Result:

```text
50
```

The final answer can contain both results.

This demonstrates sequential multi-tool execution.

---

# 🧠 AI Agent Architecture

The current architecture looks like this:

```text
                    USER
                      │
                      ▼
                   GEMINI
                      │
                      ▼
              Understand Request
                      │
                      ▼
               Choose Tool
                      │
       ┌──────────────┼───────────────┐
       │              │               │
       ▼              ▼               ▼
   Calculator    Text Analyzer     Memory
                                      │
                              ┌───────┼────────┐
                              │       │        │
                              ▼       ▼        ▼
                          Remember  Recall  Get All
                                               Memories

                      Web Research
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
                Web Search   Fetch Webpage
                    │             │
                    └──────┬──────┘
                           ▼
                         GEMINI
                           │
                           ▼
                      Final Answer
```

---

# 🔄 How Tool Calling Works

The agent uses Gemini's function-calling system.

The basic process is:

```text
User
  ↓
Gemini
  ↓
Function Call
  ↓
Python
  ↓
Tool Execution
  ↓
Tool Result
  ↓
Gemini
  ↓
Another Tool OR Final Answer
```

More specifically:

1. The user sends a request.
2. Gemini analyzes the request.
3. Gemini decides whether a tool is needed.
4. Gemini generates a function call.
5. Python receives the function call.
6. Python executes the requested tool.
7. The result is sent back to Gemini.
8. Gemini decides whether another tool is required.
9. If necessary, another tool is executed.
10. Once enough information is available, Gemini generates the final answer.

---

# 🧩 Tool Execution Architecture

The project uses a central tool router.

```text
                     GEMINI
                        │
                        ▼
                Function Call
                        │
                        ▼
                tool_executor.py
                        │
       ┌────────────────┼─────────────────┐
       │                │                 │
       ▼                ▼                 ▼
calculate_expression  analyze_text      Memory
                                          │
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                           remember    recall    get_all_memories

                        Web Research
                              │
                       ┌──────┴──────┐
                       ▼             ▼
                   web_search   fetch_webpage
```

---

# 🛡️ Tool Call Safety

The agent has a maximum tool-call limit.

Current limit:

```python
max_tool_rounds = 5
```

This prevents the model from getting stuck in an endless tool loop.

Without a limit, an agent could potentially do:

```text
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
```

The safety limit prevents this.

If the maximum number of tool calls is reached, the agent returns:

```text
I reached the maximum number of tool calls
for this request. Please try asking the
question more specifically.
```

---

# 🧠 Memory Safety

The project separates two types of memory.

## Short-Term Memory

Used for:

- Current conversation
- Follow-up questions
- References such as "it" or "that"
- Recent context

Controlled with:

```text
/history
/clear
```

---

## Persistent Memory

Stored in:

```text
memories.json
```

Used for information that the user explicitly asks the agent to remember.

Examples:

```text
Remember my favorite editor is VS Code.
```

or:

```text
What is my favorite editor?
```

The agent should not use persistent memory just to guess what an ambiguous question refers to.

---

# 📁 Project Structure

```text
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
```

---

# 📌 File Responsibilities

## `agent_loop_gemini.py`

Main AI agent program.

Responsible for:

- Connecting to Gemini
- Defining Gemini tools
- Sending messages to Gemini
- Receiving function calls
- Executing tools
- Sending tool results back
- Continuing the agent loop
- Maintaining short-term conversation context
- Handling `/history`
- Handling `/clear`
- Limiting tool calls
- Producing final answers

---

## `tool_executor.py`

Central tool router.

It receives the function name selected by Gemini and executes the correct Python function.

It connects Gemini's function calls to the actual Python tools.

---

## `tools.py`

Contains the calculator functionality.

Responsible for evaluating mathematical expressions.

---

## `text_tools.py`

Contains the text-analysis functionality.

Responsible for:

- Word counting
- Character counting

---

## `memory.py`

Contains the persistent memory system.

Responsible for:

- Saving memories
- Reading memories
- Recalling memories
- Returning all memories

---

## `memories.json`

Stores persistent memory data.

Example:

```json
{
    "favorite_programming_language": "Python",
    "favorite_editor": "VS Code",
    "learning_topic": "AI agents"
}
```

---

## `web_search.py`

Contains the internet search functionality.

Responsible for:

- Searching DuckDuckGo
- Extracting search results
- Cleaning search result URLs
- Filtering advertisement/redirect URLs
- Returning useful results

---

## `fetch_webpage.py`

Contains webpage-fetching functionality.

Responsible for:

- Downloading webpages
- Handling HTTP requests
- Extracting HTML text
- Removing unnecessary page elements
- Limiting returned content
- Returning readable webpage content

---

## `test_key.py`

Tests whether the Gemini API key is available.

---

## `test_tool.py`

Tests the calculator functionality independently.

---

## `test_text_tool.py`

Tests the text analyzer independently.

---

## `test_web_search.py`

Tests the web search functionality independently from the AI agent.

---

## `test_fetch_webpage.py`

Tests the webpage fetcher independently from the AI agent.

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

```bash
git clone https://github.com/sohail78692/My-first-AI-Agent.git
```

Enter the project directory:

```bash
cd My-first-AI-Agent
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If required:

```bash
pip install google-genai requests
```

---

# 🔑 Gemini API Key

The agent requires a Gemini API key.

Set the API key as an environment variable.

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Then test it:

```powershell
python test_key.py
```

Expected output:

```text
API key found!
```

---

# 🔐 Security

Never put your API key directly inside your Python source code.

Do not commit:

```text
.env
```

or any file containing your API key.

Your `.gitignore` should contain entries such as:

```text
.env
venv/
__pycache__/
*.pyc
```

If an API key is accidentally uploaded to GitHub:

1. Revoke the exposed key
2. Generate a new key
3. Update your local environment
4. Make sure the secret is ignored by Git

---

# ▶️ Running the Agent

Start the agent with:

```powershell
python agent_loop_gemini.py
```

Expected startup:

```text
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

Special commands:
- /history  → Show recent conversation
- /clear    → Clear short-term conversation
- exit      → Stop the agent

Type 'exit' to stop.
```

---

# ⌨️ Special Commands

## `/history`

Show recent short-term conversation history.

```text
/history
```

---

## `/clear`

Clear short-term conversation context.

```text
/clear
```

Persistent memories remain intact.

---

## `exit`

Stop the agent.

```text
exit
```

---

# 🧪 Testing Individual Tools

## Test API Key

```bash
python test_key.py
```

---

## Test Calculator

```bash
python test_tool.py
```

---

## Test Text Analyzer

```bash
python test_text_tool.py
```

---

## Test Web Search

```bash
python test_web_search.py
```

Example:

```text
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
```

---

## Test Webpage Fetcher

```bash
python test_fetch_webpage.py
```

Example:

```text
{
    'success': True,
    'url': 'https://www.python.org/downloads/latest/',
    'content': 'Python Release Python 3.14.7 ...',
    'character_count': 5023
}
```

---

# 💬 Example Agent Session

```text
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

Special commands:
- /history  → Show recent conversation
- /clear    → Clear short-term conversation
- exit      → Stop the agent

Type 'exit' to stop.

You: 21*12

Agent decided to use: calculate_expression
Arguments: {'expression': '21*12'}

Tool result: 252

Agent: 21 * 12 = 252
```

---

# 🧠 Memory Example

```text
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
```

Then:

```text
You: What is my favorite editor?

Agent decided to use: recall

Arguments:
{
    'key': 'favorite_editor'
}

Tool result:
{
    'found': True,
    'key': 'favorite_editor',
    'value': 'VS Code'
}

Agent: Your favorite editor is VS Code.
```

---

# 🌐 Web Research Example

```text
You: What is the latest Python version?
```

The agent can perform:

```text
web_search
     ↓
Find Python.org
     ↓
fetch_webpage
     ↓
Read Python downloads page
     ↓
Gemini analyzes the content
     ↓
Final answer
```

Example result:

```text
The latest stable version of Python is Python 3.14.7.
```

The agent can also answer a follow-up using short-term context:

```text
You: When was it released?

Agent: Python 3.14.7 was released on August 5, 2026.
```

---

# 🔄 Agent Decision Process

The agent does not use one fixed workflow for every request.

Gemini decides what is necessary based on the user's request.

## Simple Calculation

```text
User
  ↓
Gemini
  ↓
Calculator
  ↓
Gemini
  ↓
Answer
```

---

## Memory Request

```text
User
  ↓
Gemini
  ↓
Remember
  ↓
Gemini
  ↓
Answer
```

---

## Memory Lookup

```text
User
  ↓
Gemini
  ↓
Recall
  ↓
Gemini
  ↓
Answer
```

---

## Web Research

```text
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
```

---

## Multi-Tool Request

```text
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
```

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

## Phase 2 — Persistent Memory

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
- [x] Search → Fetch → Answer workflow

---

## Phase 4 — Agent Improvements

Completed:

- [x] Multiple tool calls
- [x] Sequential tool execution
- [x] Tool result handling
- [x] Tool call safety limit
- [x] Error handling
- [x] Web search protection
- [x] Short-term conversation history
- [x] `/history` command
- [x] `/clear` command
- [x] Follow-up question handling
- [x] Separation of short-term and persistent memory
- [x] Ambiguous-reference handling

---

# 🚧 Future Improvements

This project is currently stopped at this milestone.

Possible future improvements include:

- [ ] Better web search ranking
- [ ] Better search snippets
- [ ] Better webpage parsing
- [ ] Better handling of JavaScript-heavy websites
- [ ] Source citations in final responses
- [ ] Better tool error recovery
- [ ] Better memory management
- [ ] Update memory tool
- [ ] Delete memory tool
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

These are **future possibilities**, not features currently required by the finished milestone.

---

# 🎯 Long-Term Goal

The long-term goal is to build a more capable general-purpose AI agent from the ground up.

The planned architecture is:

```text
                    AI AGENT
                        │
                        ▼
                    Gemini LLM
                        │
                        ▼
                  Agent Planning
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
        Tools         Memory         Web
          │             │             │
          ▼             ▼             ▼
    Calculations    Persistent      Search
    Text Analysis   Storage         Fetch
    Files           Recall          Research
    APIs
          │             │             │
          └─────────────┼─────────────┘
                        │
                        ▼
                  LLM Reasoning
                        │
                        ▼
                   Final Answer
```

The purpose is to understand each layer rather than simply relying on an existing agent framework.

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
- Sequential tool execution
- Persistent memory
- Short-term conversation memory
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

```text
429 RESOURCE_EXHAUSTED
```

the API quota has been exceeded.

Possible solutions:

- Wait for the quota to reset
- Reduce unnecessary tool calls
- Reduce repeated searches
- Check Gemini API usage
- Check the API plan and limits

The agent's tool-call safety limit and web-search protection help reduce unnecessary API usage.

---

# 🧩 Design Philosophy

This project was intentionally developed incrementally.

Each feature was built and tested independently before being integrated into the main agent.

The development process is:

```text
Build
  ↓
Test
  ↓
Integrate
  ↓
Test Again
  ↓
Commit
  ↓
Improve
```

This approach makes it easier to:

- Understand the architecture
- Debug individual features
- Isolate problems
- Recover from failed changes
- Keep a working Git checkpoint

---

# 📊 Current Agent

## Version

```text
AI Agent v0.2
```

## Current Tools

```text
1. Calculator
2. Text Analyzer
3. Remember
4. Recall
5. Get All Memories
6. Web Search
7. Fetch Webpage
```

## Conversation Features

```text
8. Short-Term Conversation History
9. /history
10. /clear
```

## Status

```text
Working ✅
Milestone Complete ✅
Development Paused 🛑
```

---

# 🏆 Current Milestone

The project has successfully reached a functional multi-tool AI agent.

The current agent can:

```text
Understand User Request
        ↓
Choose Appropriate Tool
        ↓
Execute Tool
        ↓
Read Tool Result
        ↓
Decide Whether Another Tool Is Needed
        ↓
Generate Final Response
```

The web research capability adds:

```text
Search
  ↓
Find Source
  ↓
Fetch Source
  ↓
Read Source
  ↓
Reason Over Source
  ↓
Answer
```

The memory system adds:

```text
Remember
   ↓
Persistent Storage
   ↓
Recall
```

The conversation system adds:

```text
Conversation
   ↓
Short-Term Context
   ↓
Follow-Up Understanding
```

---

# 🏁 Project Milestone

At this stage, the project has achieved its original learning goal:

> Build a working AI agent that can reason about a user's request, choose tools, execute those tools, observe the results, use multiple tools when necessary, maintain memory, perform web research, and generate a final response.

The project is intentionally being paused here as a completed learning milestone.

---

# 👨‍💻 Author

**Sohail**

GitHub:

https://github.com/sohail78692

Project Repository:

https://github.com/sohail78692/My-first-AI-Agent

---

# ⭐ Project Status

```text
┌─────────────────────────────────────────────┐
│              MY FIRST AI AGENT              │
├─────────────────────────────────────────────┤
│                                             │
│  Calculator                 ✅              │
│  Text Analyzer              ✅              │
│  Remember                    ✅              │
│  Recall                      ✅              │
│  Get All Memories            ✅              │
│  Web Search                  ✅              │
│  Fetch Webpage               ✅              │
│  Multi-tool execution        ✅              │
│  Sequential tool calls       ✅              │
│  Tool safety limit           ✅              │
│  Web search protection       ✅              │
│  Short-term conversation     ✅              │
│  /history                    ✅              │
│  /clear                      ✅              │
│  Memory separation           ✅              │
│                                             │
│  Version: v0.2                              │
│  Status: Milestone Complete                 │
│  Development: Paused                        │
│                                             │
└─────────────────────────────────────────────┘
```

---

# ⭐ Final Note

This project is primarily a learning project focused on understanding the fundamentals of AI agents.

The goal was not simply to create a chatbot.

The goal was to understand how an AI agent can:

```text
Think
  ↓
Choose
  ↓
Use Tools
  ↓
Observe Results
  ↓
Use More Tools When Necessary
  ↓
Maintain Memory
  ↓
Reason
  ↓
Answer
```

Every major feature was built step-by-step to understand the underlying architecture of modern AI agents.

This project represents a practical first step toward building more advanced AI systems.

---

## 🚀 Built with Python + Gemini

**My First AI Agent**

*Learning how AI agents work, one tool at a time.*
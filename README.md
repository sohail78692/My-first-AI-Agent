# 🤖 My First AI Agent

A beginner-friendly AI agent built with **Python** and the **Google Gemini API**.

This project is my hands-on journey into understanding how AI agents work from the ground up. Instead of immediately relying on frameworks such as LangChain or LangGraph, I am first building the core agent architecture myself.

The project started as a simple Gemini API experiment and has gradually evolved into a **multi-tool AI agent with sequential tool calling, conversation context, and persistent memory**.

---

# 🚀 Project Overview

The goal of this project is to understand the fundamental architecture behind AI agents.

The agent can:

- 🧠 Understand a user's request
- 🔧 Decide whether a tool is needed
- 🎯 Select the appropriate tool
- 📦 Generate arguments for the selected tool
- ⚙️ Execute Python tools
- 👀 Receive tool results
- 🧠 Reason over tool results
- 🔄 Use multiple tools sequentially
- 💬 Maintain short-term conversation context
- 💾 Store information in persistent memory
- 🔎 Retrieve previously stored information
- 💬 Generate a final natural-language response

## Current Agent Flow

```text
User
 ↓
Gemini AI
 ↓
Decides what to do
 ↓
Selects Tool
 ↓
Tool Executor
 ↓
Python Tool
 ↓
Tool Result
 ↓
Gemini AI
 ↓
Another Tool Needed?
 ├── YES → Execute another tool
 └── NO  → Final Answer
```

---

# ✨ Features

## 🧠 Gemini-Powered AI Agent

Google Gemini acts as the AI brain and decision-making component of the project.

The model receives the user's request and decides whether it needs to use one of the available tools.

The Python application provides the tools, but Gemini decides which tool should be used.

---

# 🔧 Multi-Tool Support

The agent currently has **four tools**:

1. 🧮 Calculator
2. 📝 Text Analyzer
3. 🧠 Remember
4. 🔎 Recall

---

# 🧮 1. Calculator Tool

The calculator tool evaluates mathematical expressions.

Examples:

```text
21*12
454-12+22
2+2*4
(10+5)*3
100/5+20
```

The calculator supports:

- Addition
- Subtraction
- Multiplication
- Division
- Power
- Modulo
- Parentheses
- Negative numbers
- Operator precedence

## Example

```text
You: 21*12

Agent decided to use: calculate_expression
Arguments: {'expression': '21*12'}

Tool result: 252

Agent: 21 * 12 = 252
```

The calculator uses Python's `ast` module to safely evaluate supported mathematical expressions instead of directly using `eval()` on user input.

---

# 📝 2. Text Analyzer Tool

The text analyzer provides basic information about a piece of text.

Currently it calculates:

- Word count
- Character count

## Example

```text
You: Analyze this text: AI agents can use multiple tools.

Agent decided to use: analyze_text
Arguments: {'text': 'AI agents can use multiple tools.'}

Tool result:
{'word_count': 6, 'character_count': 33}
```

Gemini then receives the result and generates a natural-language response.

---

# 🧠 3. Remember Tool

The `remember` tool allows the AI agent to store useful information in persistent memory.

The information is stored locally in:

```text
memory.json
```

## Example

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
    'message': 'Remembered favorite_programming_language.'
}

Agent: I've remembered that your favorite programming language is Python!
```

The memory is saved to the local `memory.json` file.

---

# 🔎 4. Recall Tool

The `recall` tool retrieves previously stored information from persistent memory.

## Example

```text
You: What is my favorite programming language?

Agent decided to use: recall

Tool result:
{
    'found': True,
    'key': 'favorite_programming_language',
    'value': 'Python'
}

Agent: Your favorite programming language is Python.
```

The important part is that the information can still be retrieved after restarting the program.

---

# 🔄 Sequential Tool Calls

The agent can use multiple tools for a single user request.

For example:

```text
Analyze this text and then calculate the number of words multiplied by 10:
AI agents can use tools.
```

The agent performs:

```text
User Request
     ↓
Gemini
     ↓
analyze_text
     ↓
Word count = 5
     ↓
Tool result sent back to Gemini
     ↓
Gemini reasons again
     ↓
calculate_expression
     ↓
5 × 10 = 50
     ↓
Gemini
     ↓
Final Answer
```

Actual tool execution:

```text
Agent decided to use: analyze_text
Arguments:
{'text': 'AI agents can use tools.'}

Tool result:
{'word_count': 5, 'character_count': 24}

Agent decided to use: calculate_expression
Arguments:
{'expression': '5 * 10'}

Tool result:
50
```

This demonstrates the core agentic workflow:

```text
Think
 ↓
Act
 ↓
Observe
 ↓
Think Again
 ↓
Act Again
 ↓
Observe
 ↓
Final Answer
```

---

# 🔁 Reusable Agent Loop

The project includes a reusable agent loop in:

```text
agent_loop_gemini.py
```

The loop allows Gemini to repeatedly decide whether another tool call is necessary.

Conceptually:

```text
User
 ↓
Gemini
 ↓
Tool call?
 ├── NO → Final Answer
 │
 └── YES
      ↓
   Execute Tool
      ↓
   Tool Result
      ↓
   Gemini
      ↓
   Tool call?
      ├── YES → Execute again
      └── NO → Final Answer
```

This is an important difference between a simple chatbot and an AI agent.

A simple chatbot may work like:

```text
User → AI → Answer
```

Our agent can work like:

```text
User
 ↓
AI
 ↓
Action
 ↓
Observation
 ↓
AI
 ↓
Another Action
 ↓
Observation
 ↓
AI
 ↓
Final Answer
```

---

# 🧩 Central Tool Executor

The project uses a centralized:

```text
tool_executor.py
```

file.

Instead of placing every tool's implementation directly inside the agent, the agent sends the requested tool to the central executor.

Architecture:

```text
Gemini
 ↓
Function Call
 ↓
tool_executor.py
 ↓
Select Requested Tool
 ↓
Execute Python Function
 ↓
Return Result
```

Current structure:

```text
                 Gemini
                    │
               Tool Call
                    │
                    ▼
            ┌───────────────┐
            │ Tool Executor │
            └───────┬───────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   Calculator    Text        Memory
                 Analyzer     Tools
                              │
                         ┌────┴────┐
                         ▼         ▼
                     remember    recall
```

This architecture makes it easier to add additional tools in the future.

Possible future tools include:

```text
Web Search
File Reader
Weather
Database
Email
Calendar
Code Executor
Document Analyzer
```

---

# 💬 Short-Term Conversation Memory

The agent maintains **short-term conversation context** during an active session.

For example:

```text
You: My name is Sohail.

Agent: Nice to meet you, Sohail!

You: What is my name?

Agent: Your name is Sohail.
```

This works because the same Gemini chat session is maintained while the program is running.

## Current limitation

Short-term conversation context only exists during the active program session.

If the program is closed:

```text
Program Running
 ↓
Conversation History
 ↓
Program Closes
 ↓
Conversation Context Is Lost
```

For information that needs to survive a restart, the project now uses persistent memory.

---

# 💾 Persistent Memory

The agent can store and retrieve information even after the program is closed and restarted.

Persistent memory is currently implemented using a local JSON file:

```text
memory.json
```

The two memory tools are:

```text
remember
recall
```

## Persistent Memory Flow

```text
User
 ↓
Gemini
 ↓
remember
 ↓
memory.py
 ↓
memory.json
```

Later:

```text
User
 ↓
Gemini
 ↓
recall
 ↓
memory.py
 ↓
memory.json
 ↓
Stored Information
 ↓
Gemini
 ↓
Final Answer
```

## Persistence Test

The system has been tested by:

```text
Session 1
 ↓
Remember information
 ↓
Save to memory.json
 ↓
Close program
 ↓
Restart program
 ↓
Ask about stored information
 ↓
recall
 ↓
Information recovered
```

This confirms that the memory survives a program restart.

---

# 🏗️ Current Architecture

```text
                    ┌───────────────┐
                    │     USER      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   GEMINI AI   │
                    │  Agent Brain  │
                    └───────┬───────┘
                            │
                     Tool Selection
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌────────────────┐   ┌───────────────┐
│  Calculator   │   │ Text Analyzer  │   │    Memory     │
└───────┬───────┘   └───────┬────────┘   └───────┬───────┘
        │                   │                    │
        │                   │              ┌─────┴─────┐
        │                   │              ▼           ▼
        │                   │          remember      recall
        │                   │              │           │
        │                   │              └─────┬─────┘
        │                   │                    ▼
        │                   │              memory.json
        │                   │
        └───────────────────┼────────────────────┘
                            ▼
                    ┌───────────────┐
                    │ Tool Executor │
                    └───────┬───────┘
                            │
                            ▼
                       Tool Result
                            │
                            ▼
                    ┌───────────────┐
                    │   GEMINI AI   │
                    │  Re-evaluate  │
                    └───────┬───────┘
                            │
                   Another Tool Needed?
                       /           \
                     YES            NO
                      │              │
                      ▼              ▼
                 Execute Tool    Final Answer
                      │
                      └──────────────┐
                                     │
                                     ▼
                                  Gemini
```

---

# 📁 Project Structure

```text
My-first-AI-Agent/
│
├── agent.py
├── agent_loop.py
├── agent_loop_gemini.py
│
├── tools.py
├── text_tools.py
├── tool_executor.py
├── memory.py
│
├── test_key.py
├── test_tool.py
├── test_text_tool.py
├── test_tool_executor.py
├── test_memory.py
│
├── .gitignore
├── README.md
└── LICENSE
```

## File Descriptions

| File | Description |
|---|---|
| `agent.py` | Original multi-tool agent |
| `agent_loop.py` | Local simulated agent-loop experiment |
| `agent_loop_gemini.py` | Gemini-powered reusable agent loop |
| `tools.py` | Safe mathematical expression calculator |
| `text_tools.py` | Text analysis tool |
| `tool_executor.py` | Central tool execution layer |
| `memory.py` | Persistent memory functions |
| `test_key.py` | Tests Gemini API connectivity |
| `test_tool.py` | Tests calculator functionality |
| `test_text_tool.py` | Tests text analyzer functionality |
| `test_tool_executor.py` | Tests the centralized tool executor |
| `test_memory.py` | Tests persistent memory |
| `.gitignore` | Prevents unwanted files and secrets from being committed |
| `README.md` | Project documentation |
| `LICENSE` | MIT License |

---

# 🛠️ Technologies Used

- **Python**
- **Google Gemini API**
- **Google GenAI Python SDK**
- **JSON**
- **Git**
- **GitHub**

---

# ⚙️ Requirements

Before running the project, make sure you have:

- Python 3.10 or newer
- A Google account
- A Gemini API key
- Internet connection
- Git

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/sohail78692/My-first-AI-Agent.git
```

Move into the project directory:

```bash
cd My-first-AI-Agent
```

---

## 2. Install Dependencies

Install the Google GenAI SDK:

```bash
pip install google-genai
```

---

# 🔑 API Key Setup

The project uses the environment variable:

```text
GEMINI_API_KEY
```

The API key is intentionally kept outside the Python source code.

The code reads the API key using:

```python
import os

api_key = os.getenv("GEMINI_API_KEY")
```

## Windows CMD

```cmd
setx GEMINI_API_KEY "YOUR_API_KEY"
```

After using `setx`, restart your terminal.

## Windows PowerShell

For the current PowerShell session:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

> ⚠️ Never put your real API key directly into the source code.

> ⚠️ Never commit your API key to GitHub.

---

# ▶️ Running the Agent

The main Gemini-powered agent loop can be started with:

```bash
python agent_loop_gemini.py
```

You should see:

```text
API key found!

AI Agent is ready!

Available tools:
- Calculator
- Text Analyzer
- Remember
- Recall

Type 'exit' to stop.

You:
```

---

# 🧪 Example Usage

## Calculator

```text
You: 21*12

Agent decided to use: calculate_expression
Arguments: {'expression': '21*12'}

Tool result: 252

Agent: 21 * 12 = 252
```

---

## Text Analyzer

```text
You: Analyze this text: AI agents can use multiple tools.

Agent decided to use: analyze_text
Arguments: {'text': 'AI agents can use multiple tools.'}

Tool result:
{'word_count': 6, 'character_count': 33}

Agent: Here is the analysis of the text:

- Word count: 6
- Character count: 33
```

---

## Remember

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
    'message': 'Remembered favorite_programming_language.'
}

Agent: I've remembered that your favorite programming language is Python!
```

---

## Recall

```text
You: What is my favorite programming language?

Agent decided to use: recall

Tool result:
{
    'found': True,
    'key': 'favorite_programming_language',
    'value': 'Python'
}

Agent: Your favorite programming language is Python.
```

---

## Multiple Tool Calls

```text
You: Analyze this text and then calculate the number of words multiplied by 10: AI agents can use tools.

Agent decided to use: analyze_text

Tool result:
{'word_count': 5, 'character_count': 24}

Agent decided to use: calculate_expression

Arguments:
{'expression': '5 * 10'}

Tool result:
50
```

The agent then generates a final response using both tool results.

---

# 🧪 Testing Individual Components

## Test Gemini API

Run:

```bash
python test_key.py
```

Expected output:

```text
API key found!
Gemini response:
...
```

---

## Test Calculator

Run:

```bash
python test_tool.py
```

Expected result:

```text
Expression: 21*12
Result: 252
```

---

## Test Text Analyzer

Run:

```bash
python test_text_tool.py
```

Expected result:

```text
{'word_count': 5, 'character_count': 24}
```

---

## Test Tool Executor

Run:

```bash
python test_tool_executor.py
```

This verifies that the central tool executor can correctly route requests to the appropriate Python tools.

---

## Test Persistent Memory

Run:

```bash
python test_memory.py
```

This verifies that information can be saved and retrieved using the persistent memory system.

---

# 🔐 Security

API keys and other secrets should never be committed to this repository.

The project uses:

```text
GEMINI_API_KEY
```

as an environment variable.

The `.gitignore` file includes:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
memory.json
```

`memory.json` is excluded because it may contain user-specific information.

## If an API Key Is Accidentally Exposed

If a real API key is accidentally pushed to GitHub:

1. Revoke the exposed API key.
2. Create a new API key.
3. Update the environment variable.
4. Make sure the new key is not committed.
5. Remove the exposed secret from the repository history if necessary.

---

# 📚 What I Am Learning

This project is being developed as a practical way to understand AI agents.

Topics explored so far:

- AI agents
- Large Language Models
- Gemini API
- Prompting
- Function calling
- Tool calling
- Tool selection
- Tool execution
- Multiple tools
- Tool executors
- Agent loops
- Sequential tool calls
- Conversation state
- Persistent memory
- Memory retrieval
- JSON-based storage
- API integration
- API error handling
- API rate limits
- Environment variables
- API-key security
- Python AI applications
- Git
- GitHub

---

# 🗺️ Roadmap

## ✅ Completed

- [x] Set up Python environment
- [x] Connect Python to Gemini
- [x] Create first AI-powered program
- [x] Create first Python tool
- [x] Implement Gemini tool calling
- [x] Execute tool results
- [x] Send tool results back to Gemini
- [x] Create continuous agent conversation
- [x] Build a safe mathematical expression calculator
- [x] Support mathematical operator precedence
- [x] Add a text analysis tool
- [x] Add multiple-tool support
- [x] Create centralized tool executor
- [x] Build reusable agent loop
- [x] Connect reusable agent loop to Gemini
- [x] Support sequential tool calls
- [x] Test short-term conversation memory
- [x] Add persistent memory
- [x] Create `remember` memory tool
- [x] Create `recall` memory tool
- [x] Store memory in JSON
- [x] Retrieve memory after restarting the program
- [x] Exclude `memory.json` from GitHub
- [x] Push project to GitHub

---

## 🔨 Next Steps

- [ ] Improve persistent memory structure
- [ ] Support multiple stored memories
- [ ] Improve memory search and retrieval
- [ ] Add memory categories
- [ ] Add better memory management
- [ ] Improve agent error handling
- [ ] Add more useful tools
- [ ] Add web search
- [ ] Add document reading
- [ ] Add file-processing capabilities
- [ ] Learn Retrieval-Augmented Generation (RAG)
- [ ] Explore LangChain
- [ ] Explore LangGraph
- [ ] Build a more autonomous multi-tool agent
- [ ] Build a real-world AI agent
- [ ] Build an AI agent suitable for a hackathon
- [ ] Prepare for HackerRank Orchestrate
- [ ] Participate in HackerRank Orchestrate

---

# 🎯 Learning Goal

The goal of this project is not simply to build another chatbot.

The main goal is to understand how AI agents work internally.

The target architecture is:

```text
User Goal
    ↓
AI Reasoning
    ↓
Tool Selection
    ↓
Tool Execution
    ↓
Tool Result
    ↓
Further Reasoning
    ↓
Another Action?
    ↓
Tool Execution
    ↓
Further Reasoning
    ↓
Memory
    ↓
Final Answer
```

The project is intentionally being built from the fundamentals before moving to higher-level AI-agent frameworks.

---

# 🧠 Why Build From Scratch?

This project intentionally starts without an agent framework.

The purpose is to understand the fundamentals before using higher-level frameworks such as LangChain or LangGraph.

Instead of immediately writing:

```text
Framework
   ↓
Agent
```

the project first explores:

```text
LLM
 ↓
Tool Definition
 ↓
Function Call
 ↓
Tool Execution
 ↓
Tool Result
 ↓
Agent Loop
 ↓
Conversation Context
 ↓
Persistent Memory
```

Once these concepts are understood, frameworks such as LangChain and LangGraph will be easier to understand.

---

# 🚧 Project Status

**Status: Active Development 🚀**

This project started as a beginner experiment to understand how AI agents work.

It has now evolved into a working multi-tool agent capable of:

- Calling Gemini
- Selecting tools
- Executing Python functions
- Using multiple tools
- Performing sequential tool calls
- Maintaining short-term conversation context
- Storing persistent information
- Retrieving persistent information
- Surviving program restarts
- Generating final responses

The architecture and features will continue to evolve as new AI-agent concepts are learned and implemented.

---

# 🤝 Contributions

This is primarily a personal learning project, but suggestions, improvements, and ideas are welcome.

If you find a bug or have an idea for improving the agent, feel free to:

- Open an issue
- Submit a pull request
- Suggest a new tool
- Suggest an architecture improvement

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for the complete license text.

---

# 👨‍💻 Author

**Sohail**

GitHub:

https://github.com/sohail78692/My-first-AI-Agent

---

# ⭐ Project Goal

From:

> **"I have never built an AI agent."**

To:

> **"I understand how AI agents work and can build a multi-tool AI agent."**

🚀 **Learning by building.**
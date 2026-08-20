# 🤖 My First AI Agent

A beginner-friendly AI agent built with **Python** and **Google Gemini**.

This project is my hands-on journey into understanding how AI agents work from the ground up. Instead of immediately using frameworks like LangChain or LangGraph, I am first building the core agent architecture myself.

The project will gradually evolve from a simple tool-using agent into a more advanced multi-tool AI agent.

---

## 🚀 Project Overview

This project demonstrates how an AI agent can:

* Understand a user's request
* Decide when a tool is needed
* Select an appropriate tool
* Send arguments to the tool
* Execute the tool using Python
* Receive the tool result
* Send the result back to the AI
* Generate a final response

### Current Agent Flow

```text
User
 ↓
Gemini AI
 ↓
Decides whether a tool is needed
 ↓
Python Tool
 ↓
Tool Result
 ↓
Gemini AI
 ↓
Final Answer
```

This is the fundamental **AI Agent → Tool → Result → Agent** workflow.

---

## ✨ Current Features

### 🧠 Gemini-Powered Agent

Google Gemini acts as the reasoning/decision-making component of the agent.

### 🧮 Mathematical Expression Tool

The agent can use a Python calculator tool for mathematical expressions such as:

```text
21*12
454-12+22
2+2*4
(10+5)*3
100/5+20
```

The calculator supports:

* Addition
* Subtraction
* Multiplication
* Division
* Power
* Modulo
* Parentheses
* Negative numbers

The calculator uses Python's `ast` module instead of directly using `eval()` on user input.

### 📝 Text Analysis Tool

The project also includes a simple text-analysis tool that can calculate:

* Word count
* Character count

Example:

```text
AI agents can use tools.
```

Result:

```text
{
    "word_count": 5,
    "character_count": 25
}
```

### 🔧 Tool Calling

Gemini can decide when to use an available Python tool.

For example:

```text
You: 21*12

Agent decided to use: calculate_expression

Tool result: 252

Agent: 21 * 12 = 252
```

### 💬 Continuous Conversation

The agent can remain active and process multiple requests until the user enters:

```text
exit
```

---

# 🏗️ Architecture

The current architecture is:

```text
                    ┌───────────────┐
                    │     USER      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  GEMINI AI    │
                    │   AI BRAIN    │
                    └───────┬───────┘
                            │
                    Decide what to do
                            │
                            ▼
                    ┌───────────────┐
                    │     TOOLS     │
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
      ┌───────────────┐          ┌────────────────┐
      │  Calculator   │          │ Text Analyzer  │
      └───────┬───────┘          └───────┬────────┘
              │                           │
              └─────────────┬─────────────┘
                            ▼
                      Tool Result
                            │
                            ▼
                    ┌───────────────┐
                    │  GEMINI AI    │
                    │ Final Response │
                    └───────────────┘
```

---

# 📁 Project Structure

```text
My-first-AI-Agent/
│
├── agent.py
├── tools.py
├── text_tools.py
├── test_key.py
├── test_tool.py
├── test_text_tool.py
├── .gitignore
├── README.md
└── LICENSE
```

## File Descriptions

| File                | Description                                              |
| ------------------- | -------------------------------------------------------- |
| `agent.py`          | Main AI agent and tool-calling logic                     |
| `tools.py`          | Safe mathematical expression calculator                  |
| `text_tools.py`     | Text analysis functionality                              |
| `test_key.py`       | Tests Gemini API connectivity                            |
| `test_tool.py`      | Tests the calculator tool                                |
| `test_text_tool.py` | Tests the text analysis tool                             |
| `.gitignore`        | Prevents unwanted files and secrets from being committed |
| `README.md`         | Project documentation                                    |
| `LICENSE`           | MIT License                                              |

---

# 🛠️ Technologies Used

* **Python**
* **Google Gemini API**
* **Google GenAI Python SDK**
* **Git**
* **GitHub**

---

# ⚙️ Requirements

Before running the project, make sure you have:

* Python 3.10+
* A Google account
* A Gemini API key
* Internet connection
* Git

---

# 🔑 API Key Setup

The project uses the `GEMINI_API_KEY` environment variable.

**Never put your API key directly inside the Python source code.**

The code reads the key using:

```python
import os

api_key = os.getenv("GEMINI_API_KEY")
```

## Windows CMD

Set the environment variable with:

```cmd
setx GEMINI_API_KEY "YOUR_API_KEY"
```

After using `setx`, restart your terminal before running the project.

## Windows PowerShell

For the current PowerShell session:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

> ⚠️ Never commit your API key to GitHub.

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/sohail78692/My-first-AI-Agent.git
```

Move into the project directory:

```bash
cd My-first-AI-Agent
```

Install the Google GenAI SDK:

```bash
pip install google-genai
```

---

# ▶️ Running the Agent

Run:

```bash
python agent.py
```

You should see:

```text
API key found!

AI Agent is ready!
Type 'exit' to stop.

You:
```

You can now enter a request.

Example:

```text
You: 21*12
```

The agent can decide to use the calculator tool.

Example output:

```text
Agent decided to use: calculate_expression
Arguments: {'expression': '21*12'}

Tool result: 252

Agent: 21 * 12 = 252
```

---

# 🧪 Example Calculations

### Example 1

```text
You: 21*12
```

Result:

```text
252
```

### Example 2

```text
You: 454-12+22
```

Result:

```text
464
```

### Example 3

```text
You: 2+2*4
```

Result:

```text
10
```

### Example 4

```text
You: (10+5)*3
```

Result:

```text
45
```

### Example 5

```text
You: 100/5+20
```

Result:

```text
40
```

---

# 🔐 Security

This project intentionally keeps API credentials outside the source code.

The following files should never contain API keys:

```text
agent.py
test_key.py
tools.py
text_tools.py
```

The `.gitignore` file also prevents common environment files from being committed:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
```

If an API key is accidentally pushed to GitHub, it should be revoked immediately and replaced with a new key.

---

# 📚 What I Am Learning

This project is being developed as a practical way to understand AI agents.

Topics currently being explored:

* What AI agents are
* LLMs and AI models
* Gemini API integration
* Prompting
* Tool calling
* Function declarations
* Tool execution
* Agent loops
* API error handling
* Rate limits
* Environment variables
* API-key security
* Python-based AI applications
* Git and GitHub

---

# 🗺️ Roadmap

## Completed

* [x] Set up Python environment
* [x] Connect Python to Gemini
* [x] Create first AI-powered program
* [x] Create first Python tool
* [x] Implement Gemini tool calling
* [x] Execute tool results
* [x] Send tool results back to Gemini
* [x] Create continuous agent conversation
* [x] Build a safe mathematical expression calculator
* [x] Support mathematical operator precedence
* [x] Add a text analysis tool
* [x] Push project to GitHub

## In Progress / Planned

* [ ] Support multiple tools in the same agent
* [ ] Improve the agent/tool execution loop
* [ ] Handle multiple consecutive tool calls
* [ ] Improve error handling
* [ ] Add memory/state
* [ ] Add conversation history management
* [ ] Add document reading
* [ ] Learn RAG
* [ ] Add web search capabilities
* [ ] Explore LangChain
* [ ] Explore LangGraph
* [ ] Build a real-world AI agent
* [ ] Build a multi-tool autonomous agent
* [ ] Prepare an AI agent for a hackathon
* [ ] Participate in HackerRank Orchestrate

---

# 🎯 Learning Goal

The main goal of this project is not simply to create a chatbot.

The goal is to understand how an AI agent works internally:

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
Final Answer
```

After understanding these fundamentals, frameworks such as **LangChain** and **LangGraph** can be explored to understand how they simplify and extend these concepts.

---

# 🚧 Project Status

This project is currently **under active development**.

It started as a beginner project to learn AI agents from scratch and will gradually become more advanced as new concepts and tools are added.

Features, architecture, and documentation may change as the project evolves.

---

# 🤝 Contributions

This is primarily a personal learning project, but suggestions, improvements, and ideas are welcome.

If you find a bug or have an idea for improving the agent, feel free to open an issue or submit a pull request.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for the full license text.

---

# 👨‍💻 Author

**Sohail**

GitHub:

https://github.com/sohail78692

---

## ⭐ Project Goal

From:

> **"I have never built an AI agent."**

To:

> **"I understand and can build a multi-tool AI agent."**

🚀 **Learning by building.**

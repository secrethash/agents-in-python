# Agents in Python

This is a personal learning path repository for learning to build agents in python.

> **NOTE:** This is not meant to teach, but to learn.

## 👩‍💻 Learning Path

The learning path is divided into 3 Tiers:

---

### 🟢 Tier 1 — Fundamentals (Tool Use, Memory, Planning)

#### 🔧 [CLI Agent](./cli-agent)

An agent that can use Python functions as tools — a calculator, a weather fetcher, a file reader. This is the "Hello World" of agents. Learn the ReAct loop (Reason → Act → Observe) which is the heartbeat of every agent.

#### 🧠 [Personal Memory Agent](./memory-agent/)

An agent that remembers things across conversations using a simple vector store (like ChromaDB). Understand the difference between short-term context and long-term memory — a key design decision in every real agent.

#### 📋 [Task Planning Agent](./planning-agent/)

Give the agent a high-level goal (e.g., "Research Python best practices and write a summary") and it breaks it into subtasks, executes them sequentially, and reports back. Core concept: planning and self-prompting.

---

### 🟡 Tier 2 — Real-World Automation

#### 🌐 [Web Research Agent](./research-agent)

An agent that takes a question, searches the web (via Tavily/SerpAPI), scrapes relevant pages, synthesizes an answer, and cites sources. Combines tool use, chaining, and output formatting.

#### 📁 [Codebase Assistant Agent](./)

Point the agent at a local repo and ask it questions: "Find all functions that handle auth", "Refactor this module". You'll learn RAG + agents together with file I/O tools.

#### 📧 [Email/Calendar Automation Agent](./)

Connect to Gmail and Google Calendar APIs. The agent reads emails, drafts replies, schedules meetings, and handles follow-ups. This is where real-world reliability and error handling become the main lesson.

---

### 🔴 Tier 3 — Multi-Agent Systems

#### 🤝 [Research + Writer Multi-Agent Pipeline](./)

Two agents with distinct roles: a Researcher agent that gathers data, and a Writer agent that turns it into a blog post or report. They communicate via a shared message bus. This teaches agent orchestration.

#### 🏗️ [Autonomous Software Developer (Mini Devin)](./)

Give a spec, and a team of agents (Planner → Coder → Tester → Debugger) collaboratively write, run, test, and fix code. This is the capstone — it ties together everything from all tiers.

---

## 📍 Recommended Learning Stack

| Layer           | Recommended                         | Used                             |
|-----------------|-------------------------------------|----------------------------------|
| LLM API         | Anthropic (claude-sonnet) or OpenAI | Ollama + qwen2.5:7B              |
| Agent Framework | Raw Python first, then LangGraph    | Raw Python first, then LangGraph |
| Memory          | ChromaDB or FAISS                   | ChromaDB                         |
| Tool Execution  | Function calling / MCP              | Function calling                 |
| Orchestration   | LangGraph or AutoGen (Tier 3)       | &mdash;                          |

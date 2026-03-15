# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

A learning project for Python basics, virtual environments, and LangGraph fundamentals — building a chatbot with tools, human-in-the-loop approval, and streaming.

## Project Structure

```
chatbot/
├── state.py      # State TypedDict (message list)
├── nodes.py      # LLM setup, all node functions, conditional edge logic
├── graph.py      # Wires nodes/edges, compiles graph
├── cli.py        # Chat loop, streaming, interrupt handling
└── main.py       # Entry point

tools/
├── weather.py    # get_weather tool
├── calculator.py # calculator tool
└── __init__.py   # exports all_tools list

basics/
└── minimal_graph.py  # First LangGraph example (learning exercise)
```

## Environment Setup

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

## Running Code

```bash
# Run the chatbot
PYTHONPATH=. python3 -m chatbot.main

# Run a specific file
PYTHONPATH=. python3 path/to/script.py

# Run a single test (once tests are added)
python -m pytest tests/test_foo.py::test_bar -v
```

## Key Dependencies

- `langgraph` — graph-based agent/workflow orchestration
- `langchain-ollama` — Ollama LLM integration (model: `gpt-oss:120b-cloud`)
- `python-dotenv` — load API keys from `.env`

## LangGraph Concepts (project focus)

LangGraph models agent logic as a **directed graph** of nodes and edges:

- **State** — a typed dict passed through the graph at each step
- **Nodes** — Python functions that receive and return state
- **Edges** — control flow between nodes (can be conditional)
- **Graph** — assembled via `StateGraph`, compiled with `.compile()`
- **MemorySaver** — persists state across invocations via `thread_id`
- **interrupt()** — pauses graph execution for human input
- **Command(resume=...)** — resumes a paused graph with a decision
- **stream_mode="messages"** — streams LLM tokens chunk by chunk

## Conventions

- Keep API keys in `.env`, loaded via `python-dotenv`
- One concept per file (e.g., `state.py`, `nodes.py`, `graph.py`)
- Always run from project root with `PYTHONPATH=.` so package imports resolve

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

A learning project for Python basics, virtual environments, and LangGraph fundamentals — building toward a simple chatbot.

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
# Run a script
python main.py

# Run a specific file
python path/to/script.py

# Run a single test (once tests are added)
python -m pytest tests/test_foo.py::test_bar -v
```

## Key Dependencies (to be added)

- `langgraph` — graph-based agent/workflow orchestration
- `langchain-anthropic` or `langchain-openai` — LLM integrations
- `python-dotenv` — load API keys from `.env`

## LangGraph Concepts (project focus)

LangGraph models agent logic as a **directed graph** of nodes and edges:

- **State** — a typed dict passed through the graph at each step
- **Nodes** — Python functions that receive and return state
- **Edges** — control flow between nodes (can be conditional)
- **Graph** — assembled via `StateGraph`, compiled with `.compile()`

A minimal chatbot pattern: `user input → LLM node → output`, with optional memory via `MemorySaver` checkpointer.

## Conventions

- Keep API keys in `.env`, loaded via `python-dotenv`
- One concept per file while learning (e.g., `basic_graph.py`, `chatbot.py`)

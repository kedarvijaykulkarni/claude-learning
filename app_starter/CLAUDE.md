# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# Install package in development mode
uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_document.py

# Run a single test by name
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

This is an MCP (Model Context Protocol) server that exposes document-processing tools to AI assistants. Tools are Python functions registered with a `FastMCP` server instance.

**Entry point:** `main.py` — creates the `FastMCP` server, imports tool functions from `tools/`, registers each with `mcp.tool()(function_name)`, and calls `mcp.run()`.

**Tool implementations:** Live in `tools/`. Each file defines one or more plain Python functions. Functions are not automatically discovered — they must be explicitly imported and registered in `main.py`.

**Tests:** `tests/` uses `pytest` with class-based test groups. Binary fixture files (`.docx`, `.pdf`) live in `tests/fixtures/`.

## Defining MCP Tools

Tools are plain Python functions. Registration in `main.py`:

```python
from tools.my_module import my_function
mcp.tool()(my_function)
```

Use `pydantic.Field` for parameter descriptions (these surface as tool parameter docs in the MCP protocol):

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="What this parameter does"),
    param2: int = Field(description="What this parameter does")
) -> str:
    """
    One-line summary.

    Detailed explanation of what the tool does, when to use it (and when not to).

    Examples:
        my_tool("foo", 42) -> "result"
    """
```

Tool docstrings should follow this structure (per README): one-line summary → detailed explanation → when to use/not use → usage examples with expected input/output.

## Current Tools

| Tool | File | Registered |
|---|---|---|
| `add` | `tools/math.py` | Yes |
| `binary_document_to_markdown` | `tools/document.py` | No — defined but not yet added to `main.py` |

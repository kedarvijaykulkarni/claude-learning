# Document Tools

A Python package implementing document-related tools for converting and processing PDF and DOCX files. These tools are exposed through an MCP server interface for seamless integration with AI assistants.

## Setup

```bash
# Create a virtual env and activate it
uv venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# Install the package in development mode
uv pip install -e .
```

## Running

```bash
# Start the MCP server
uv run main.py
```

## Testing

```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_document_path_to_markdown.py

# Run a specific test by name
uv run pytest tests/test_document_path_to_markdown.py::TestHappyPath::test_pdf_returns_str
```

## Available Tools

| Tool | Description |
|---|---|
| `add` | Add two numbers together |
| `binary_document_to_markdown` | Convert binary document data (bytes) to markdown |
| `document_path_to_markdown` | Read a `.pdf` or `.docx` file from disk and return its contents as markdown |

### `document_path_to_markdown`

Reads a file at the given path and converts it to markdown text. Supports `.pdf` and `.docx` (case-insensitive). Raises:

- `FileNotFoundError` — path does not exist
- `ValueError` — unsupported extension, directory path, empty string, or zero-byte file
- `TypeError` — path is `None`
- `PermissionError` — file is not readable

## Development

### Adding a Tool

Define the function in `tools/`, then register it in `main.py`:

```python
from tools.my_module import my_function
mcp.tool()(my_function)
```

### Tool Docstring Convention

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """One-line summary.

    Detailed explanation of what the tool does.

    When to use:
    - ...

    When not to use:
    - ...

    Examples:
        my_tool("foo", 42) -> "result"
    """
```

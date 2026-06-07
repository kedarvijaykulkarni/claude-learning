import os
from io import BytesIO

from markitdown import MarkItDown, StreamInfo
from pydantic import Field

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to a .pdf or .docx file"),
) -> str:
    """Convert a PDF or DOCX file on disk to markdown-formatted text.

    Reads the file at the given path and returns its contents as markdown.
    Only .pdf and .docx extensions are supported (case-insensitive).

    When to use:
    - When you have a local file path and need its text content as markdown.
    - Prefer binary_document_to_markdown when you already have the file bytes.

    When not to use:
    - For file types other than PDF or DOCX.
    - When the file is remote (download it first).

    Examples:
        document_path_to_markdown("/docs/report.pdf") -> "# Report\\n\\n..."
        document_path_to_markdown("/docs/spec.docx")  -> "# Spec\\n\\n..."
    """
    if file_path is None:
        raise TypeError("file_path must be a string, got None")
    if not isinstance(file_path, str):
        raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")
    if file_path == "":
        raise ValueError("file_path must not be empty")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    if os.path.isdir(file_path):
        raise ValueError(f"Path is a directory, not a file: '{file_path}'")

    _, ext = os.path.splitext(file_path)
    ext_lower = ext.lower()
    if ext_lower not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file extension '{ext}'. Supported: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    with open(file_path, "rb") as f:
        binary_data = f.read()

    if len(binary_data) == 0:
        raise ValueError(f"File is empty (0 bytes): '{file_path}'")

    return binary_document_to_markdown(binary_data, ext_lower.lstrip("."))

import os
import shutil

import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")
DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")


# ---------------------------------------------------------------------------
# Extension variants
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def pdf_uppercase_ext(tmp_path_factory):
    dest = tmp_path_factory.mktemp("ext") / "mcp_docs.PDF"
    shutil.copy(PDF_FIXTURE, dest)
    return dest


@pytest.fixture(scope="session")
def docx_uppercase_ext(tmp_path_factory):
    dest = tmp_path_factory.mktemp("ext") / "mcp_docs.DOCX"
    shutil.copy(DOCX_FIXTURE, dest)
    return dest


@pytest.fixture(scope="session")
def pdf_renamed_to_docx(tmp_path_factory):
    """Valid PDF content but .docx extension."""
    dest = tmp_path_factory.mktemp("wrong_ext") / "mcp_docs_wrong.docx"
    shutil.copy(PDF_FIXTURE, dest)
    return dest


@pytest.fixture(scope="session")
def docx_renamed_to_pdf(tmp_path_factory):
    """Valid DOCX content but .pdf extension."""
    dest = tmp_path_factory.mktemp("wrong_ext") / "mcp_docs_wrong.pdf"
    shutil.copy(DOCX_FIXTURE, dest)
    return dest


@pytest.fixture(scope="session")
def file_no_extension(tmp_path_factory):
    dest = tmp_path_factory.mktemp("no_ext") / "mcp_docs"
    shutil.copy(PDF_FIXTURE, dest)
    return dest


@pytest.fixture(scope="session")
def file_txt_extension(tmp_path_factory):
    dest = tmp_path_factory.mktemp("unsupported") / "mcp_docs.txt"
    shutil.copy(PDF_FIXTURE, dest)
    return dest


@pytest.fixture(scope="session")
def file_doc_extension(tmp_path_factory):
    """Old Word .doc extension (not supported)."""
    dest = tmp_path_factory.mktemp("unsupported") / "legacy.doc"
    shutil.copy(DOCX_FIXTURE, dest)
    return dest


# ---------------------------------------------------------------------------
# Empty / zero-byte files
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def zero_byte_pdf(tmp_path_factory):
    path = tmp_path_factory.mktemp("empty") / "empty.pdf"
    path.touch()
    return path


@pytest.fixture(scope="session")
def zero_byte_docx(tmp_path_factory):
    path = tmp_path_factory.mktemp("empty") / "empty.docx"
    path.touch()
    return path


# ---------------------------------------------------------------------------
# Path edge cases
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def path_with_spaces(tmp_path_factory):
    dest = tmp_path_factory.mktemp("path with spaces") / "my document file.pdf"
    shutil.copy(PDF_FIXTURE, dest)
    return dest


@pytest.fixture(scope="session")
def path_with_unicode(tmp_path_factory):
    dest = tmp_path_factory.mktemp("unicode") / "résumé_café.pdf"
    shutil.copy(PDF_FIXTURE, dest)
    return dest


# ---------------------------------------------------------------------------
# Complex DOCX fixtures (built with python-docx)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def docx_with_headings(tmp_path_factory):
    Document = pytest.importorskip("docx").Document
    doc = Document()
    doc.add_heading("Main Title", level=1)
    doc.add_paragraph("Introduction paragraph.")
    doc.add_heading("Section One", level=2)
    doc.add_paragraph("Content in section one.")
    doc.add_heading("Subsection 1.1", level=3)
    doc.add_paragraph("Subsection content.")
    doc.add_heading("Section Two", level=2)
    doc.add_paragraph("Content in section two.")
    path = tmp_path_factory.mktemp("complex") / "headings.docx"
    doc.save(str(path))
    return path


@pytest.fixture(scope="session")
def docx_with_table(tmp_path_factory):
    Document = pytest.importorskip("docx").Document
    doc = Document()
    doc.add_heading("Table Test Document", level=1)
    table = doc.add_table(rows=3, cols=3)
    headers = ["Name", "Role", "Score"]
    rows = [["Alice", "Engineer", "95"], ["Bob", "Designer", "88"]]
    for col, header in enumerate(headers):
        table.cell(0, col).text = header
    for row_idx, row_data in enumerate(rows, start=1):
        for col_idx, value in enumerate(row_data):
            table.cell(row_idx, col_idx).text = value
    path = tmp_path_factory.mktemp("complex") / "table.docx"
    doc.save(str(path))
    return path


@pytest.fixture(scope="session")
def docx_with_formatted_text(tmp_path_factory):
    Document = pytest.importorskip("docx").Document
    doc = Document()
    para = doc.add_paragraph()
    run = para.add_run("Bold text ")
    run.bold = True
    run = para.add_run("italic text ")
    run.italic = True
    para.add_run("normal text")
    path = tmp_path_factory.mktemp("complex") / "formatted.docx"
    doc.save(str(path))
    return path


@pytest.fixture(scope="session")
def docx_with_list(tmp_path_factory):
    Document = pytest.importorskip("docx").Document
    doc = Document()
    doc.add_heading("Shopping List", level=1)
    for item in ["Apples", "Bananas", "Cherries"]:
        doc.add_paragraph(item, style="List Bullet")
    path = tmp_path_factory.mktemp("complex") / "list.docx"
    doc.save(str(path))
    return path


@pytest.fixture(scope="session")
def docx_with_special_chars(tmp_path_factory):
    Document = pytest.importorskip("docx").Document
    doc = Document()
    doc.add_paragraph("Special chars: & < > \" ' © ® ™ € £ ¥")
    doc.add_paragraph("Unicode text: café naïve résumé")
    path = tmp_path_factory.mktemp("complex") / "special_chars.docx"
    doc.save(str(path))
    return path


@pytest.fixture(scope="session")
def docx_empty_content(tmp_path_factory):
    """Valid DOCX structure but no paragraphs or content."""
    Document = pytest.importorskip("docx").Document
    doc = Document()
    path = tmp_path_factory.mktemp("empty") / "empty_content.docx"
    doc.save(str(path))
    return path

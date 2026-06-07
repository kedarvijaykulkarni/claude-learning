"""Tests for the document_path_to_markdown tool.

Covers: happy path, PDF-specific, DOCX-specific, extension/type validation,
path & filesystem edge cases, complex document elements, and output format.
"""

import os
import sys

import pytest

from tools.document import document_path_to_markdown

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")
DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")


# ===========================================================================
# Happy path
# ===========================================================================

class TestHappyPath:
    def test_pdf_returns_str(self):
        assert isinstance(document_path_to_markdown(PDF_FIXTURE), str)

    def test_docx_returns_str(self):
        assert isinstance(document_path_to_markdown(DOCX_FIXTURE), str)

    def test_pdf_result_is_not_none(self):
        assert document_path_to_markdown(PDF_FIXTURE) is not None

    def test_docx_result_is_not_none(self):
        assert document_path_to_markdown(DOCX_FIXTURE) is not None

    def test_pdf_result_is_nonempty(self):
        assert len(document_path_to_markdown(PDF_FIXTURE)) > 0

    def test_docx_result_is_nonempty(self):
        assert len(document_path_to_markdown(DOCX_FIXTURE)) > 0


# ===========================================================================
# PDF-specific
# ===========================================================================

class TestPdfSpecific:
    def test_uppercase_extension_accepted(self, pdf_uppercase_ext):
        result = document_path_to_markdown(str(pdf_uppercase_ext))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_multipage_pdf_returns_substantial_content(self):
        # MCP docs fixture is multi-page; expect more than a trivial snippet
        result = document_path_to_markdown(PDF_FIXTURE)
        assert len(result) > 100

    def test_pdf_output_is_valid_utf8(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        # If encoding were broken this would raise UnicodeEncodeError
        result.encode("utf-8")

    def test_pdf_output_contains_no_raw_binary(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        # No null bytes — sign of unprocessed binary data leaking through
        assert "\x00" not in result

    def test_pdf_content_is_text_not_binary_artifact(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        # At least some printable ASCII should exist
        printable_count = sum(1 for c in result if c.isprintable())
        assert printable_count > 0


# ===========================================================================
# DOCX-specific
# ===========================================================================

class TestDocxSpecific:
    def test_uppercase_extension_accepted(self, docx_uppercase_ext):
        result = document_path_to_markdown(str(docx_uppercase_ext))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_headings_preserved_in_output(self, docx_with_headings):
        result = document_path_to_markdown(str(docx_with_headings))
        assert "Main Title" in result
        assert "Section One" in result
        assert "Section Two" in result

    def test_headings_use_markdown_hash_syntax(self, docx_with_headings):
        result = document_path_to_markdown(str(docx_with_headings))
        assert "#" in result

    def test_table_cell_content_present(self, docx_with_table):
        result = document_path_to_markdown(str(docx_with_table))
        assert "Alice" in result
        assert "Bob" in result
        assert "Engineer" in result

    def test_table_rendered_as_markdown_table(self, docx_with_table):
        result = document_path_to_markdown(str(docx_with_table))
        assert "|" in result

    def test_list_items_present(self, docx_with_list):
        result = document_path_to_markdown(str(docx_with_list))
        assert "Apples" in result
        assert "Bananas" in result
        assert "Cherries" in result

    def test_formatted_text_content_preserved(self, docx_with_formatted_text):
        result = document_path_to_markdown(str(docx_with_formatted_text))
        assert "Bold text" in result
        assert "italic text" in result
        assert "normal text" in result

    def test_special_characters_do_not_corrupt_output(self, docx_with_special_chars):
        result = document_path_to_markdown(str(docx_with_special_chars))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_special_characters_content_readable(self, docx_with_special_chars):
        result = document_path_to_markdown(str(docx_with_special_chars))
        # At minimum the plain ASCII words survive
        assert "Special chars" in result or "café" in result

    def test_empty_content_docx_returns_str(self, docx_empty_content):
        # A structurally valid but content-free DOCX should return a string
        # (empty or near-empty), not raise an exception
        result = document_path_to_markdown(str(docx_empty_content))
        assert isinstance(result, str)

    def test_output_contains_no_raw_xml_tags(self, docx_with_headings):
        result = document_path_to_markdown(str(docx_with_headings))
        assert "<w:" not in result
        assert "</w:" not in result

    @pytest.mark.skip(reason="Requires a fixture with embedded image — add tests/fixtures/image.docx")
    def test_docx_with_embedded_image_does_not_crash(self):
        pass

    @pytest.mark.skip(reason="Requires a password-protected .docx fixture")
    def test_password_protected_docx_raises_error(self):
        pass


# ===========================================================================
# Extension and file-type validation
# ===========================================================================

class TestExtensionAndFileTypeValidation:
    def test_txt_extension_raises_value_error(self, file_txt_extension):
        with pytest.raises(ValueError):
            document_path_to_markdown(str(file_txt_extension))

    def test_no_extension_raises_value_error(self, file_no_extension):
        with pytest.raises(ValueError):
            document_path_to_markdown(str(file_no_extension))

    def test_old_doc_extension_raises_value_error(self, file_doc_extension):
        with pytest.raises(ValueError):
            document_path_to_markdown(str(file_doc_extension))

    def test_zero_byte_pdf_raises_exception(self, zero_byte_pdf):
        with pytest.raises(Exception):
            document_path_to_markdown(str(zero_byte_pdf))

    def test_zero_byte_docx_raises_exception(self, zero_byte_docx):
        with pytest.raises(Exception):
            document_path_to_markdown(str(zero_byte_docx))

    def test_pdf_content_with_docx_extension_returns_str(self, pdf_renamed_to_docx):
        """markitdown is lenient with content/extension mismatches — result is a string."""
        result = document_path_to_markdown(str(pdf_renamed_to_docx))
        assert isinstance(result, str)

    def test_docx_content_with_pdf_extension_returns_str(self, docx_renamed_to_pdf):
        """markitdown is lenient with content/extension mismatches — result is a string."""
        result = document_path_to_markdown(str(docx_renamed_to_pdf))
        assert isinstance(result, str)


# ===========================================================================
# Path and filesystem
# ===========================================================================

class TestPathAndFilesystem:
    def test_nonexistent_file_raises_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(str(tmp_path / "ghost.pdf"))

    def test_directory_path_raises_error(self, tmp_path):
        with pytest.raises((IsADirectoryError, ValueError, OSError)):
            document_path_to_markdown(str(tmp_path))

    def test_none_raises_type_or_value_error(self):
        with pytest.raises((TypeError, ValueError)):
            document_path_to_markdown(None)

    def test_empty_string_raises_error(self):
        with pytest.raises((ValueError, FileNotFoundError)):
            document_path_to_markdown("")

    def test_path_with_spaces(self, path_with_spaces):
        result = document_path_to_markdown(str(path_with_spaces))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_path_with_unicode_characters(self, path_with_unicode):
        result = document_path_to_markdown(str(path_with_unicode))
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.skipif(sys.platform == "win32", reason="chmod read-deny unreliable on Windows")
    def test_permission_denied_raises_permission_error(self, tmp_path):
        import shutil
        path = tmp_path / "noaccess.pdf"
        shutil.copy(PDF_FIXTURE, path)
        os.chmod(path, 0o000)
        try:
            with pytest.raises(PermissionError):
                document_path_to_markdown(str(path))
        finally:
            os.chmod(path, 0o644)


# ===========================================================================
# Output format validation
# ===========================================================================

class TestOutputFormat:
    def test_return_type_is_str_for_pdf(self):
        assert type(document_path_to_markdown(PDF_FIXTURE)) is str

    def test_return_type_is_str_for_docx(self):
        assert type(document_path_to_markdown(DOCX_FIXTURE)) is str

    def test_output_is_valid_utf8_for_pdf(self):
        document_path_to_markdown(PDF_FIXTURE).encode("utf-8")

    def test_output_is_valid_utf8_for_docx(self):
        document_path_to_markdown(DOCX_FIXTURE).encode("utf-8")

    def test_output_has_no_null_bytes_pdf(self):
        assert "\x00" not in document_path_to_markdown(PDF_FIXTURE)

    def test_output_has_no_null_bytes_docx(self):
        assert "\x00" not in document_path_to_markdown(DOCX_FIXTURE)

    def test_output_has_no_internal_xml_for_docx(self):
        result = document_path_to_markdown(DOCX_FIXTURE)
        assert "<w:" not in result

    def test_output_has_no_internal_xml_for_pdf(self):
        result = document_path_to_markdown(PDF_FIXTURE)
        assert "<?xml" not in result or result.count("<?xml") == 0

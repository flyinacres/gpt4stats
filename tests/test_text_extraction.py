import fitz
from extract_stats import extract_text_from_pdf

def test_text_extraction():
    pdf_path = "tests/sample.pdf"
    text = extract_text_from_pdf(pdf_path)
    assert isinstance(text, str)
    assert len(text) > 0

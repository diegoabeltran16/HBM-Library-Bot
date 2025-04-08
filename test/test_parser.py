# tests/test_parser.py

from src.parser import extract_text

def test_extraccion_pdf_simple():
    texto = extract_text("tests/fixtures/pdf_simple.pdf")
    assert len(texto) > 100  # Texto mínimo esperado

def test_descarta_formula():
    texto = extract_text("tests/fixtures/pdf_formula.pdf")
    assert "∫" not in texto

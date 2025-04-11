# tests/test_parser.py
import sys
from pathlib import Path
from src.parser import extract_text

# 🔧 Asegura que src/ sea visible desde cualquier entorno
sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_extraccion_pdf_simple():
    texto = extract_text("tests/fixtures/pdf_simple.pdf")
    assert len(texto) > 100  # Texto mínimo esperado

def test_descarta_formula():
    texto = extract_text("tests/fixtures/pdf_formula.pdf")
    assert "∫" not in texto

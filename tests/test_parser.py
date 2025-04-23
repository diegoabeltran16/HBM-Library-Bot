import sys
from pathlib import Path
import pytest

# 🔧 Asegura que src/ sea visible desde cualquier entorno
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.parser import extract_text, es_pdf_complejo

# ---
# 🧪 test_parser.py – Pruebas integradas del módulo de parsing
#
# Incluye tests para:
# - PDFs normales (texto extraíble directamente)
# - PDFs escaneados (requieren OCR)
# - Validación de la heurística `es_pdf_complejo`
# - Comportamiento de limpieza semántica


def test_extraccion_pdf_simple():
    texto = extract_text("tests/fixtures/pdf_simple.pdf")
    assert len(texto) > 100  # Texto mínimo esperado


def test_descarta_formula():
    texto = extract_text("tests/fixtures/pdf_formula.pdf")
    assert "∫" not in texto  # Esperamos limpieza de caracteres simbólicos si están mal interpretados


def test_pdf_texto_normal():
    texto = extract_text("tests/fixtures/pdf_textual.pdf")
    assert isinstance(texto, str)
    assert len(texto) > 50
    assert "introducción" in texto.lower()


def test_pdf_necesita_ocr():
    texto = extract_text("tests/fixtures/pdf_escaneado.pdf")
    assert isinstance(texto, str)
    assert len(texto.strip()) > 20


def test_heuristica_es_pdf_complejo():
    assert es_pdf_complejo("tests/fixtures/pdf_escaneado.pdf") is True
    assert es_pdf_complejo("tests/fixtures/pdf_textual.pdf") is False

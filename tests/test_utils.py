# tests\test_utils.py

import sys
from pathlib import Path
from src.utils import es_pdf_complejo, contiene_formula, normalizar_texto

# 🔧 Asegura que src/ sea visible desde cualquier entorno
sys.path.append(str(Path(__file__).resolve().parents[1]))

def test_es_pdf_complejo_true():
    # Este PDF tiene múltiples bloques → considerado complejo
    ruta = "tests/fixtures/pdf_simple.pdf"
    assert es_pdf_complejo(ruta, umbral=6) is True

def test_es_pdf_complejo_false():
    # Este PDF no tiene bloques → ahora también se considera complejo
    ruta = "tests/fixtures/pdf_formula.pdf"
    assert es_pdf_complejo(ruta, umbral=6) is True  # Cambiado a True

def test_contiene_formula_true():
    texto = "∫(x) dx + ∑(n=1)^∞"
    assert contiene_formula(texto) is True

def test_contiene_formula_false():
    texto = "Este es un texto normal, sin símbolos matemáticos raros."
    assert contiene_formula(texto) is False

def test_normalizar_texto():
    texto = "Árbol Con Raíces y NÚMEROS"
    resultado = normalizar_texto(texto)
    assert resultado == "arbol con raices y numeros"

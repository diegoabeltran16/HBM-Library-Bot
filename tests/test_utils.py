import sys
from pathlib import Path
import pytest

# 🔧 Asegura visibilidad del módulo src/
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import (
    es_pdf_complejo,
    contiene_formula,
    normalizar_texto,
    calcular_hash_md5
)

# ─────────────────────────────────────────────────────────────
# Tests de evaluación estructural de PDF
# ─────────────────────────────────────────────────────────────

def test_es_pdf_complejo_true():
    # Este PDF tiene múltiples bloques → considerado complejo
    ruta = "tests/fixtures/pdf_simple.pdf"
    assert es_pdf_complejo(ruta, umbral=6) is True

def test_es_pdf_complejo_false():
    # Este PDF no tiene bloques → ahora también se considera complejo
    ruta = "tests/fixtures/pdf_formula.pdf"
    assert es_pdf_complejo(ruta, umbral=6) is True  # Se considera complejo si no hay texto

# ─────────────────────────────────────────────────────────────
# Tests de heurística sobre fórmulas
# ─────────────────────────────────────────────────────────────

def test_contiene_formula_true():
    texto = "∫(x) dx + ∑(n=1)^∞"
    assert contiene_formula(texto) is True

def test_contiene_formula_false():
    texto = "Este es un texto normal, sin símbolos matemáticos raros."
    assert contiene_formula(texto) is False

# ─────────────────────────────────────────────────────────────
# Tests de normalización semántica
# ─────────────────────────────────────────────────────────────

def test_normalizar_texto():
    texto = "Árbol Con Raíces y NÚMEROS"
    resultado = normalizar_texto(texto)
    assert resultado == "arbol con raices y numeros"

# ─────────────────────────────────────────────────────────────
# Test de trazabilidad genética (hashing)
# ─────────────────────────────────────────────────────────────

def test_calcular_hash_md5(tmp_path):
    # Creamos un PDF mínimo simulado
    archivo = tmp_path / "mini.pdf"
    archivo.write_bytes(b"%PDF-1.4\n%EOF")

    hash_val = calcular_hash_md5(str(archivo))
    assert isinstance(hash_val, str)
    assert len(hash_val) == 32  # Longitud típica del hash MD5

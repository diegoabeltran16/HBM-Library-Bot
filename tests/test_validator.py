import pytest
import sys
from pathlib import Path

# Asegura visibilidad del módulo src/
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.validator import (
    validar_resumen,
    validar_secciones,
    validar_citas_referencias,
    validar_documento
)

# ─────────────────────────────────────────────────────────────
# Tests unitarios específicos
# ─────────────────────────────────────────────────────────────

def test_validar_resumen_faltante():
    texto = "Este documento no tiene resumen inicial explícito."
    errores = validar_resumen(texto)
    assert any("Resumen no encontrado" in e for e in errores)

def test_validar_secciones_faltantes():
    texto = "Este texto solo tiene una sección llamada Resultados."
    errores = validar_secciones(texto)
    assert any("Secciones faltantes" in e for e in errores)

def test_validar_citas_referencias_ausentes():
    texto = "Este texto no contiene ningún patrón válido de referencia académica."
    errores = validar_citas_referencias(texto)
    assert any("citas" in e.lower() for e in errores)

# ─────────────────────────────────────────────────────────────
# Test integrador: documento con múltiples errores
# ─────────────────────────────────────────────────────────────

def test_validar_documento_con_errores(tmp_path):
    texto = "texto muy corto sin estructura ni resumen ni referencias"
    ruta_pdf = tmp_path / "doc_fallido.pdf"
    ruta_pdf.write_text("contenido simulado")

    es_valido, info = validar_documento(texto, str(ruta_pdf))
    assert es_valido is True
    assert isinstance(info.get("razones"), list)
    assert len(info["razones"]) >= 3
    assert any("Resumen" in e for e in info["razones"])
    assert any("Secciones" in e for e in info["razones"])
    assert any("citas" in e.lower() for e in info["razones"])

def test_documento_real_the_origins():
    import fitz  # PyMuPDF
    ruta = "tests/fixtures/The Origins of music.pdf"
    doc = fitz.open(ruta)
    texto = "\n".join([page.get_text() for page in doc if page.get_text()])

    es_valido, info = validar_documento(texto, ruta)
    print("Errores detectados:", info)
    assert es_valido is True
    assert isinstance(info.get("razones"), list)
    assert len(info["razones"]) <= 2  # toleramos 0-2 errores leves

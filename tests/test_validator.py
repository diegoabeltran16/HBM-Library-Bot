# tests/test_validator.py

import pytest
import sys
from pathlib import Path

# 🔧 Asegura que src/ sea visible desde cualquier entorno
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.validator import (
    validar_texto_no_vacio,
    validar_longitud,
    validar_titulo,
    validar_autor,
    validar_documento
)

# ─────────────────────────────────────────────────────────────
# Test individuales
# ─────────────────────────────────────────────────────────────

def test_validar_texto_no_vacio():
    assert validar_texto_no_vacio("   ")[0] is False
    assert validar_texto_no_vacio("Contenido útil")[0] is True

def test_validar_longitud():
    texto_corto = "Esto es un texto corto."
    texto_largo = " ".join(["palabra"] * 200)
    assert validar_longitud(texto_corto)[0] is False
    assert validar_longitud(texto_largo)[0] is True

def test_validar_titulo():
    assert validar_titulo("untitled")[0] is False
    assert validar_titulo("")[0] is False
    assert validar_titulo("Mi gran investigación sobre redes")[0] is True

def test_validar_autor():
    assert validar_autor("anonymous")[0] is False
    assert validar_autor("-")[0] is False
    assert validar_autor("Jane Doe")[0] is True

# ─────────────────────────────────────────────────────────────
# Test de la función principal
# ─────────────────────────────────────────────────────────────

def test_validar_documento_valido():
    texto = " ".join(["contenido"] * 200)
    titulo = "Un estudio profundo sobre grafos semánticos"
    autor = "Dr. Ada Lovelace"
    es_valido, info = validar_documento(texto, titulo, autor)
    assert es_valido is True
    assert info == {}

def test_validar_documento_invalido():
    texto = "    "  # vacío
    titulo = "untitled"
    autor = ""
    es_valido, info = validar_documento(texto, titulo, autor)
    assert es_valido is False
    assert "texto vacío" in " ".join(info.get("razones", []))
    assert any("autor" in r for r in info.get("razones", []))

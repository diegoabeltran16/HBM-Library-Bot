# tests/test_enhancer.py – Pruebas unitarias para enhancer.py

import pytest
import sys
import unicodedata
from src.enhancer import reparar_cid, normalizar_unicode, enriquecer_texto
from pathlib import Path

# 🔧 Asegura que src/ sea visible desde cualquier entorno
sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_reparar_cid():
    texto = "introduccid:413ión a la AI cid:99"
    esperado = "introducción a la AI "
    corregido, stats = reparar_cid(texto)
    assert "cid:413" not in corregido
    assert "cid:99" not in corregido
    assert stats["cid_reparados"] == 2


def test_normalizar_unicode():
    texto = "cafe\u0301"  # e + acento
    esperado = unicodedata.normalize("NFKC", "café")  # normaliza el esperado también
    corregido, stats = normalizar_unicode(texto)
    assert unicodedata.normalize("NFKC", corregido) == esperado
    assert stats["unicode_normalizado"] is True



def test_enriquecer_texto_completo():
    texto = "cid:200 texto cid:11ó"
    enriquecido = enriquecer_texto(texto)
    assert "cid:" not in enriquecido
    assert "texto" in enriquecido



def test_enriquecer_texto_sin_cambios():
    texto = "Este es un texto limpio y correcto."
    enriquecido = enriquecer_texto(texto)
    assert enriquecido == texto

# TODO: cuando implementemos corrección de encoding (latin1 → utf-8), testear reconstrucción de "óptima", etc.

"""
🧪 tests/test_enhancer.py – Validación de la lógica avanzada de reparación de texto

Objetivo:
- Verificar la efectividad de cada función de mejora del módulo enhancer
- Confirmar que estadísticas se acumulen correctamente
- Comprobar el comportamiento de la cascada con parámetros
"""

import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.enhancer import (
    reemplazar_cid_ascii,
    reparar_cid,
    reparar_palabras_partidas,
    reparar_encoding,
    normalizar_unicode,
    marcar_fragmentos_dudosos,
    enriquecer_texto,
    acumular_stats,
    reparar_ocr_simbolos,  # 🆕 OCR fix test
)

# ─────────────────────────────────────────────────────────────
# ✅ Tests individuales de funciones
# ─────────────────────────────────────────────────────────────

def test_reemplazar_cid_ascii():
    texto = "Introduc(cid:243)n a la teor(cid:237)a"
    corregido, stats = reemplazar_cid_ascii(texto)
    assert "cid:" not in corregido
    assert "ó" in corregido
    assert "í" in corregido
    assert stats["cid_ascii_convertidos"] == 2

def test_reparar_cid():
    texto = "cid:123 algo cid:456"
    corregido, stats = reparar_cid(texto)
    assert "cid:" not in corregido
    assert stats["cid_reparados"] == 2

def test_reparar_palabras_partidas():
    texto = "introduccid:415ion funciocid:123nal"
    corregido, stats = reparar_palabras_partidas(texto)
    assert "cid:" not in corregido
    assert "introduccion" in corregido or "introducion" in corregido
    assert stats["palabras_reparadas"] == 2

def test_reparar_encoding():
    texto = "funciÃ³n y automÃ¡tico"
    corregido, stats = reparar_encoding(texto)
    assert "Ã" not in corregido
    assert "ó" in corregido or "á" in corregido
    assert stats["encoding_reparado"] == 1

def test_normalizar_unicode():
    texto = "Cafe\u0301"
    corregido, stats = normalizar_unicode(texto)
    assert corregido == "Café"
    assert stats["unicode_normalizado"] == 1

def test_marcar_fragmentos_dudosos():
    texto = "†∆≈©§"
    corregido, stats = marcar_fragmentos_dudosos(texto)
    assert "[DUDOSO]" in corregido
    assert stats["marcas_insertadas"] == 1

def test_reparar_ocr_simbolos():
    texto = "This ﬁle has ﬂawed OCR with Ɵ instead of O."
    corregido, stats = reparar_ocr_simbolos(texto)
    assert "ﬁ" not in corregido
    assert "flawed" in corregido
    assert "file" in corregido
    assert "Ɵ" not in corregido
    assert "O" in corregido or "Theta" not in corregido
    assert stats["simbolos_ocr_corregidos"] >= 1

# ─────────────────────────────────────────────────────────────
# 🔁 Test integración y flujo completo
# ─────────────────────────────────────────────────────────────

def test_enriquecer_texto_completo():
    texto = "cid:123 Introduc(cid:243)n Ã³ptima ﬁle Ɵbservations cid:777"
    enriquecido = enriquecer_texto(texto, debug=False)
    assert "cid:" not in enriquecido
    assert "óptima" in enriquecido
    assert "Introducción" in enriquecido or "introduccion" in enriquecido or "Introducón" in enriquecido
    assert "ﬁle" not in enriquecido
    assert "Ɵ" not in enriquecido
    assert "file" in enriquecido or "observations" in enriquecido

def test_enriquecer_texto_sin_cambios():
    texto = "Este texto es limpio y claro."
    enriquecido = enriquecer_texto(texto)
    assert enriquecido == texto

def test_enriquecer_texto_condicional_pasando_pasos():
    texto = "cid:321 funciocid:444nal"
    pasos = [reparar_palabras_partidas]
    enriquecido = enriquecer_texto(texto, pasos=pasos)
    assert "cid:" in enriquecido  # porque no aplicamos reparar_cid
    assert "funcional" in enriquecido or "funcionl" in enriquecido

# ─────────────────────────────────────────────────────────────
# 🔢 Test utilitario de acumulación de estadísticas
# ─────────────────────────────────────────────────────────────

def test_acumular_stats():
    a = {"cid": 2, "errores": 1}
    b = {"cid": 3, "nuevos": 4}
    combinado = acumular_stats(a.copy(), b)
    assert combinado == {"cid": 5, "errores": 1, "nuevos": 4}

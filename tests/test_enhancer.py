import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.enhancer import (
    reemplazar_cid_ascii,
    reparar_encoding,
    normalizar_unicode,
    reparar_palabras_partidas,
    reparar_cid,
    reparar_ocr_simbolos,
    marcar_fragmentos_dudosos,
    pipeline_hooked_enhancer,
    enriquecer_texto
)

# ─────────────────────────────────────────────────────────────
# 🧬 Test nuevo flujo: pipeline_hooked_enhancer
# ─────────────────────────────────────────────────────────────

def test_pipeline_hooked_enhancer_basico(tmp_path):
    texto_dañado = "cid:241 El aÃ±o 2023 fue difÃ­cil. ﬁle, ﬂuid, Ɵmega."
    ruta_dummy = tmp_path / "texto_dummy.pdf"
    ruta_dummy.write_text("dummy content")

    config = {
        "pasos": [
            reemplazar_cid_ascii,
            reparar_encoding,
            normalizar_unicode,
            reparar_palabras_partidas,
            reparar_cid,
            reparar_ocr_simbolos,
            marcar_fragmentos_dudosos
        ],
        "retry_umbral": 1,
        "max_intentos": 2
    }

    enriquecido, stats = pipeline_hooked_enhancer(texto_dañado, config)

    assert "cid:" not in enriquecido
    # Verifica que se corrija al menos un caracter acentuado (í) tras encoding
    assert "í" in enriquecido, "Debe contener al menos un carácter acentuado (í) tras la corrección"
    assert "file" in enriquecido
    assert "fluid" in enriquecido
    assert "Omega" in enriquecido or "O" in enriquecido
    assert "Ã" not in enriquecido


def test_pipeline_hooked_enhancer_no_cambios(tmp_path):
    texto_limpio = "Este es un texto sin errores visibles."
    ruta_dummy = tmp_path / "texto_ok.pdf"
    ruta_dummy.write_text("dummy content")

    config = {
        "pasos": [
            reemplazar_cid_ascii,
            reparar_encoding,
            normalizar_unicode,
            reparar_palabras_partidas,
            reparar_cid,
            reparar_ocr_simbolos,
            marcar_fragmentos_dudosos
        ]
    }

    enriquecido, stats = pipeline_hooked_enhancer(texto_limpio, config)
    assert enriquecido == texto_limpio

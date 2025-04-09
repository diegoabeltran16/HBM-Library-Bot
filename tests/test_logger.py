# tests/test_logger.py

import os
import builtins
import pytest
from src.logger import log_mensaje

@pytest.mark.parametrize("lang,evento,esperado", [
    ("es", "export_ok", "✔️ Exportación completa"),
    ("en", "export_ok", "✔️ Export completed"),
    ("es", "clasificacion", "📖 Clasificado como"),
    ("en", "clasificacion", "📖 Classified as"),
    ("es", "formato_descartado", "⚠️ Línea descartada"),
])
def test_log_mensaje_parametrizado(lang, evento, esperado, capsys):
    os.environ["LANG"] = lang
    log_mensaje(evento, archivo="demo.txt", categoria="Filosofía", dewey="100")

    salida = capsys.readouterr().out
    assert esperado in salida


def test_log_mensaje_evento_desconocido(capsys):
    log_mensaje("evento_fake")
    salida = capsys.readouterr().out
    assert "⚠️ Evento desconocido" in salida

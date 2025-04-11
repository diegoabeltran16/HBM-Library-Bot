# tests/test_logger.py

import os
import json
import pytest
from pathlib import Path
from src.logger import log_evento

# 🌍 Forzamos idioma en entorno CI/test
os.environ["LANG"] = "es"

@pytest.fixture
def ruta_dummy(tmp_path):
    archivo = tmp_path / "demo_test.pdf"
    archivo.write_text("Contenido simulado para logging.")
    return str(archivo)

def test_log_evento_clasificado_en_consola_y_jsonl(capsys, ruta_dummy):
    os.environ["LANG"] = "es"
    log_evento("clasificado", archivo=ruta_dummy, categoria="Ciencias", dewey="500")

    # ✅ Salida visual
    salida = capsys.readouterr().out
    assert "📖 Clasificado como: Ciencias (500)" in salida

    # ✅ Persistencia .jsonl
    logs_dir = Path("output/logs")
    jsonl_logs = list(logs_dir.glob("run_*.jsonl"))
    assert jsonl_logs, "No se generó archivo .jsonl"

    with open(jsonl_logs[-1], encoding="utf-8") as f:
        lineas = [json.loads(line) for line in f if line.strip()]
        eventos = [l for l in lineas if l["evento"] == "clasificado"]
        assert eventos, "No se encontró el evento 'clasificado'"
        assert eventos[-1]["categoria"] == "Ciencias"
        assert eventos[-1]["dewey"] == "500"
        assert eventos[-1]["nivel"] == "INFO"

def test_log_warning_texto_corto(capsys, ruta_dummy):
    log_evento("warning_texto_corto", archivo=ruta_dummy, nivel="WARNING")
    salida = capsys.readouterr().out
    assert "⚠️ Texto extraído demasiado corto" in salida

def test_log_error_parse(capsys, ruta_dummy):
    log_evento("error_parse", archivo=ruta_dummy, nivel="ERROR")
    salida = capsys.readouterr().out
    assert "❌ Error procesando archivo" in salida

def test_log_individual_por_pdf(ruta_dummy):
    log_evento("procesar", archivo=ruta_dummy)

    logs_dir = Path("output/logs")
    nombre_pdf = Path(ruta_dummy).stem
    archivo_log = logs_dir / f"{nombre_pdf}.log"

    assert archivo_log.exists(), f"No se creó log individual: {archivo_log}"

    with open(archivo_log, encoding="utf-8") as f:
        contenido = f.read()
        assert "📘" in contenido or "PROCESAR" in contenido.upper()

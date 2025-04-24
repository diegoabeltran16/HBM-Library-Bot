# tests/test_logger.py

import sys
from pathlib import Path

# 🔧 Asegura que src/ sea visible desde cualquier entorno
sys.path.append(str(Path(__file__).resolve().parents[1]))

import os
import json
import pytest

from src.logger import log_evento, log_validacion  # <- ya podés importar ambos


# 🌍 Forzar idioma en pruebas
os.environ["LANG"] = "es"

@pytest.fixture
def ruta_dummy(tmp_path):
    archivo = tmp_path / "demo_test.pdf"
    archivo.write_text("Contenido simulado para logging.")
    return str(archivo)

def test_log_evento_clasificado_en_consola_y_jsonl(ruta_dummy):
    mensaje = log_evento("clasificado", archivo=ruta_dummy, categoria="Ciencias", dewey="500")
    assert "📖 Clasificado como: Ciencias (500)" in mensaje

    # ✅ Persistencia .jsonl
    logs_dir = Path("output/logs")
    jsonl_logs = list(logs_dir.glob("run_*.jsonl"))
    assert jsonl_logs, "No se generó archivo .jsonl"

    eventos = []
    with open(jsonl_logs[-1], encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("evento") == "clasificado":
                    eventos.append(data)
            except json.JSONDecodeError:
                continue  # Línea corrupta o mal formada

    assert eventos, "No se encontró el evento 'clasificado'"
    assert eventos[-1]["categoria"] == "Ciencias"
    assert eventos[-1]["dewey"] == "500"
    assert eventos[-1]["nivel"] == "INFO"



def test_log_warning_texto_corto(ruta_dummy):
    mensaje = log_evento("warning_texto_corto", archivo=ruta_dummy, nivel="WARNING")
    assert "⚠️ Texto extraído demasiado corto" in mensaje

def test_log_error_parse(ruta_dummy):
    mensaje = log_evento("error_parse", archivo=ruta_dummy, nivel="ERROR")
    assert "❌ Error procesando archivo" in mensaje

def test_log_individual_por_pdf(ruta_dummy):
    log_evento("procesar", archivo=ruta_dummy)

    logs_dir = Path("output/logs")
    nombre_pdf = Path(ruta_dummy).stem
    archivo_log = logs_dir / f"{nombre_pdf}.log"

    assert archivo_log.exists(), f"No se creó log individual: {archivo_log}"

    with open(archivo_log, encoding="utf-8") as f:
        contenido = f.read()
        assert "📘" in contenido or "PROCESAR" in contenido.upper()

def test_log_validacion_crea_log_por_hash(tmp_path):
    # Simula un PDF hash ficticio
    hash_doc = "abc123hash"

    ruta = tmp_path / "doc_ejemplo.pdf"
    ruta.write_text("Contenido del documento para test")

    # Registro semántico
    log_validacion(
        evento="validation_error",
        error_code="E4002",
        severity="WARNING",
        zone="abstract",
        archivo=str(ruta),
        razones=["Resumen fuera de rango: 87 palabras."],
        hash=hash_doc
    )

    # Verifica log por hash
    log_hash_file = Path("output/logs") / f"{hash_doc}.jsonl"
    assert log_hash_file.exists(), "No se creó el log por hash"

    with open(log_hash_file, encoding="utf-8") as f:
        data = json.loads(f.readline())
        assert data["error_code"] == "E4002"
        assert data["zone"] == "abstract"
        assert data["severity"] == "WARNING"
        assert "Resumen fuera de rango" in data["razones"][0]

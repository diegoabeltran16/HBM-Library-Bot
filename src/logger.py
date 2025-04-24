"""
📘 logger.py – Registro estructurado y visual para OpenPages Pipeline

Este módulo cumple dos funciones clave:
1. Registro multilingüe con salida visual (terminal) para trazabilidad en tiempo real.
2. Logging estructurado en formato JSONL para trazabilidad semántica y análisis posterior.

Incluye dos tipos de eventos:
- Eventos generales (clasificación, errores de procesamiento, etc.)
- Eventos de validación semántica (estructura, resumen, citas...)

🧬 En la Vuelta #3 se implementa log_validacion(), que permite:
- Registrar eventos ligados a zonas del documento (abstract, body, references)
- Clasificar errores por código (E4001–E4999)
- Escribir logs por ejecución y por hash de documento
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from loguru import logger

# ─────────────────────────────────────────────────────────────
# 🌍 Diccionario multilenguaje con emojis amigables
# ─────────────────────────────────────────────────────────────
MENSAJES = {
    "procesar": {
        "es": "📘 Procesando: {archivo}",
        "en": "📘 Processing: {archivo}"
    },
    "clasificado": {
        "es": "📖 Clasificado como: {categoria} ({dewey})",
        "en": "📖 Classified as: {categoria} ({dewey})"
    },
    "export_ok": {
        "es": "✔️ Exportación completa: [{archivo}]",
        "en": "✔️ Export completed: [{archivo}]"
    },
    "warning_meta": {
        "es": "⚠️ Metadatos incompletos o inválidos",
        "en": "⚠️ Incomplete or invalid metadata"
    },
    "warning_texto_corto": {
        "es": "⚠️ Texto extraído demasiado corto. Archivo omitido.",
        "en": "⚠️ Extracted text too short. Skipping file."
    },
    "error_parse": {
        "es": "❌ Error procesando archivo: {archivo}",
        "en": "❌ Error processing file: {archivo}"
    },
    "archivo_inaccesible": {
        "es": "❌ Archivo inaccesible o corrupto: {archivo}",
        "en": "❌ Unreadable or corrupt file: {archivo}"
    }
}

# ─────────────────────────────────────────────────────────────
# ⚙️ Configuración global para logs
# ─────────────────────────────────────────────────────────────
LANG = os.getenv("LANG", "es")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
EXECUTION_ID = os.getenv("EXECUTION_ID", uuid.uuid4().hex)

LOGS_DIR = Path("output/logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
global_log_txt = LOGS_DIR / f"run_{timestamp}.log"
global_log_jsonl = LOGS_DIR / f"run_{timestamp}.jsonl"

logger.remove()
logger.add(global_log_txt, level=LOG_LEVEL, format="{time} | {level} | {message}")
logger.add(global_log_jsonl, serialize=True, level=LOG_LEVEL)

# ─────────────────────────────────────────────────────────────
# 🧩 log_evento(): para eventos generales (pipeline, errores)
# ─────────────────────────────────────────────────────────────
def log_evento(evento: str, archivo: str = "", categoria: str = "", dewey: str = "", nivel: str = "INFO", **extra) -> str:
    """
    Registra un evento general en consola, archivo .log y .jsonl
    """
    global LANG
    LANG = os.getenv("LANG", "es")
    idioma = MENSAJES.get(evento, {}).get(LANG, evento)
    mensaje = idioma.format(archivo=archivo, categoria=categoria, dewey=dewey)

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "ejecucion": EXECUTION_ID,
        "evento": evento,
        "archivo": archivo,
        "categoria": categoria,
        "dewey": dewey,
        "nivel": nivel.upper(),
    }

    # Visual amigable
    print(mensaje)

    # Log plano
    try:
        logger.log(nivel.upper(), mensaje)
    except Exception as e:
        print(f"❌ Error en log plano: {e}")

    # Log estructurado
    try:
        with open(global_log_jsonl, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data) + "\n")
    except Exception as e:
        print(f"❌ Error escribiendo log estructurado: {e}")

    # Log individual por archivo
    if archivo:
        try:
            archivo_log = LOGS_DIR / f"{Path(archivo).stem}.log"
            with open(archivo_log, "a", encoding="utf-8") as f:
                f.write(f"{log_data['timestamp']} | {evento.upper()} | {mensaje}\n")
        except Exception as e:
            print(f"❌ Error escribiendo log individual: {e}")

    return mensaje

# ─────────────────────────────────────────────────────────────
# 🧬 log_validacion(): eventos semánticos AI-ready
# ─────────────────────────────────────────────────────────────
def log_validacion(evento: str, error_code: str, severity: str, zone: str, archivo: str, razones: list, hash: str = "", **kwargs):
    """
    Registra un evento de validación semántica en formato AI-ready:
    - Incluye código, severidad, zona, hash, y razones
    - Se escribe tanto en el log global como en un log exclusivo por documento (basado en hash)

    Args:
        evento: tipo de evento (debe ser 'validation_error')
        error_code: código semántico (ej: E4002)
        severity: INFO / WARNING / ERROR / CRITICAL
        zone: sección del documento afectada
        archivo: ruta al PDF original
        razones: lista con descripciones del problema
        hash: hash_md5 del documento (opcional pero recomendado)
    """
    assert evento == "validation_error", "Evento inválido para log_validacion"
    assert isinstance(razones, list) and razones, "Razones debe ser una lista no vacía"

    log_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ejecucion": EXECUTION_ID,
        "evento": evento,
        "error_code": error_code,
        "severity": severity.upper(),
        "zone": zone,
        "archivo": archivo,
        "razones": razones,
        "hash_doc": hash
    }

    # Registro principal en .jsonl global
    try:
        with open(global_log_jsonl, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data) + "\n")
    except Exception as e:
        print(f"❌ Error escribiendo validación global: {e}")

    # Registro alternativo por documento (hash)
    if hash:
        try:
            archivo_hash = LOGS_DIR / f"{hash}.jsonl"
            with open(archivo_hash, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_data) + "\n")
        except Exception as e:
            print(f"❌ Error escribiendo log por hash: {e}")

    # Mensaje en consola
    print(f"[{severity.upper()}] {zone} → {razones[0]}")

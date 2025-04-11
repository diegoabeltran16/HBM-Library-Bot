# src/logger.py

"""
📘 Logger persistente para Dewey Pipeline
Registra eventos con formato estructurado (.log y .jsonl) y visual (emoji).
Compatible con trazabilidad por corrida e integración futura.

🧱 Estructura del JSON generado (1 línea por evento):
{
    "timestamp": "2025-04-10T15:42:21.543Z",
    "ejecucion": "c78fbccbeed045b5919e8a7e79dd4d73",
    "evento": "clasificado",
    "archivo": "input/Libro.pdf",
    "categoria": "Tecnología",
    "dewey": "600",
    "nivel": "INFO"
}
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from loguru import logger

# ─────────────────────────────────────────────────────────────
# 🌍 Diccionario multilenguaje con emojis
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
# ⚙️ Configuración global y persistencia
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
# 🧩 Función principal de logging
# ─────────────────────────────────────────────────────────────
def log_evento(evento: str, archivo: str = "", categoria: str = "", dewey: str = "", nivel: str = "INFO"):
    idioma = MENSAJES.get(evento, {}).get(LANG, evento)
    mensaje = idioma.format(archivo=archivo, categoria=categoria, dewey=dewey)

    # Visual amigable (terminal)
    print(mensaje)

    # Entrada estructurada
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "ejecucion": EXECUTION_ID,
        "evento": evento,
        "archivo": archivo,
        "categoria": categoria,
        "dewey": dewey,
        "nivel": nivel.upper(),
    }

    # Log .log plano
    try:
        logger.log(nivel.upper(), mensaje)
    except Exception as e:
        print(f"❌ Error escribiendo en log plano: {e}")

    # Log .jsonl
    try:
        with open(global_log_jsonl, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data) + "\n")
    except Exception as e:
        print(f"❌ Error escribiendo en log JSONL: {e}")

    # Log individual por archivo
    if archivo:
        try:
            archivo_log = LOGS_DIR / f"{Path(archivo).stem}.log"
            with open(archivo_log, "a", encoding="utf-8") as f:
                f.write(f"{log_data['timestamp']} | {evento.upper()} | {mensaje}\n")
        except Exception as e:
            print(f"❌ Error escribiendo log individual: {e}")

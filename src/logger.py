# src/logger.py

import os

# ─────────────────────────────────────────────────────────────
# 🌍 Diccionario de mensajes multilenguaje
# ─────────────────────────────────────────────────────────────
MENSAJES = {
    "export_ok": {
        "es": "✔️ Exportación completa: [{archivo}]\n📚 Categoría: {categoria} ({dewey})",
        "en": "✔️ Export completed: [{archivo}]\n📚 Category: {categoria} ({dewey})"
    },
    "clasificacion": {
        "es": "📖 Clasificado como: {categoria} ({dewey})",
        "en": "📖 Classified as: {categoria} ({dewey})"
    },
    "formato_descartado": {
        "es": "⚠️ Línea descartada por posible fórmula o ruido visual.",
        "en": "⚠️ Line discarded due to formula or visual noise."
    },
    "parser_error": {
        "es": "❌ Error al procesar el archivo: {archivo}",
        "en": "❌ Error processing file: {archivo}"
    },
    "salida_creada": {
        "es": "📁 Archivos exportados en carpeta /output",
        "en": "📁 Files exported to /output folder"
    }
}

# ─────────────────────────────────────────────────────────────
# 🧩 Función principal de logging
# ─────────────────────────────────────────────────────────────
def log_mensaje(evento, archivo=None, categoria=None, dewey=None):
    """
    Muestra un mensaje visual en el idioma elegido vía ENV.
    Admite íconos, categorías y personalización según contexto.
    """
    idioma = os.getenv("LANG", "es")

    if evento not in MENSAJES:
        print(f"⚠️ Evento desconocido: {evento}")
        return

    mensaje = MENSAJES[evento].get(idioma, MENSAJES[evento]["es"])  # fallback a español

    # Rellenar placeholders
    mensaje_formateado = mensaje.format(
        archivo=archivo or "archivo.pdf",
        categoria=categoria or "Desconocida",
        dewey=dewey or "000"
    )

    print(mensaje_formateado)

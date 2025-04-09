# main.py

"""
Script principal del Dewey Pipeline 🧠📘

Procesa todos los archivos PDF dentro de /input
y genera versiones limpias, clasificadas y exportadas
en /output como .txt, .md y .jsonl.
"""

import os
from pathlib import Path

from src.parser import extract_text
from src.cleaner import limpiar_texto_completo
from src.classifier import clasificar_documento
from src.exporter import exportar_archivos
from src.logger import log_mensaje

# Directorio donde están los PDFs a procesar
INPUT_DIR = "input"

def main():
    print("🚀 Iniciando Dewey Pipeline...")
    archivos_pdf = [f for f in Path(INPUT_DIR).glob("*.pdf")]

    if not archivos_pdf:
        print("⚠️  No se encontraron archivos PDF en la carpeta 'input/'")
        return

    print(f"🔍 Se encontraron {len(archivos_pdf)} archivos para procesar.")

    for archivo in archivos_pdf:
        ruta = str(archivo)
        nombre_archivo = archivo.stem  # sin la extensión .pdf

        try:
            # 1️⃣ Extracción inteligente
            texto_crudo = extract_text(ruta)

            # 2️⃣ Limpieza profunda y opcionalmente modo Markdown
            texto_limpio = limpiar_texto_completo(texto_crudo, modo_md=True)

            # 3️⃣ Clasificación temática y metadatos
            tipo, categoria, dewey, titulo, autor = clasificar_documento(texto_limpio)

            # 4️⃣ Exportar en los tres formatos
            exportar_archivos(tipo, titulo, texto_limpio, categoria, dewey, autor)

            # 5️⃣ Mostrar feedback amigable
            log_mensaje("clasificacion", ruta, categoria, dewey)
            log_mensaje("export_ok", ruta)

        except Exception as e:
            log_mensaje("error", ruta, detalle=str(e))

    print("✅ Pipeline finalizado con éxito.")

# Punto de entrada
if __name__ == "__main__":
    main()

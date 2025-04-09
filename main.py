# main.py

"""
Script principal del Dewey Pipeline 🧠📘
Procesa todos los archivos PDF dentro de /input/** y genera salidas en /output
"""

import os
from pathlib import Path

from src.parser import extract_text
from src.cleaner import limpiar_texto_completo
from src.classifier import clasificar_documento
from src.exporter import exportar_archivos
from src.logger import log_mensaje

INPUT_DIR = "input"

def main():
    print("🚀 Iniciando Dewey Pipeline...")

    # Buscar archivos PDF recursivamente
    archivos_pdf = list(Path(INPUT_DIR).rglob("*.pdf"))

    if not archivos_pdf:
        print("⚠️  No se encontraron archivos PDF en la carpeta 'input/'")
        return

    print(f"🔍 Se encontraron {len(archivos_pdf)} archivos para procesar.")

    for archivo in archivos_pdf:
        ruta = str(archivo)
        nombre_archivo = archivo.stem

        try:
            # 1️⃣ Extracción de texto
            texto_crudo = extract_text(ruta)

            # 2️⃣ Limpieza profunda
            texto_limpio = limpiar_texto_completo(texto_crudo, modo_md=True)

            # 3️⃣ Clasificación y metadatos
            resultado = clasificar_documento(texto_limpio)
            tipo = Path(archivo).parent.name  # nombre de carpeta como tipo
            categoria = resultado["categoria"]
            dewey = resultado["dewey"]
            titulo = resultado["titulo"]
            autor = resultado["autor"]

            # 4️⃣ Exportar
            exportar_archivos(tipo, titulo, texto_limpio, categoria, dewey, autor)

            # 5️⃣ Logs
            log_mensaje("clasificacion", ruta, categoria, dewey)
            log_mensaje("export_ok", ruta)

        except Exception as e:
            print(f"❌ Error procesando {ruta}: {e}")
            log_mensaje("error", archivo.name)

    print("✅ Pipeline finalizado con éxito.")

if __name__ == "__main__":
    main()

# main.py

"""
Script principal del Dewey Pipeline 🧠📘

Este script recorre todos los archivos PDF en /input, ejecuta el pipeline completo (extracción, limpieza, clasificación, exportación)
y registra eventos importantes mediante el módulo logger.

📘 Para más información sobre el sistema de logging:
Ver README.logger.md
"""

import os
from pathlib import Path

from src.parser import extract_text
from src.cleaner import limpiar_texto_completo
from src.classifier import clasificar_documento
from src.exporter import exportar_archivos
from src.logger import log_evento  # <- Logger central visual + persistente

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def main():
    print("🚀 Iniciando Dewey Pipeline...")

    # ✅ Validación inicial de carpetas
    if not Path(INPUT_DIR).exists():
        raise FileNotFoundError(f"El directorio de entrada '{INPUT_DIR}' no existe.")
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    archivos_pdf = list(Path(INPUT_DIR).rglob("*.pdf"))
    if not archivos_pdf:
        print("⚠️ No se encontraron archivos PDF en la carpeta 'input/'")
        return

    print(f"🔍 Se encontraron {len(archivos_pdf)} archivos para procesar.")

    resumen = {"procesados": 0, "omitidos": 0, "errores": 0}

    for archivo in archivos_pdf:
        ruta = str(archivo)
        tipo = Path(archivo).parent.name  # Carpeta como tipo

        # 🔐 Verificar accesibilidad física del archivo
        try:
            with open(ruta, "rb") as f:
                f.read(4)
        except Exception:
            log_evento("archivo_inaccesible", archivo=ruta, nivel="ERROR")
            resumen["errores"] += 1
            continue

        try:
            # 1️⃣ Registro de inicio
            log_evento("procesar", archivo=ruta)

            # 2️⃣ Extracción de texto
            texto_crudo = extract_text(ruta)

            # 3️⃣ Limpieza
            texto_limpio = limpiar_texto_completo(texto_crudo, modo_md=True)

            if len(texto_limpio.strip()) < 300:
                log_evento("warning_texto_corto", archivo=ruta, nivel="WARNING")
                resumen["omitidos"] += 1
                continue

            # 4️⃣ Clasificación
            resultado = clasificar_documento(texto_limpio)
            categoria = resultado.get("categoria")
            dewey = resultado.get("dewey")
            titulo = resultado.get("titulo")
            autor = resultado.get("autor")

            # 5️⃣ Validación de metadatos
            if not all([titulo, autor, categoria, dewey]):
                log_evento("warning_meta", archivo=ruta, nivel="WARNING")
                resumen["omitidos"] += 1
                continue

            # 6️⃣ Exportación
            exportar_archivos(tipo, titulo, texto_limpio, categoria, dewey, autor)

            # 7️⃣ Logs estructurados
            log_evento("clasificado", archivo=ruta, categoria=categoria, dewey=dewey)
            log_evento("export_ok", archivo=ruta, categoria=categoria, dewey=dewey)
            resumen["procesados"] += 1

        except Exception as e:
            log_evento("error_parse", archivo=ruta, nivel="ERROR")
            print(f"❌ Error procesando {ruta}: {e}")
            resumen["errores"] += 1

    # 🔚 Informe final
    print(f"""
🔚 Resumen del Pipeline:
✔️ Procesados: {resumen['procesados']}
⚠️ Omitidos: {resumen['omitidos']}
❌ Errores: {resumen['errores']}
""")

if __name__ == "__main__":
    main()

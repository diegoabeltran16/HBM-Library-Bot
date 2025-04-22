"""
Script principal del OpenPages-pipeline 🧠📘
Procesa todos los archivos PDF dentro de /input/** y genera salidas en /output
"""

import os
import argparse
from pathlib import Path

from src.parser import extract_text
from src.cleaner import limpiar_texto_completo
from src.enhancer import enriquecer_texto
from src.classifier import clasificar_documento
from src.exporter import exportar_archivos
from src.logger import log_evento
from src.validator import validar_documento

# Forzar idioma visual en consola
os.environ["LANG"] = "es"

INPUT_DIR = "input"

def main(debug=False):
    print("🚀 Iniciando Dewey Pipeline...")

    archivos_pdf = list(Path(INPUT_DIR).rglob("*.pdf"))
    if not archivos_pdf:
        print("⚠️  No se encontraron archivos PDF en la carpeta 'input/'")
        return

    print(f"🔍 Se encontraron {len(archivos_pdf)} archivos para procesar.")

    resumen = {
        "procesados": 0,
        "omitidos": 0,
        "errores": 0
    }

    for archivo in archivos_pdf:
        ruta = str(archivo)
        nombre_archivo = archivo.stem
        tipo = Path(archivo).parent.name  # Carpeta como tipo (Book, Essay, etc.)

        try:
            print(f"\n📘 Procesando: {ruta}")
            # 1 Extraer texto
            texto_crudo = extract_text(ruta)
            log_evento("procesar", archivo=ruta)

            # 2️ Limpiar texto
            texto_limpio = limpiar_texto_completo(texto_crudo, modo_md=True)

            # 3 Enriquecer texto (reparar cid, normalizar unicode, marcar dudosos)
            texto_enriquecido = enriquecer_texto(texto_limpio, archivo=ruta, debug=debug)

            # 4 Clasificar
            resultado = clasificar_documento(texto_enriquecido)
            categoria = resultado.get("categoria")
            dewey = resultado.get("dewey")
            titulo = resultado.get("titulo")
            autor = resultado.get("autor")

            print(f"📖 Clasificado como: {categoria} ({dewey})")
            print(f"📝 Título: {titulo or '[Sin título]'} | Autor: {autor or '[Sin autor]'}")

            # 5 Validar documento completo
            es_valido, info = validar_documento(texto_enriquecido, titulo, autor)
            if not es_valido:
                log_evento("warning_meta", archivo=ruta, nivel="WARNING", razones=info.get("razones", []))
                print(f"⚠️  Documento omitido: {info.get('razones', [])}")
                resumen["omitidos"] += 1
                continue

            # 6 Exportar
            exportar_archivos(tipo, titulo, texto_enriquecido, categoria, dewey, autor)

            # 7 Logging visual + estructurado
            log_evento("clasificado", archivo=ruta, categoria=categoria, dewey=dewey, nombre=nombre_archivo)
            log_evento("export_ok", archivo=ruta, categoria=categoria, dewey=dewey)
            resumen["procesados"] += 1

        except Exception as e:
            log_evento("error_parse", archivo=ruta, nivel="ERROR", mensaje=str(e))
            print(f"❌ Error procesando {ruta}: {e}")
            resumen["errores"] += 1

    print(f"""
📊 Resumen del Pipeline:
          ✔️ Procesados: {resumen['procesados']}
          ⚠️ Omitidos: {resumen['omitidos']}
          ❌ Errores: {resumen['errores']}
""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dewey Pipeline – Procesador de PDFs enriquecidos")
    parser.add_argument("--debug", action="store_true", help="Muestra pre/post enriquecimiento")
    args = parser.parse_args()

    main(debug=args.debug)

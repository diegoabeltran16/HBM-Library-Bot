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
from src.utils import calcular_hash_md5  # Para trazabilidad única del documento

# Forzar idioma visual en consola a español
os.environ["LANG"] = "es"

INPUT_DIR = "input"

def main(debug: bool = False):
    print("🚀 Iniciando Dewey Pipeline...")

    archivos_pdf = list(Path(INPUT_DIR).rglob("*.pdf"))
    if not archivos_pdf:
        print("⚠️ No se encontraron archivos PDF en la carpeta 'input/'")
        return

    total = len(archivos_pdf)
    errores = 0
    procesados = 0

    if debug:
        print(f"🔍 Se encontraron {total} archivos para procesar.")

    for archivo in archivos_pdf:
        ruta = str(archivo)
        try:
            # Extracción y logging inicial
            if debug:
                print(f"\n📘 Procesando: {ruta}")
            texto_crudo = extract_text(ruta)
            log_evento("procesar", archivo=ruta)

            # Limpieza y enriquecimiento
            texto_limpio = limpiar_texto_completo(texto_crudo, modo_md=True)
            texto_enriquecido = enriquecer_texto(texto_limpio, archivo=ruta, debug=debug)

            # Clasificación
            resultado = clasificar_documento(texto_enriquecido)
            categoria = resultado.get("categoria")
            dewey = resultado.get("dewey")
            titulo = resultado.get("titulo")
            autor = resultado.get("autor")
            print(f"📖 Clasificado como: {categoria} ({dewey})")
            print(f"📝 Título: {titulo or '[Sin título]'} | Autor: {autor or '[Sin autor]'}")

            # Hash para trazabilidad
            hash_doc = calcular_hash_md5(ruta)

            # Validación semántica (solo logging, no omitir)
            es_valido, info = validar_documento(texto_enriquecido, ruta, hash_doc)
            if debug and info.get('razones'):
                for razon in info['razones']:
                    print(f"⚠️ {razon}")

            # Exportar siempre
            exportar_archivos(
                tipo=Path(archivo).parent.name,
                titulo=titulo,
                texto=texto_enriquecido,
                categoria=categoria,
                dewey=dewey,
                autor=autor,
                hash_doc=hash_doc
            )

            # Logging final
            log_evento("clasificado", archivo=ruta, categoria=categoria, dewey=dewey)
            log_evento("export_ok", archivo=ruta, categoria=categoria, dewey=dewey)
            procesados += 1

        except Exception as e:
            errores += 1
            log_evento("error_parse", archivo=ruta, nivel="ERROR", mensaje=str(e))
            if debug:
                print(f"❌ Error procesando {ruta}: {e}")

    # Resumen final en estilo multilinea
    print(f"""
📊 Resumen del Pipeline:
  ✔️ Procesados: {procesados}
  ❌ Errores: {errores}
""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dewey Pipeline – Procesador de PDFs enriquecidos")
    parser.add_argument(
        "--debug", action="store_true",
        help="Muestra detalles de cada paso del pipeline"
    )
    args = parser.parse_args()

    main(debug=args.debug)

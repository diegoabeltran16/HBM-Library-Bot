"""
📦 exporter.py – Exportación estructurada y AI-ready para OpenPages Pipeline
"""
from pathlib import Path
import json
import re

# Carpeta de salida base
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ────────────────────────────────────────────────
# 🔣 Función de slugificación
# ────────────────────────────────────────────────
def slugify(texto: str) -> str:
    """
    Convierte cualquier texto en un slug amigable para nombres de carpeta.
    """
    texto = texto or "sin_titulo"
    texto = texto.lower()
    texto = re.sub(r"[^\w\s-]", "", texto)
    texto = re.sub(r"[\s_-]+", "-", texto).strip('-')
    return texto

# ────────────────────────────────────────────────
# 📤 Exportador principal
# ────────────────────────────────────────────────
def exportar_archivos(
    tipo: str,
    titulo: str,
    texto: str,
    categoria: str,
    dewey: str,
    autor: str = "",
    hash_doc: str = ""
):
    """
    Exporta el texto procesado en .txt, .md y .jsonl,
    dentro de output/{slug_tipo}/{slug_titulo}_{hash_doc}/
    """
    if not hash_doc:
        raise ValueError("Se requiere un hash único para la exportación por documento.")

    tipo_slug = slugify(tipo)
    titulo_slug = slugify(titulo)
    carpeta = OUTPUT_DIR / tipo_slug / f"{titulo_slug}_{hash_doc}"
    carpeta.mkdir(parents=True, exist_ok=True)

    # Archivos de salida
    ruta_txt   = carpeta / f"{hash_doc}.txt"
    ruta_md    = carpeta / f"{hash_doc}.md"
    ruta_jsonl = carpeta / f"{hash_doc}.jsonl"

    # Guardar contenido
    _guardar_txt(ruta_txt, texto)
    _guardar_md(ruta_md, texto, titulo, autor, categoria, dewey)
    _guardar_jsonl(ruta_jsonl, texto, hash_doc, categoria, dewey)

# ────────────────────────────────────────────────
# 📄 Helpers de guardado
# ────────────────────────────────────────────────
def _guardar_txt(ruta: Path, texto: str):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)

def _guardar_md(ruta: Path, texto: str, titulo: str, autor: str, categoria: str, dewey: str):
    encabezado = (
        "---\n"
        f"titulo: {titulo or 'Sin título'}\n"
        f"autor: {autor or 'Desconocido'}\n"
        f"categoria: {categoria}\n"
        f"dewey: {dewey}\n"
        "---\n\n"
    )
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(encabezado + texto)

def _guardar_jsonl(ruta: Path, texto: str, hash_doc: str, categoria: str, dewey: str):
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    with open(ruta, "w", encoding="utf-8") as f:
        for i, p in enumerate(parrafos):
            linea = {
                "id": hash_doc,
                "index": i,
                "paragraph": p,
                "categoria": categoria,
                "dewey": dewey
            }
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")

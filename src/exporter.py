# src/exporter.py

from pathlib import Path
import json
import re

# ────────────────────────────────────────────────
# 📂 Carpeta de salida configurable (por ahora fija)
# ────────────────────────────────────────────────
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ────────────────────────────────────────────────
# 📤 Exportador principal
# ────────────────────────────────────────────────
def exportar_archivos(tipo: str, nombre_base: str, texto: str, categoria: str, dewey: str, autores: str = ""):
    """
    Exporta el texto en .txt, .md y .jsonl con nombre estructurado:
    tipo_dewey_categoria_nombre_autores
    """
    if not texto or not tipo or not categoria or not nombre_base:
        raise ValueError("Faltan datos requeridos para exportar.")

    tipo = limpiar_nombre(tipo)
    categoria = limpiar_nombre(categoria)
    nombre_base = limpiar_nombre(nombre_base)
    autores = limpiar_nombre(autores)

    nombre_final = f"{tipo}_{dewey}_{categoria}_{nombre_base}"
    if autores:
        nombre_final += f"_{autores}"

    guardar_txt(nombre_final, texto)
    guardar_md(nombre_final, texto, categoria, dewey)
    guardar_jsonl(nombre_final, texto)


# ────────────────────────────────────────────────
# 📄 Exportar .txt
# ────────────────────────────────────────────────
def guardar_txt(nombre_base: str, texto: str):
    ruta = OUTPUT_DIR / f"{nombre_base}.txt"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)


# ────────────────────────────────────────────────
# 📝 Exportar .md con metadatos
# ────────────────────────────────────────────────
def guardar_md(nombre_base: str, texto: str, categoria: str, dewey: str):
    ruta = OUTPUT_DIR / f"{nombre_base}.md"
    encabezado = f"""---
categoria: {categoria.replace("_", " ")}
dewey: {dewey}
---

"""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(encabezado + texto)


# ────────────────────────────────────────────────
# 🔣 Exportar .jsonl por párrafo
# ────────────────────────────────────────────────
def guardar_jsonl(nombre_base: str, texto: str):
    ruta = OUTPUT_DIR / f"{nombre_base}.jsonl"
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    with open(ruta, "w", encoding="utf-8") as f:
        for p in parrafos:
            json_line = json.dumps({"paragraph": p}, ensure_ascii=False)
            f.write(json_line + "\n")


# ────────────────────────────────────────────────
# 🧼 Limpiar nombres de archivo
# ────────────────────────────────────────────────
def limpiar_nombre(nombre: str) -> str:
    """
    Limpia caracteres no válidos y convierte a snake_case amigable.
    """
    nombre = re.sub(r"[^\w\s-]", "", nombre)
    nombre = re.sub(r"[\s-]+", "_", nombre)
    return nombre.strip().lower()

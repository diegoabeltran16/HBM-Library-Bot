"""
📦 Tiddler Exporter – scripts/tiddler_exporter.py

Este módulo recorre los archivos fuente del proyecto, detecta cambios mediante hashes,
extrae etiquetas (tags) automáticamente en base a la ruta y extensión, y exporta un archivo
por cada entrada como tiddler individual en formato JSON, listo para importar en TiddlyWiki.

🔒 100% en Python, sin dependencias externas. Ideal para documentación viva, visual y offline.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List

# ==========================
# ⚙️ CONFIGURACIÓN GENERAL
# ==========================

ROOT_DIR = Path(__file__).resolve().parents[1]  # raíz del proyecto
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "tiddlers-export"
HASH_FILE = SCRIPT_DIR / ".hashes.json"

VALID_EXTENSIONS = ['.py', '.md', '.json', '.sh', '.html', '.css']
IGNORE_DIRS = ['.git', '__pycache__', 'venv', 'dist', 'node_modules', 'output', 'tests']

LANGUAGE_MAP = {
    '.py': 'python',
    '.md': 'markdown',
    '.json': 'json',
    '.sh': 'bash',
    '.html': 'html',
    '.css': 'css'
}

TAG_MAP = [
    {"dir": "src", "tag": "[[--- Codigo]]"},
    {"dir": "tests", "tag": "[[--- Test]]"},
    {"dir": "scripts", "tag": "[[--- Automatizacion]]"},
    {"ext": ".md", "tag": "[[--- Documentacion]]"},
    {"ext": ".py", "tag": "[[Python]]"},
    {"ext": ".json", "tag": "[[JSON]]"},
    {"ext": ".sh", "tag": "[[Shell]]"},
]

# ==============================
# 🔎 FUNCIONES AUXILIARES
# ==============================

def get_all_files(directory: Path) -> List[Path]:
    """Recorre recursivamente el proyecto y devuelve los archivos válidos."""
    all_files = []
    for root, dirs, files in os.walk(directory):
        # Ignorar carpetas no deseadas
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            ext = Path(file).suffix
            if ext in VALID_EXTENSIONS:
                all_files.append(Path(root) / file)
    return all_files

def get_hash(content: str) -> str:
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

def detect_tags(file_path: Path) -> List[str]:
    """Asigna tags automáticamente según carpeta o extensión."""
    tags = []
    rel_path = str(file_path.relative_to(ROOT_DIR))
    for rule in TAG_MAP:
        if rule.get("dir") and f"/{rule['dir']}/" in rel_path:
            tags.append(rule["tag"])
        if rule.get("ext") and rel_path.endswith(rule["ext"]):
            tags.append(rule["tag"])
    return list(set(tags))  # evitar duplicados

def safe_title(path: Path) -> str:
    """Convierte la ruta del archivo en un título válido para TiddlyWiki."""
    return str(path.relative_to(ROOT_DIR)).replace(os.sep, '_')

# ==============================
# 🚀 EXPORTADOR PRINCIPAL
# ==============================

def export_tiddlers(dry_run=False):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if HASH_FILE.exists():
        with open(HASH_FILE, 'r', encoding='utf-8') as f:
            old_hashes = json.load(f)
    else:
        old_hashes = {}

    new_hashes = {}
    changed_files = []

    for file_path in get_all_files(ROOT_DIR):
        rel_path = str(file_path.relative_to(ROOT_DIR))
        ext = file_path.suffix
        lang = LANGUAGE_MAP.get(ext, 'text')
        content = file_path.read_text(encoding='utf-8')
        hash_now = get_hash(content)
        new_hashes[rel_path] = hash_now

        if old_hashes.get(rel_path) == hash_now:
            continue  # sin cambios

        tags = detect_tags(file_path)
        title = safe_title(file_path)

        # 🧠 Contenido markdown con tags visuales arriba
        text_block = f"## [[Tags]]\n{' '.join(tags)}\n\n```{lang}\n{content}\n```"

        tiddler = {
            "title": title,
            "text": text_block,
            "tags": ' '.join(tags),
            "type": "text/markdown",
            "created": datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:17],
            "modified": datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:17],
        }

        if dry_run:
            print(f"[dry-run] Detectado cambio en: {rel_path}")
            continue

        out_file = OUTPUT_DIR / f"{title}.json"
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(tiddler, f, indent=2, ensure_ascii=False)

        changed_files.append(rel_path)

    if not dry_run:
        with open(HASH_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_hashes, f, indent=2)

    print(f"\n📦 Archivos modificados: {len(changed_files)}")
    if changed_files:
        for path in changed_files:
            print(f"  ✅ Exportado: {path}")
    else:
        print("  🔁 Sin cambios detectados.")

# ==============================
# 🧪 ENTRADA DIRECTA (CLI SIMPLE)
# ==============================

if __name__ == "__main__":
    import sys
    dry = '--dry-run' in sys.argv
    export_tiddlers(dry_run=dry)

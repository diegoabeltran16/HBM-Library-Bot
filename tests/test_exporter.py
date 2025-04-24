import sys
import hashlib
import shutil
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.exporter import exportar_archivos, slugify

def test_exportar_archivos_crea_todos_los_formatos(tmp_path):
    # 📄 Crear PDF falso para simular entrada
    pdf_path = tmp_path / "fake_doc.pdf"
    pdf_path.write_text("Simulado")

    texto = "Este es un párrafo.\n\nEste es otro."
    titulo = "Documento de Prueba"
    autor = "Ana María"
    tipo = "Essay"
    categoria = "Filosofía"
    dewey = "100"

    # 🧬 Calcular hash simulado
    hash_doc = hashlib.md5("Simulado".encode("utf-8")).hexdigest()

    # 📦 Ejecutar exportación
    exportar_archivos(tipo, titulo, texto, categoria, dewey, autor, hash_doc)

    tipo_slug = slugify(tipo)
    titulo_slug = slugify(titulo)
    base_path = Path("output") / tipo_slug / f"{titulo_slug}_{hash_doc}"

    assert base_path.exists(), "No se creó la carpeta por documento"

    for ext in [".txt", ".md", ".jsonl"]:
        archivo = base_path / f"{hash_doc}{ext}"
        assert archivo.exists(), f"Falta el archivo: {archivo}"
        assert archivo.stat().st_size > 0, f"Archivo vacío: {archivo}"

    # 🔐 Cierre explícito y limpieza solo si no está en uso
    try:
        for archivo in base_path.glob("*"):
            archivo.unlink()
        base_path.rmdir()
        base_path.parent.rmdir()
    except PermissionError as e:
        print(f"⚠️ No se pudo limpiar completamente por permisos: {e}")

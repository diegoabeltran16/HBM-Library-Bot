# tests/test_exporter.py
import sys
from pathlib import Path
from pathlib import Path
from src.exporter import exportar_archivos, limpiar_nombre

# 🔧 Asegura que src/ sea visible desde cualquier entorno
sys.path.append(str(Path(__file__).resolve().parents[1]))

def test_exportar_archivos_crea_todos_los_formatos():
    tipo = "Essay"
    nombre = "Prueba de Exportación"
    texto = "Párrafo 1.\n\nPárrafo 2."
    categoria = "Philosophy and Psychology"
    dewey = "100"
    autores = "Jane Doe"

    # Construir nombre_base con la misma lógica del exporter
    nombre_base = "_".join([
        limpiar_nombre(tipo),
        dewey,
        limpiar_nombre(categoria),
        limpiar_nombre(nombre),
        limpiar_nombre(autores)
    ])

    output_dir = Path("output")
    extensiones = [".txt", ".md", ".jsonl"]

    exportar_archivos(tipo, nombre, texto, categoria, dewey, autores)

    for ext in extensiones:
        path = output_dir / f"{nombre_base}{ext}"
        assert path.exists(), f"Falta el archivo: {path}"
        assert path.stat().st_size > 0, f"Archivo vacío: {path}"
        path.unlink()  # Limpieza

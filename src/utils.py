# src/utils.py

"""
Funciones auxiliares para soporte al parser:
- Evaluación de complejidad estructural de un PDF
- Detección de fórmulas matemáticas u objetos sospechosos
"""

import fitz
import re

def es_pdf_complejo(ruta_pdf):
    """
    Usa PyMuPDF para contar bloques de texto en la primera página.
    Si hay muchos bloques, se asume layout complejo (columnas, tablas...).
    """
    doc = fitz.open(ruta_pdf)
    primera = doc[0]
    bloques = primera.get_text("blocks")
    doc.close()

    return len(bloques) > 10


def contiene_formula(texto):
    """
    Heurística básica para detectar texto con alta densidad de símbolos matemáticos.
    También descarta contenido muy corto (posibles imágenes o símbolos aislados).
    """
    if not texto or len(texto.strip()) < 10:
        return True  # Posiblemente una imagen sin texto

    simbolos = re.findall(r"[^a-zA-Z0-9\s]", texto)
    proporcion = len(simbolos) / len(texto)

    return proporcion > 0.3  # Más del 30% símbolos → se descarta

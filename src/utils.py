"""
Funciones auxiliares para soporte al parser:
- Evaluación de complejidad estructural de un PDF
- Detección de fórmulas matemáticas u objetos sospechosos
- Normalización de texto para búsqueda semántica
"""

from unidecode import unidecode
import fitz
import re

def es_pdf_complejo(ruta_pdf, max_paginas=3, umbral=8):
    """
    Determina si un PDF es complejo por su estructura visual:
    - Muchos bloques (columnas, tablas, secciones)
    - O bien, sin bloques (imagen o escaneado)

    Esto permite activar estrategias especiales como OCR o fallback.

    Retorna:
    - True si el PDF es complejo por layout o ausencia de texto
    """
    doc = fitz.open(ruta_pdf)
    paginas = min(len(doc), max_paginas)
    total_bloques = 0

    for i in range(paginas):
        bloques = doc[i].get_text("blocks")
        total_bloques += len(bloques)

    doc.close()

    if total_bloques == 0:
        return True  # Escaneado o sin texto detectable

    promedio = total_bloques / paginas
    return promedio > umbral


def contiene_formula(texto):
    """
    Detecta líneas con alta densidad de símbolos matemáticos.
    También filtra entradas muy cortas (probables imágenes).
    """
    if not texto or len(texto.strip()) < 10:
        return True

    simbolos = re.findall(r"[^a-zA-Z0-9\s]", texto)
    proporcion = len(simbolos) / len(texto)

    return proporcion > 0.3


def normalizar_texto(texto: str) -> str:
    """
    Convierte a minúsculas y remueve acentos. Ideal para matching.
    """
    return unidecode(texto.lower())

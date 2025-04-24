"""
🧩 utils.py – Funciones auxiliares para el análisis estructural y semántico de documentos PDF

Este módulo cumple el rol de "gen auxiliar" dentro del pipeline OpenPages.
Proporciona funciones reutilizables que permiten:
- Evaluar la complejidad visual de un PDF (bloques o escaneado)
- Detectar posibles fórmulas u objetos no textuales
- Normalizar texto para matching semántico
- Calcular un hash único (MD5) que actúa como identificador genético del documento

Todas las funciones están diseñadas para ser:
✔️ Independientes
✔️ Trazables
✔️ Reutilizables
✔️ Seguras ante errores comunes
"""

from unidecode import unidecode
import fitz  # PyMuPDF
import re
import hashlib


def es_pdf_complejo(ruta_pdf: str, max_paginas: int = 3, umbral: int = 8) -> bool:
    """
    Evalúa si un PDF es "complejo" en su estructura visual.

    Criterios:
    - Muchos bloques detectados (posible layout complicado: columnas, tablas)
    - Ningún bloque visible (posible imagen o escaneado)

    Args:
        ruta_pdf: Ruta local del archivo PDF.
        max_paginas: Número de páginas a analizar (default: 3).
        umbral: Cantidad promedio de bloques para considerarlo complejo.

    Returns:
        True si el PDF es complejo, False si es "simple".
    """
    try:
        doc = fitz.open(ruta_pdf)
    except Exception as e:
        print(f"❌ Error abriendo PDF: {e}")
        return True  # Por defecto, tratamos como complejo si no se puede abrir

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


def contiene_formula(texto: str) -> bool:
    """
    Detecta si un bloque de texto contiene fórmulas u objetos sospechosos,
    usando la proporción de símbolos no alfabéticos como indicador.

    También filtra textos demasiado cortos.

    Args:
        texto: Fragmento de texto (párrafo o línea).

    Returns:
        True si parece contener fórmula o es sospechoso, False si es texto normal.
    """
    if not texto or len(texto.strip()) < 10:
        return True

    simbolos = re.findall(r"[^a-zA-Z0-9\s]", texto)
    proporcion = len(simbolos) / len(texto)

    return proporcion > 0.3


def normalizar_texto(texto: str) -> str:
    """
    Limpieza semántica del texto para búsquedas y comparación.

    Acciones:
    - Convierte a minúsculas
    - Elimina acentos y caracteres especiales (via unidecode)

    Args:
        texto: Cualquier string

    Returns:
        Texto normalizado, listo para matching semántico
    """
    return unidecode(texto.lower())


def calcular_hash_md5(path_pdf: str) -> str:
    """
    Calcula el hash MD5 único de un archivo PDF.

    Usado para:
    - Trazabilidad de documentos
    - Nombrado de logs
    - Identificación genética en IA-ready exports

    Args:
        path_pdf: Ruta absoluta al archivo

    Returns:
        Cadena hexadecimal (32 caracteres)
    """
    try:
        with open(path_pdf, 'rb') as f:
            contenido = f.read()
            return hashlib.md5(contenido).hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(f"⚠️ Archivo no encontrado para hashing: {path_pdf}")

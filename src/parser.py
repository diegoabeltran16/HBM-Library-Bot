# src/parser.py

"""
Este módulo se encarga de extraer texto de archivos PDF usando la librería más adecuada
según su estructura. Integra PyMuPDF para PDFs simples y pdfplumber para casos complejos.
También filtra bloques sospechosos como fórmulas matemáticas o imágenes.
"""

from .cleaner import limpiar_texto
from .utils import es_pdf_complejo, contiene_formula

def extract_text(ruta_pdf):
    """
    Punto de entrada principal del parser. Decide el extractor adecuado
    y retorna el texto limpio y usable.
    """
    if es_pdf_complejo(ruta_pdf):
        texto_crudo = extract_with_pdfplumber(ruta_pdf)
    else:
        texto_crudo = extract_with_pymupdf(ruta_pdf)

    return limpiar_texto(texto_crudo)


def extract_with_pymupdf(ruta_pdf):
    """
    Extrae texto con PyMuPDF, ideal para PDFs simples y rápidos.
    Filtra bloques vacíos y con símbolos sospechosos.
    """
    import fitz
    texto = []
    doc = fitz.open(ruta_pdf)

    for page in doc:
        contenido = page.get_text()
        if contiene_formula(contenido):
            continue
        texto.append(contenido)

    doc.close()
    return "\n".join(texto)


def extract_with_pdfplumber(ruta_pdf):
    """
    Extrae texto con pdfplumber, más robusto para PDFs con múltiples columnas o tablas.
    También filtra fórmulas y bloques sospechosos.
    """
    import pdfplumber
    texto = []

    with pdfplumber.open(ruta_pdf) as pdf:
        for page in pdf.pages:
            contenido = page.extract_text()
            if contiene_formula(contenido):
                continue
            texto.append(contenido)

    return "\n".join(texto)

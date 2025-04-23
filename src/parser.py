from pathlib import Path
import fitz  # PyMuPDF
import pdfplumber
from src.cleaner import limpiar_texto
from src.ocr import ocr_completo_inteligente

# ---
# 📦 parser.py – Núcleo de extracción de texto
#
# Este módulo decide cómo extraer texto desde un PDF:
# - Si el PDF contiene texto "normal", usa PyMuPDF o pdfplumber.
# - Si detecta que el PDF está escaneado (imágenes), activa el gen OCR.
#
# 🧠 Reflexiones para futuras mutaciones:
# - ¿Deberíamos permitir forzar el uso de OCR manualmente?
# - ¿Y si combinamos texto extraído + OCR como capas complementarias?
# - ¿Podemos estimar idioma del PDF para OCR más preciso automáticamente?

# Heurística: si el texto extraído es muy corto, probablemente sea un PDF escaneado
THRESHOLD_MIN_CARACTERES = 100


def es_pdf_complejo(ruta_pdf: str) -> bool:
    """
    Intenta determinar si un PDF está compuesto por imágenes escaneadas
    mediante un umbral de cantidad mínima de caracteres extraídos.

    ❓ ¿Y si el texto es muy corto pero no escaneado? Puede haber falsos positivos.
    """
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            texto = " ".join([page.extract_text() or "" for page in pdf.pages])
            return len(texto.strip()) < THRESHOLD_MIN_CARACTERES
    except Exception:
        return True  # Si pdfplumber falla, asumimos que es complejo


def extract_with_pdfplumber(ruta_pdf: str) -> str:
    """Extrae texto desde PDF usando pdfplumber (más fiel al layout)."""
    with pdfplumber.open(ruta_pdf) as pdf:
        return "\n".join([page.extract_text() or "" for page in pdf.pages])


def extract_with_pymupdf(ruta_pdf: str) -> str:
    """Extrae texto con PyMuPDF, muy rápido pero menos preciso con columnas o fórmulas."""
    doc = fitz.open(ruta_pdf)
    return "\n".join([page.get_text("text") for page in doc])


def extract_text(ruta_pdf: str) -> str:
    """
    Ruta principal de extracción. Intenta lo más eficiente primero,
    y recurre al OCR solo si es necesario.

    🔁 Este enfoque mantiene el rendimiento sin sacrificar precisión cuando se requiere.
    """
    texto_crudo = ""

    if es_pdf_complejo(ruta_pdf):
        try:
            texto_crudo = extract_with_pdfplumber(ruta_pdf)
            if not texto_crudo.strip():
                raise ValueError("Sin texto extraído con pdfplumber")
        except Exception:
            texto_crudo = ocr_completo_inteligente(ruta_pdf)
    else:
        texto_crudo = extract_with_pymupdf(ruta_pdf)
        if not texto_crudo.strip():
            texto_crudo = ocr_completo_inteligente(ruta_pdf)

    return limpiar_texto(texto_crudo)
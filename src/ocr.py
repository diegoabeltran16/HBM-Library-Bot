# 👁️ src/ocr.py – Gen Visual OCR Inteligente

# ---
# Este módulo es responsable de transformar PDFs escaneados en texto legible
# usando Tesseract OCR. Se plantea como un gen especializado, activado solo si
# el sistema detecta que el PDF no contiene texto extraíble directamente.
#
# 💬 Reflexión: ¿Qué pasa si la calidad de imagen es mala? ¿Y si las páginas tienen rotación?
# ¿Deberíamos permitir preprocesamiento (contraste, binarización)? Eso puede ser una Vuelta 3...

from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError
from PIL import Image
import pytesseract
import os
import shutil
import fitz  # PyMuPDF como alternativa
from pathlib import Path

# ✅ Ruta local esperada donde se instaló Tesseract
TESSERACT_LOCAL_PATH = Path.home() / "AppData" / "Local" / "Programs" / "Tesseract-OCR" / "tesseract.exe"
if TESSERACT_LOCAL_PATH.exists():
    pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_LOCAL_PATH)
    print(f"✅ Tesseract detectado en: {TESSERACT_LOCAL_PATH}")
else:
    print("⚠️ No se encontró tesseract.exe en la ruta local esperada.")

# ✅ Ruta local esperada para Poppler (solo Windows)
POPPLER_LOCAL_PATH = Path.home() / "AppData" / "Local" / "Programs" / "poppler-24.08.0" / "Library" / "bin"
if not POPPLER_LOCAL_PATH.exists():
    POPPLER_LOCAL_PATH = None
    print("⚠️ No se encontró Poppler en la ruta local esperada.")
else:
    print(f"✅ Poppler detectado en: {POPPLER_LOCAL_PATH}")

# 📁 Carpeta temporal para imágenes OCR
CARPETA_TEMP = "temp_ocr"


def convertir_pdf_a_imagenes(pdf_path: str, poppler_path=POPPLER_LOCAL_PATH) -> list[Image.Image]:
    """
    Convierte cada página del PDF en una imagen (formato PNG), usando pdf2image.
    Si Poppler no está disponible, lanza excepción que puede ser manejada por fallback.
    """
    os.makedirs(CARPETA_TEMP, exist_ok=True)
    try:
        imagenes = convert_from_path(pdf_path, poppler_path=poppler_path)
        rutas_imagenes = []
        for i, imagen in enumerate(imagenes):
            ruta = os.path.join(CARPETA_TEMP, f"pagina_{i+1}.png")
            imagen.save(ruta, "PNG")
            rutas_imagenes.append(ruta)
        return [Image.open(ruta) for ruta in rutas_imagenes]
    except PDFInfoNotInstalledError:
        raise


def convertir_pdf_con_fitzz(pdf_path: str) -> list[Image.Image]:
    """
    Conversión alternativa: rasteriza el PDF usando PyMuPDF.
    🔬 Menor calidad que Poppler, pero útil cuando este no está disponible.
    """
    doc = fitz.open(pdf_path)
    imagenes = []
    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        imagenes.append(img)
    return imagenes


def extraer_texto_ocr(imagen: Image.Image, lang: str = 'eng') -> str:
    return pytesseract.image_to_string(imagen, lang=lang)


def borrar_temporales():
    if os.path.exists(CARPETA_TEMP):
        shutil.rmtree(CARPETA_TEMP)


def ocr_completo(pdf_path: str, lang: str = "eng") -> str:
    imagenes = convertir_pdf_a_imagenes(pdf_path)
    texto_total = []
    for idx, imagen in enumerate(imagenes):
        texto = extraer_texto_ocr(imagen, lang=lang)
        print(f"[OCR] Página {idx + 1} procesada")
        texto_total.append(texto)
    borrar_temporales()
    return "\n".join(texto_total)


def ocr_completo_inteligente(pdf_path: str, lang: str = "eng") -> str:
    """
    Versión tolerante del OCR: usa Poppler si está disponible, y fallback con PyMuPDF si no.

    📚 Ideal para facilitar pruebas locales, sin obligar a instalar binarios externos.
    """
    try:
        return ocr_completo(pdf_path, lang=lang)
    except PDFInfoNotInstalledError:
        print("⚠️ Poppler no disponible. Usando modo OCR Lite (calidad reducida).")
        imagenes = convertir_pdf_con_fitzz(pdf_path)
        texto_total = []
        for idx, imagen in enumerate(imagenes):
            texto = extraer_texto_ocr(imagen, lang=lang)
            print(f"[OCR Lite] Página {idx + 1} procesada")
            texto_total.append(texto)
        return "\n".join(texto_total)

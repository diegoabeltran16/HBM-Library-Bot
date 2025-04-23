import sys
from pathlib import Path

# 🔁 Para que se pueda importar src/
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.ocr import ocr_completo_inteligente


def test_ocr_pdf_con_imagen():
    texto = ocr_completo_inteligente("tests/fixtures/ocr_simple.pdf")
    assert isinstance(texto, str)
    assert len(texto.strip()) > 10
    assert "Multidimensional Change of Variable" in texto


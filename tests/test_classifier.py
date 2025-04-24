# tests/test_classifier.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.classifier import clasificar_tematica, extraer_titulo, extraer_autor, clasificar_documento



def test_clasificacion_tematica_naturales():
    texto = "Esta investigación explora conceptos clave de la biología y física cuántica."
    categoria, codigo = clasificar_tematica(texto)
    assert categoria == "Natural Sciences and Mathematics"
    assert codigo == "500"

def test_extraer_titulo_simple():
    texto = """Aprendizaje profundo y representación del conocimiento
Autor: Diego Beltrán
Resumen: Este estudio explora técnicas de representación..."""
    titulo = extraer_titulo(texto)
    assert titulo.startswith("Aprendizaje profundo")

def test_extraer_autor_formato_es():
    texto = "Autor: María José Ramírez"
    autor = extraer_autor(texto)
    assert autor == "María José Ramírez"

def test_extraer_autor_formato_en():
    texto = "Written by Alexander Hamilton"
    autor = extraer_autor(texto)
    assert autor == "Alexander Hamilton"

def test_clasificacion_completa():
    texto = """Machine learning techniques in medicine
By Ana Gómez
This paper discusses supervised learning and applications in diagnostics."""
    resultado = clasificar_documento(texto)

    assert resultado["categoria"] == "Technology"
    assert resultado["dewey"] == "600"
    assert resultado["titulo"].startswith("Machine learning")
    assert resultado["autor"] == "Ana Gómez"

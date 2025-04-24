# tests/test_cleaner.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))  # ✅ Esto primero

from src.cleaner import (  # ✅ Ahora Python sabe dónde está 'src'
    limpiar_texto,
    normalizar_unicode,
    eliminar_lineas_ruido,
    limpiar_texto_completo,
)


# 🔧 Asegura que src/ sea visible desde cualquier entorno
sys.path.append(str(Path(__file__).resolve().parents[1]))

# 🔹 Test 1: Limpieza básica de saltos y espacios
def test_limpieza_espacios_y_saltos():
    texto = "Este es un texto   con  espacios  \n y saltos \n\n\n innecesarios."
    resultado = limpiar_texto(texto)
    assert "\n\n" in resultado
    assert "  " not in resultado
    assert resultado.startswith("Este es un texto")

# 🔹 Test 2: Normalización Unicode de caracteres acentuados
def test_normalizacion_unicode():
    texto = "Cafe\u0301"  # "Café" descompuesto (C + acento)
    resultado = normalizar_unicode(texto)
    assert resultado == "Café"

# 🔹 Test 3: Eliminación de líneas de símbolos decorativos
def test_elimina_lineas_de_ruido():
    texto = "Resumen\n****\nEste es el contenido\n...\n"
    resultado = eliminar_lineas_ruido(texto)
    assert "****" not in resultado
    assert "..." not in resultado
    assert "Resumen" in resultado
    assert "contenido" in resultado

# 🔹 Test 4: Encabezados convertidos a Markdown si modo_md=True
def test_limpieza_completa_con_markdown():
    texto = "1. Introducción\n\nEste trabajo estudia...\n\nConclusión"
    resultado = limpiar_texto_completo(texto, modo_md=True)
    assert "## 1. Introducción" in resultado
    assert "## Conclusión" in resultado
    assert "estudia" in resultado

# 🔹 Test 5: Texto técnico simulado con fórmula y encabezado
def test_texto_tecnico_simulado_formula():
    texto = """
    B. 519.2 Probability and Statistics, the Science of Uncertainty
    =====================
    Let X ~ N(0, 1) be a standard normal random variable.

    Then: E[X] = 0   and    Var(X) = 1

    ***
    """

    resultado = limpiar_texto_completo(texto, modo_md=True)
    assert "519.2 Probability" in resultado
    assert "Let X ~ N(0, 1)" in resultado
    assert "E[X] = 0" in resultado
    assert "***" not in resultado
    assert "=====" not in resultado

"""
📘 enhancer_utils.py – Funciones auxiliares para el gen enhancer

🧠 Propósito del módulo:
Este archivo actúa como un gen auxiliar especializado para `enhancer.py`, y contiene funciones de soporte
ligadas a:
- Acumulación de estadísticas de reparación
- Aplicación de diccionarios OCR personalizados
- Futuras reglas heurísticas o nlp ligeras

Esta separación refuerza el principio de modularidad semántica y trazabilidad helicoidal.
"""

from typing import Dict, Tuple
import re

# → Esta función permite combinar los resultados de varias reparaciones
# sin sobreescribir las claves, acumulando los valores numéricos.
def acumular_stats(global_stats: Dict[str, float], nuevos_stats: Dict[str, float]) -> Dict[str, float]:
    """
    🔢 Acumulador de estadísticas numéricas de funciones correctoras.

    Ideal para contar cuántas correcciones se han hecho en total al texto.
    No modifica valores no numéricos.
    """
    for clave, valor in nuevos_stats.items():
        if isinstance(valor, (int, float)):
            global_stats[clave] = global_stats.get(clave, 0) + valor
    return global_stats

# → Esta función aplica un diccionario de reemplazos OCR comunes
# El diccionario puede ser cargado desde un JSON externo (ej: "ocr_dict.json")
def aplicar_diccionario(texto: str, diccionario: Dict[str, str]) -> Tuple[str, Dict[str, int]]:
    """
    📖 Aplica un diccionario de reemplazos sobre el texto.

    Ideal para limpiar errores de OCR conocidos como:
    - "rn" por "m"
    - "1ntroducción" por "Introducción"

    Args:
        texto: Texto a procesar
        diccionario: Diccionario con pares {"mal": "bien"}

    Returns:
        texto corregido y stats con cantidad de reemplazos
    """
    reemplazos = 0
    for clave, valor in diccionario.items():
        if clave in texto:
            ocurrencias = texto.count(clave)
            texto = texto.replace(clave, valor)
            reemplazos += ocurrencias

    return texto, {"reemplazos_dict": reemplazos}
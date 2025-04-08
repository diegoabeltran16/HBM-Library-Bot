# src/cleaner.py

"""
Función de limpieza para normalizar el texto extraído:
- Elimina saltos de línea innecesarios
- Remueve múltiples espacios
- Recorta texto
"""

import re

def limpiar_texto(texto):
    """
    Devuelve una versión limpia del texto:
    sin saltos de línea, espacios dobles o triples.
    """
    texto = texto.replace('\n', ' ')
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

# src/cleaner.py

import re
import unicodedata

# 🔧 Lista de símbolos decorativos considerados como "ruido visual"
SIMBOLOS_RUIDO = {'----', '***', '///', '...', '__', '==', '~~~', '====='}

# 🔹 1. Normaliza caracteres Unicode a forma NFC
def normalizar_unicode(texto):
    """
    Normaliza caracteres a una forma estándar para evitar errores de codificación.
    """
    return unicodedata.normalize("NFC", texto)

# 🔹 2. Elimina líneas vacías o compuestas solo por símbolos decorativos
def eliminar_lineas_ruido(texto):
    """
    Filtra líneas que son solo símbolos, guiones, etc.
    """
    lineas_limpias = []
    for linea in texto.split('\n'):
        strip = linea.strip()
        if not strip:
            continue
        if strip in SIMBOLOS_RUIDO:
            continue
        if re.match(r'^[\-\*\.\|\\_=~]{3,}$', strip):
            continue
        if len(strip) < 3 and not strip.isalpha():
            continue
        lineas_limpias.append(linea)
    return '\n'.join(lineas_limpias)

# 🔹 3. Heurística básica para detectar encabezados o títulos
def detectar_encabezado(linea):
    """
    Detecta si una línea es un encabezado usando heurísticas comunes.
    """
    if linea.isupper() and len(linea.split()) < 10:
        return True
    if re.match(r'^\d+(\.\d+)*\s+', linea):
        return True
    if re.search(r'\b(Resumen|Introducción|Conclusión|Referencias)\b', linea, re.IGNORECASE):
        return True
    return False

# 🔹 4. Marca líneas detectadas como encabezados con sintaxis Markdown (##)
def agregar_markdown_headers(texto):
    """
    Convierte encabezados detectados en encabezados Markdown (nivel 2).
    """
    lineas = texto.split('\n')
    nuevas = []
    for linea in lineas:
        if detectar_encabezado(linea):
            nuevas.append(f"## {linea.strip()}")
        else:
            nuevas.append(linea)
    return '\n'.join(nuevas)

# 🔹 5. Limpieza general: saltos, espacios y saltos semánticos entre párrafos
def limpiar_texto(texto):
    """
    Elimina saltos de línea innecesarios, normaliza espacios y mejora legibilidad.
    """
    texto = texto.replace('\r\n', '\n')
    texto = re.sub(r'(?<=[a-z0-9\.\)])\n(?=[A-Z])', '\n\n', texto)  # salto entre frases conectadas
    texto = re.sub(r'\n{3,}', '\n\n', texto)  # máximo 2 saltos seguidos
    texto = re.sub(r'[ \t]+', ' ', texto)
    texto = re.sub(r' *\n *', '\n', texto)
    return texto.strip()

# 🔹 6. Pipeline principal de limpieza, configurable por flags
def limpiar_texto_completo(texto, modo_md=False, filtrar_ruido=True):
    """
    Ejecuta la limpieza completa con opciones para markdown y filtrado de ruido.

    Args:
        texto (str): El texto a limpiar.
        modo_md (bool): Si True, convierte encabezados en ## estilo Markdown.
        filtrar_ruido (bool): Si True, elimina líneas de bajo valor visual.

    Returns:
        str: El texto limpio y procesado.
    """
    texto = normalizar_unicode(texto)
    if filtrar_ruido:
        texto = eliminar_lineas_ruido(texto)
    texto = limpiar_texto(texto)
    if modo_md:
        texto = agregar_markdown_headers(texto)
    return texto

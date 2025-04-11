# src/validator.py

from typing import Tuple, Dict

def validar_texto_no_vacio(texto: str) -> Tuple[bool, str]:
    if not texto or len(texto.strip()) < 10:
        return False, "texto vacío o invisible"
    return True, ""

def validar_longitud(texto: str, umbral_palabras: int = 150) -> Tuple[bool, str]:
    palabras = texto.split()
    if len(palabras) < umbral_palabras:
        return False, f"texto muy corto ({len(palabras)} palabras)"
    return True, ""

def validar_titulo(titulo: str) -> Tuple[bool, str]:
    if not titulo or titulo.strip().lower() in ["untitled", "document", "none", ""]:
        return False, "título genérico o vacío"
    if len(titulo.strip()) < 15:
        return False, "título demasiado corto"
    return True, ""

def validar_autor(autor: str) -> Tuple[bool, str]:
    if not autor:
        return False, "autor no presente"
    blacklist = ["unknown", "anonymous", "n/a", "-", ""]
    if autor.strip().lower() in blacklist:
        return False, f"autor inválido: {autor.strip()}"
    return True, ""

def validar_documento(texto: str, titulo: str = "", autor: str = "") -> Tuple[bool, Dict]:
    """
    Evalúa criterios mínimos antes de exportar.
    Incluye validación de texto, longitud, título y autor.
    """
    errores = []

    for funcion in [validar_texto_no_vacio, validar_longitud]:
        ok, razon = funcion(texto)
        if not ok:
            errores.append(razon)

    for funcion, valor in [(validar_titulo, titulo), (validar_autor, autor)]:
        ok, razon = funcion(valor)
        if not ok:
            errores.append(f"(warning) {razon}")

    if errores:
        return False, {"razones": errores}

    return True, {}

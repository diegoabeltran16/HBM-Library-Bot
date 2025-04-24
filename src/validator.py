import re
from datetime import datetime
from src.logger import log_validacion
from src.utils import calcular_hash_md5

def validar_documento(texto: str, ruta_pdf: str) -> list:
    """
    Ejecuta validaciones sintácticas y semánticas sobre el texto extraído,
    loggea cada evento y devuelve un resumen de errores.
    """
    errores = []

    # Validaciones sintácticas mínimas
    if len(texto.strip()) < 10:
        errores.append("Texto vacío o ilegible.")

    if len(texto.split()) < 150:
        errores.append("Texto demasiado corto (menos de 150 palabras).")

    # Validaciones semánticas
    errores += validar_resumen(texto)
    errores += validar_secciones(texto)
    errores += validar_citas_referencias(texto)

    # Logging de errores con trazabilidad
    hash_doc = calcular_hash_md5(ruta_pdf)
    for error in errores:
        log_validacion(
            evento="validation_error",
            error_code=mapear_codigo(error),
            severity=clasificar_severidad(error),
            zone=detectar_zona(error),
            archivo=ruta_pdf,
            razones=[error],
            hash=hash_doc
        )

    return errores

def validar_resumen(texto):
    errores = []
    match = re.search(r'(?i)^(Resumen|Abstract):\s*(.+?)(\n\n|\n[A-Z])', texto, re.DOTALL | re.MULTILINE)
    if not match:
        errores.append("Resumen no encontrado.")
    else:
        resumen = match.group(2)
        palabras = len(resumen.split())
        if not (100 <= palabras <= 250):
            errores.append(f"Resumen fuera de rango: {palabras} palabras.")
    return errores

def validar_secciones(texto):
    esperadas = ['Introducción', 'Método', 'Resultados', 'Discusión', 'Referencias']
    encontradas = re.findall(r'^\s*(%s)' % '|'.join(esperadas), texto, re.MULTILINE | re.IGNORECASE)
    faltantes = set(esperadas) - set(map(str.capitalize, encontradas))
    return [f"Secciones faltantes: {', '.join(faltantes)}"] if faltantes else []

def validar_citas_referencias(texto):
    if not re.search(r'\[\d+\]|\([A-Z][a-z]+, \d{4}\)', texto):
        return ["No se detectaron citas ni referencias."]
    return []

def mapear_codigo(error_msg):
    if "Resumen" in error_msg:
        return "E4002"
    if "Secciones faltantes" in error_msg:
        return "E4001"
    if "citas" in error_msg:
        return "E4003"
    if "vacío" in error_msg:
        return "E4000"
    return "E4999"

def clasificar_severidad(error_msg):
    if "vacío" in error_msg:
        return "CRITICAL"
    if "Resumen" in error_msg:
        return "WARNING"
    if "Secciones" in error_msg:
        return "ERROR"
    return "INFO"

def detectar_zona(error_msg):
    if "Resumen" in error_msg:
        return "abstract"
    if "Secciones" in error_msg:
        return "body"
    if "citas" in error_msg:
        return "references"
    return "global"

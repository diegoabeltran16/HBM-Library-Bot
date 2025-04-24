import re
from datetime import datetime
from src.logger import log_validacion
from src.utils import calcular_hash_md5

def validar_documento(
    texto: str,
    ruta_pdf: str,
    hash_doc: str = None,
    tolerante: bool = False
) -> tuple[bool, dict]:
    """
    Ejecuta validaciones sintácticas y semánticas sobre el texto extraído,
    loggea cada evento pero nunca bloquea la exportación.

    Retorna:
      - True siempre (validación sólo emite warnings)
      - info: dict con la clave 'razones' listando los errores detectados
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

    # Determinar identificador de documento para logging
    if not hash_doc:
        hash_doc = calcular_hash_md5(ruta_pdf)

    # Registrar cada error como evento de validación
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

    # Nunca bloqueamos la exportación
    return True, {"razones": errores}


def validar_resumen(texto: str) -> list[str]:
    errores = []
    match = re.search(r'(?i)^(Resumen|Abstract):\s*(.+?)(\n\n|\n[A-Z])', texto, re.DOTALL | re.MULTILINE)
    if not match:
        errores.append("Resumen no encontrado.")
    else:
        resumen = match.group(2)
        palabras = len(resumen.split())
        if palabras < 100 or palabras > 250:
            errores.append(f"Resumen fuera de rango: {palabras} palabras.")
    return errores


def validar_secciones(texto: str) -> list[str]:
    esperadas = ['Introducción', 'Método', 'Resultados', 'Discusión', 'Referencias']
    encontradas = re.findall(r'^\s*(%s)' % '|'.join(esperadas), texto, re.MULTILINE | re.IGNORECASE)
    encontradas_cap = set(map(str.capitalize, encontradas))
    faltantes = [sec for sec in esperadas if sec not in encontradas_cap]
    if faltantes:
        return [f"Secciones faltantes: {', '.join(faltantes)}"]
    return []


def validar_citas_referencias(texto: str) -> list[str]:
    if not re.search(r'\[\d+\]|\([A-Z][a-z]+, \d{4}\)', texto):
        return ["No se detectaron citas ni referencias."]
    return []


def mapear_codigo(error_msg: str) -> str:
    msg = error_msg.lower()
    if "vacío" in msg or "ilegible" in msg:
        return "E4000"
    if "secciones faltantes" in error_msg:
        return "E4001"
    if "resumen" in error_msg.lower():
        return "E4002"
    if "citas" in msg:
        return "E4003"
    return "E4999"


def clasificar_severidad(error_msg: str) -> str:
    msg = error_msg.lower()
    if "vacío" in msg or "ilegible" in msg:
        return "WARNING"
    if "resumen" in msg:
        return "INFO"
    if "secciones faltantes" in error_msg:
        return "INFO"
    return "INFO"


def detectar_zona(error_msg: str) -> str:
    if "resumen" in error_msg.lower():
        return "abstract"
    if "secciones faltantes" in error_msg:
        return "body"
    if "citas" in error_msg.lower():
        return "references"
    return "global"

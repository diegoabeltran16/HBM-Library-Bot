"""
📘 enhancer.py – Reparación y mejora de texto dañado extraído de PDF

Propósito:
- Reparar patrones comunes de texto dañado por PDF parsing (ej: cid, unicode corrupto)
- Facilitar mejor clasificación, validación y lectura
- Registrar impactos vía log_evento para auditabilidad

Funciones principales:
- reparar_cid()
- normalizar_unicode()
- marcar_fragmentos_dudosos()
- enriquecer_texto() (función compuesta)
"""

import re
import unicodedata
from datetime import datetime

# 🌐 Fallback en caso de que log_evento no esté disponible (para testeo aislado)
try:
    from src.logger import log_evento
except ImportError:
    log_evento = lambda *args, **kwargs: None  # noop


def reparar_cid(texto: str) -> tuple[str, dict]:
    """Elimina patrones tipo 'cid:123' generados por PDFs mal decodificados."""
    patron = r"cid:\d+"
    encontrados = re.findall(patron, texto)
    nuevo_texto = re.sub(patron, "", texto)
    return nuevo_texto, {"cid_reparados": len(encontrados)}


def normalizar_unicode(texto: str) -> tuple[str, dict]:
    """Corrige codificaciones defectuosas como 'Ã³' → 'ó'."""
    normalizado = unicodedata.normalize("NFKC", texto)
    cambios = {"unicode_normalizado": normalizado != texto}
    return normalizado, cambios


def marcar_fragmentos_dudosos(texto: str) -> tuple[str, dict]:
    """Marca bloques sin letras como sospechosos para auditoría."""
    if not re.search(r"[a-zA-Z]", texto):
        return f"[DUDOSO] {texto}", {"marcas_insertadas": 1}
    return texto, {"marcas_insertadas": 0}


def enriquecer_texto(texto: str, archivo: str = "") -> str:
    """
    Aplica secuencialmente todas las funciones de mejora.
    Devuelve el texto enriquecido y registra el cambio si aplica.
    """
    stats_global = {}

    for funcion in [reparar_cid, normalizar_unicode, marcar_fragmentos_dudosos]:
        texto, stats = funcion(texto)
        stats_global.update(stats)

    # Log solo si hubo cambios significativos
    if any(stats_global.values()):
        log_evento("enhanced_text", archivo=archivo, **stats_global)

    return texto

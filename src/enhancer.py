"""
📘 enhancer.py – Reparación y mejora de texto dañado extraído de PDF

🎯 Propósito:
- Corregir patrones comunes de corrupción en el texto (cid:123, mojibake, palabras partidas)
- Mejorar la legibilidad antes de clasificación o exportación
- Ofrecer trazabilidad con estadísticas y modo debug opcional

🛠️ Funciones principales:
- reemplazar_cid_ascii(): (cid:243) → ó
- reparar_cid(): Elimina residuos tipo "cid:123"
- reparar_palabras_partidas(): "introduccid:123on" → "introducon"
- reparar_encoding(): "Ã³ptima" → "óptima" (usando ftfy)
- normalizar_unicode(): é → é (forma precompuesta)
- marcar_fragmentos_dudosos(): etiqueta líneas ilegibles
- enriquecer_texto(): orquesta todas las anteriores

⚙️ Extras:
- acumulación de estadísticas
- control de flujo flexible (pasos)
- debug opcional
"""

import re
import unicodedata

# Reparación de codificación tipo mojibake
try:
    from ftfy import fix_text
except ImportError:
    fix_text = lambda x: x  # fallback silencioso si no está instalado

# Logging opcional para trazabilidad
try:
    from src.logger import log_evento
except ImportError:
    log_evento = lambda *args, **kwargs: None


# ────────────────────────────────────────────────
# 🔢 Acumulador de estadísticas
# ────────────────────────────────────────────────

def acumular_stats(global_stats: dict, nuevos_stats: dict) -> dict:
    """Suma estadísticas numéricas, evita sobrescritura."""
    for clave, valor in nuevos_stats.items():
        if isinstance(valor, (int, float)):
            global_stats[clave] = global_stats.get(clave, 0) + valor
    return global_stats


# ────────────────────────────────────────────────
# 🔧 Funciones de reparación específicas
# ────────────────────────────────────────────────

def reemplazar_cid_ascii(texto: str) -> tuple[str, dict]:
    """
    Reemplaza (cid:NNN) → carácter Unicode.
    Ej: (cid:243) → ó
    """
    patron = re.compile(r"\(cid:(\d+)\)")
    ocurrencias = patron.findall(texto)
    reemplazos = 0

    def convertir(match):
        nonlocal reemplazos
        try:
            codigo = int(match.group(1))
            reemplazos += 1
            return chr(codigo)
        except ValueError:
            return match.group(0)

    texto_corregido = patron.sub(convertir, texto)
    return texto_corregido, {"cid_ascii_convertidos": reemplazos}


def reparar_cid(texto: str) -> tuple[str, dict]:
    """
    Elimina residuos de "cid:123" aún presentes.
    """
    patron = r"cid:\d+"
    encontrados = re.findall(patron, texto)
    texto_corregido = re.sub(patron, "", texto)
    return texto_corregido, {"cid_reparados": len(encontrados)}


def reparar_palabras_partidas(texto: str) -> tuple[str, dict]:
    """
    Repara palabras divididas por cid:NNN intermedio.
    Ej: "introduccid:123ion" → "introduccion"
    """
    patron = r"(\w{2,})cid:\d+(\w{2,})"
    matches = re.findall(patron, texto)
    texto_reparado = re.sub(patron, r"\1\2", texto)
    return texto_reparado, {"palabras_reparadas": len(matches)}


def reparar_encoding(texto: str, forzar: bool = False) -> tuple[str, dict]:
    """
    Repara errores de codificación con ftfy.
    Solo se activa si hay símbolos tipo "Ã" o si `forzar=True`.
    """
    if not forzar and "Ã" not in texto:
        return texto, {"encoding_reparado": 0}
    try:
        corregido = fix_text(texto)
        return corregido, {"encoding_reparado": int(corregido != texto)}
    except Exception as e:
        return texto, {"encoding_reparado": 0, "error_encoding": str(e)}


def normalizar_unicode(texto: str) -> tuple[str, dict]:
    """
    Convierte secuencias Unicode a formas precompuestas.
    Ej: "é" → "é"
    """
    normalizado = unicodedata.normalize("NFKC", texto)
    return normalizado, {"unicode_normalizado": int(normalizado != texto)}


def marcar_fragmentos_dudosos(texto: str) -> tuple[str, dict]:
    """
    Si no hay letras, marca con "[DUDOSO]".
    Ej: líneas de símbolos o fórmulas perdidas.
    """
    if not re.search(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]", texto):
        return f"[DUDOSO] {texto}", {"marcas_insertadas": 1}
    return texto, {"marcas_insertadas": 0}


# ────────────────────────────────────────────────
# 🚀 Función principal: enriquecer_texto
# ────────────────────────────────────────────────

def enriquecer_texto(
    texto: str,
    archivo: str = "",
    pasos: list = None,
    debug: bool = False
) -> str:
    """
    Aplica en cascada funciones de mejora. Loguea cambios si los hay.

    Parámetros:
    - texto: str → Texto base a corregir
    - archivo: str → Ruta opcional para trazabilidad
    - pasos: list[func] → Orden y selección de funciones a aplicar
    - debug: bool → Muestra comparación antes/después (útil para desarrollo)
    """

    if pasos is None:
        pasos = [
            reemplazar_cid_ascii,
            reparar_encoding,
            normalizar_unicode,
            reparar_palabras_partidas,
            reparar_cid,
            marcar_fragmentos_dudosos,
        ]

    original = texto
    stats_global = {}

    for funcion in pasos:
        texto, stats = funcion(texto)
        stats_global = acumular_stats(stats_global, stats)

    if any(stats_global.values()):
        log_evento("enhanced_text", archivo=archivo, **stats_global)
        if debug:
            print("🧪 Debug Enriquecimiento:")
            print("Antes:\n", original[:500])
            print("Después:\n", texto[:500])
            print("Stats:", stats_global)

    return texto

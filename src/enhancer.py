import json
import re
import unicodedata
from pathlib import Path
from typing import Callable, Tuple, Dict, List

from src.enhancer_utils import acumular_stats, aplicar_diccionario

__all__ = [
    'reemplazar_cid_ascii', 'reparar_encoding', 'normalizar_unicode',
    'reparar_palabras_partidas', 'reparar_cid', 'reparar_ocr_simbolos',
    'marcar_fragmentos_dudosos', 'pipeline_hooked_enhancer', 'enriquecer_texto', 'acumular_stats'
]

# === Funciones de reparación semántica ===

def reemplazar_cid_ascii(texto: str) -> Tuple[str, Dict[str, int]]:
    """
    Elimina etiquetas 'cid:123' y cuenta cuántas sustituciones realizó.
    """
    matches = re.findall(r'cid:\d+', texto)
    nuevo_texto = re.sub(r'cid:\d+', '', texto)
    return nuevo_texto, {'reemplazos_cid_ascii': len(matches)}


def reparar_encoding(texto: str) -> Tuple[str, Dict[str, int]]:
    """
    Corrige errores comunes de encoding (mojibake) en el texto.
    """
    mapping = {
        'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
        'Ã±': 'ñ', 'Ã‘': 'Ñ'
    }
    count = 0
    nuevo = texto
    for mal, bien in mapping.items():
        ocurrencias = nuevo.count(mal)
        if ocurrencias:
            nuevo = nuevo.replace(mal, bien)
            count += ocurrencias
    return nuevo, {'reparaciones_encoding': count}


def normalizar_unicode(texto: str) -> Tuple[str, Dict[str, int]]:
    """
    Normaliza la forma Unicode a NFC para asegurar combinación de caracteres.
    """
    return unicodedata.normalize('NFC', texto), {}


def reparar_palabras_partidas(texto: str) -> Tuple[str, Dict[str, int]]:
    """
    Une palabras partidas al final de línea: 'pro-\nducto' → 'producto'.
    """
    pattern = r'-\s*\n\s*'
    ocurrencias = len(re.findall(pattern, texto))
    nuevo = re.sub(pattern, '', texto)
    return nuevo, {'palabras_reparadas': ocurrencias}


def reparar_cid(texto: str) -> Tuple[str, Dict[str, int]]:
    """
    Elimina patrones 'cid(123)' y cuenta las sustituciones.
    """
    matches = re.findall(r'cid\(\d+\)', texto)
    nuevo = re.sub(r'cid\(\d+\)', '', texto)
    return nuevo, {'reemplazos_cid': len(matches)}


def reparar_ocr_simbolos(texto: str) -> Tuple[str, Dict[str, int]]:
    """
    Sustituye ligaduras y símbolos OCR por caracteres ASCII estándar.
    Ejemplo: 'ﬁ' → 'fi', 'ﬂ' → 'fl', 'Ɵ' → 'O'.
    """
    mapping = {'ﬁ': 'fi', 'ﬂ': 'fl', 'Ɵ': 'O'}
    count = 0
    nuevo = texto
    for mal, bien in mapping.items():
        ocurrencias = nuevo.count(mal)
        if ocurrencias:
            nuevo = nuevo.replace(mal, bien)
            count += ocurrencias
    return nuevo, {'reparados_ocr_simbolos': count}


def marcar_fragmentos_dudosos(texto: str) -> Tuple[str, Dict[str, int]]:
    """
    Marca fragmentos dudosos sin alterar el contenido,
    añadiendo etiquetas para análisis posterior.
    """
    # Implementación mínima: no-op, sin estadísticas
    return texto, {}


def pipeline_hooked_enhancer(
    texto: str,
    config: Dict[str, any]
) -> Tuple[str, Dict[str, float]]:
    """
    🧬 Enhancer adaptativo con hooks inteligentes.

    Aplica funciones de reparación semántica en orden definido y de forma adaptativa:
    - Mide el impacto de cada paso (cuántas correcciones aplicó).
    - Reintenta los que superan cierto umbral de ganancia.
    - Carga un diccionario OCR externo si está disponible.

    Args:
        texto: texto original a mejorar.
        config: diccionario con:
            pasos: lista de funciones (func) que devuelven (texto, stats).
            retry_umbral: umbral mínimo de impacto para reintentar función.
            max_intentos: máximo de repeticiones por función.
            ocr_dict_path: ruta opcional al archivo ocr_dict.json.

    Returns:
        texto corregido y estadísticas acumuladas.
    """
    pasos: List[Callable] = config.get('pasos', [])
    retry_umbral: float = config.get('retry_umbral', 5)
    max_intentos: int = config.get('max_intentos', 2)
    stats_global: Dict[str, float] = {}
    intentos: Dict[str, int] = {func.__name__: 0 for func in pasos}

    # Cargar diccionario OCR si existe
    dict_path = config.get('ocr_dict_path')
    if dict_path and Path(dict_path).exists():
        diccionario = json.loads(Path(dict_path).read_text(encoding='utf-8'))
        pasos.insert(0, lambda t: aplicar_diccionario(t, diccionario))
        intentos['<ocr_dict>'] = 0

    # Loop adaptativo
    cambios = True
    texto_actual = texto
    while cambios:
        cambios = False
        for func in pasos:
            nombre = getattr(func, '__name__', '<ocr_dict>')
            if intentos.get(nombre, 0) >= max_intentos:
                continue

            texto_nuevo, stats = func(texto_actual)
            impacto = sum(v for v in stats.values() if isinstance(v, (int, float)))
            if impacto >= retry_umbral:
                cambios = True
                intentos[nombre] += 1
                texto_actual = texto_nuevo
                stats_global = acumular_stats(stats_global, stats)

    return texto_actual, stats_global


def enriquecer_texto(
    texto: str,
    config: Dict[str, any] = None
) -> str:
    """
    Función de envoltura que expone un flujo de enriquecimiento sencillo.

    Si no se proporciona configuración, usa los pasos por defecto.
    """
    default_steps = [
        reemplazar_cid_ascii,
        reparar_encoding,
        normalizar_unicode,
        reparar_palabras_partidas,
        reparar_cid,
        reparar_ocr_simbolos,
        marcar_fragmentos_dudosos
    ]
    cfg = config or {}
    cfg.setdefault('pasos', default_steps)
    enriched, _ = pipeline_hooked_enhancer(texto, cfg)
    return enriched

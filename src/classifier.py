# src/classifier.py

from .utils import normalizar_texto
import re

# ===============================
# Diccionario de categorías Dewey
# ===============================
CATEGORIAS_DEWEY = {
    "General Works": (["encyclopedia", "news", "summary"], "000"),
    "Philosophy and Psychology": (["ethics", "logic", "psychology", "epistemology"], "100"),
    "Religion": (["bible", "god", "theology", "religion"], "200"),
    "Social Sciences": (["economy", "education", "law", "government", "sociology"], "300"),
    "Language": (["grammar", "linguistics", "translation", "language"], "400"),
    "Natural Sciences and Mathematics": (["mathematics", "physics", "biology", "chemistry", "science","física", "biología", "química", "ciencia","mathematics", "physics", "biology", "chemistry", "science",
        "fisica", "biologia", "quimica", "ciencia", "cuantica"], "500"),
    "Technology": (["engineering", "medicine", "software", "ai", "agriculture"], "600"),
    "The Arts": (["music", "drawing", "photography", "design", "sports"], "700"),
    "Literature": (["poetry", "novel", "fiction", "essay", "drama"], "800"),
    "History and Geography": (["history", "war", "civilizations", "travel", "biography"], "900")
}


def clasificar_documento(texto: str) -> dict:
    """
    Clasifica un texto según la clasificación Dewey,
    y extrae metadatos básicos (título, autor).
    """
    categoria, dewey = clasificar_tematica(texto)
    titulo = extraer_titulo(texto)
    autor = extraer_autor(texto)

    return {
        "categoria": categoria,
        "dewey": dewey,
        "titulo": titulo,
        "autor": autor
    }


def clasificar_tematica(texto: str) -> tuple:
    texto = normalizar_texto(texto)

    for categoria, (palabras, codigo) in CATEGORIAS_DEWEY.items():
        for palabra in palabras:
            if re.search(rf"\b{palabra}\b", texto):
                return categoria, codigo

    return "General Works", "000"



def extraer_titulo(texto: str) -> str:
    """
    Retorna la primera línea que parece título (no autor).
    """
    for linea in texto.splitlines()[:10]:
        if len(linea.strip()) > 10 and not re.search(r"\b(by|autor:|escrito por)\b", linea, re.IGNORECASE):
            return linea.strip()
    return "Sin título"


def extraer_autor(texto: str) -> str:
    """
    Busca patrones comunes de autoría.
    """
    patrones = [
        r"by ([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)",
        r"autor: ([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)",
        r"escrito por:? ([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)"
    ]

    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return match.group(1)

    return "Autor desconocido"

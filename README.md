# 📘 Dewey Pipeline – Procesamiento Inteligente de PDFs en forma de biblioteca publica :D

![](https://github.com/diegoabeltran16/dewey-pipeline/actions/workflows/test.yml/badge.svg)

---

## 🎯 Objetivo General

Facilitar el análisis y organización de literatura científica con una herramienta local, ética y extensible.

---

## 🔧 ¿Qué hace el pipeline?

- 📄 Extrae texto de PDFs técnicos o académicos usando [`PyMuPDF`](https://pymupdf.readthedocs.io/en/latest/) o [`pdfplumber`](https://github.com/jsvine/pdfplumber)

- 🧹 Limpia el texto para que sea legible y apto para NLP
- 📚 Clasifica el contenido según la clasificación Dewey (ej. 500 – Ciencias Naturales)
- ✍️ Extrae título y autor automáticamente
- 💾 Exporta tres formatos listos para IA:
    - `.txt`: texto plano
    - `.md`: formato Markdown con metadatos
    - `.jsonl`: párrafos individuales para NLP / embeddings

---
## Melvil Dewey y el Acceso Abierto al Conocimiento

> ✨ *"Mi trabajo de vida es hacer más fácil el camino hacia el conocimiento."*  
> — **Melvil Dewey** *
> 

El nombre y propósito de este proyecto están profundamente ligados al trabajo de **Melvil Louis Kossuth Dewey** (1851–1931), bibliotecólogo, reformador educativo y visionario de la organización del conocimiento.

### 🧠 ¿Qué hizo Dewey?

- 🌐 **Creador del Dewey Decimal Classification (DDC)**: un sistema lógico y modular para clasificar todo el conocimiento humano, aún vigente en miles de bibliotecas del mundo.
- 📦 **Inspirado en Francis Bacon**: estructuró el saber en ramas que pudieran ser ordenadas, consultadas y ampliadas.
- 📚 **Fundador de la American Library Association (ALA)** y la primera escuela de bibliotecología.
- 🚐 **Promotor de las bibliotecas viajeras**: acercó los libros a comunidades rurales, entendiendo la información como bien público.

### 🌱 ¿Qué hereda este proyecto?

- **Organización estructurada del conocimiento científico** (vía clasificación Dewey y output estandarizado).
- **Simplicidad de acceso**, desde la terminal y sin servicios externos.
- **Compromiso ético con la educación libre**, la modularidad del software y la soberanía de los datos personales.
- **Portabilidad y autonomía**, como las bibliotecas viajeras... pero ahora en `.jsonl` 😉

**Dewey Pipeline** es una herramienta educativa y modular que automatiza el procesamiento de documentos en formato PDF.

Extrae texto, lo limpia, lo clasifica según la *Clasificación Decimal Dewey*, y genera salidas listas para sistemas de IA o uso humano.

> 🧠 Ideal para estudiantes, investigadores, autodidactas, y desarrolladores apasionados por el conocimiento abierto.
> 


## ▶️ ¿Cómo usarlo?


# 1. Clonar el repositorio
```bash
git clone https://github.com/diegoabeltran16/dewey-pipeline
cd dewey-pipeline
```

# 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
```

# 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

# 4. Colocar PDFs dentro de /input/ (pueden estar en subcarpetas)
```bash
mkdir input/Book
mv tu_archivo.pdf input/Book/
```

# 5. Ejecutar el pipeline
```bash
python main.py
```

---

## 💡 Ejemplo de salida

Archivo procesado como:

```
📁 output/
├── essay_100_philosophy_and_psychology_aprendizaje_automatico_diego_beltran.txt
├── essay_100_philosophy_and_psychology_aprendizaje_automatico_diego_beltran.md
├── essay_100_philosophy_and_psychology_aprendizaje_automatico_diego_beltran.jsonl

```

---

## 🔍 Fase actual: MVP Offline

| Módulo | Estado |
| --- | --- |
| Extracción | ✅ PyMuPDF + heurística de layout |
| Limpieza | ✅ Markdown-ready, preservación de semántica |
| Clasificación | ✅ Heurística Dewey + título/autor |
| Exportación | ✅ Organizado y AI-friendly |
| Logger | ✅ Multilenguaje (es/en) |
| Testing | ✅ Pytest + GitHub Actions CI |


---

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la **Apache License 2.0**.

Podés usar, modificar y distribuir este código libremente, siempre que incluyas la atribución correspondiente.

© 2024 – *diegoabeltran_16*

---

## ✨ Contribuciones

Si compartes esta visión de acceso libre al conocimiento y te interesa empezar a contruir portafolio:

- 💬 Abre issues o mejoras
- 🧪 Añade tests
- 🤝 Usá este proyecto como base para tu propia herramienta

> "El pipeline es tuyo también. Mejorémoslo juntos." LINK de como contribuir
>

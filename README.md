# 📘 OpenPages-pipeline – Procesamiento Inteligente de PDFs como Biblioteca Abierta 🤖📚

![](https://github.com/diegoabeltran16/OpenPages-pipeline/actions/workflows/test.yml/badge.svg)

---

## 🎯 Objetivo General

Facilitar el análisis y organización de literatura científica con una herramienta local, ética y extensible — lista para IA, pero pensada para humanos.

---

## 🔧 ¿Qué hace el pipeline?

- 📄 Extrae texto de PDFs técnicos o académicos usando [`PyMuPDF`](https://pymupdf.readthedocs.io/en/latest/) o [`pdfplumber`](https://github.com/jsvine/pdfplumber)
- 🧹 Limpia el texto para que sea legible y apto para NLP
- 🧠 Clasifica el contenido según taxonomías configurables (por defecto: **Clasificación Dewey**)
- ✍️ Extrae título y autor automáticamente
- 💾 Exporta tres formatos listos para IA:
  - `.txt`: texto plano
  - `.md`: formato Markdown con metadatos
  - `.jsonl`: párrafos individuales para NLP / embeddings

---

## 📚 Melvil Dewey y el Acceso Abierto al Conocimiento

> ✨ *"Mi trabajo de vida es hacer más fácil el camino hacia el conocimiento."*  
> — **Melvil Dewey** *

Este proyecto se inspiró inicialmente en el sistema decimal creado por **Melvil Louis Kossuth Dewey** (1851–1931), pionero en la organización del conocimiento. Sin embargo, también reconocemos que:

- Fue una figura controvertida por su exclusión de voces no occidentales y su conducta discriminatoria.
- Su sistema, aunque útil, no representa todas las formas de saber ni todas las culturas.

🔄 **OpenPages-pipeline** toma lo útil de esa estructura, pero abre la puerta a múltiples formas de clasificar y explorar el conocimiento.

---

## 🌱 ¿Qué hereda este proyecto?

- **Organización estructurada**, comenzando por Dewey, pero con apertura a otros enfoques (UNESCO, folksonomías).
- **Acceso simple**, desde terminal y sin conexión a internet.
- **Ética educativa**: sin trackers, sin nube, sin barreras.
- **Portabilidad libre**, como las bibliotecas viajeras... pero en `.jsonl` 😉

> 🧠 Ideal para estudiantes, investigadores, docentes, autodidactas, y desarrolladores comprometidos con el conocimiento abierto.

---

## ▶️ ¿Cómo usarlo?

### 1. Clonar el repositorio

```bash
git clone https://github.com/diegoabeltran16/OpenPages-pipeline
cd OpenPages-pipeline
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
.venv\Scripts\activate  # en Windows
# o en Linux/macOS:
# source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Colocar PDFs dentro de /input/ (pueden estar en subcarpetas)

```bash
mkdir input/Book
mv tu_archivo.pdf input/Book/
```

### 5. Ejecutar el pipeline

```bash
python main.py
```

---

## 💡 Ejemplo de salida

```plaintext
📁 output/
├── ensayo_100_filosofia_aprendizaje_automatico_diego_beltran.txt
├── ensayo_100_filosofia_aprendizaje_automatico_diego_beltran.md
├── ensayo_100_filosofia_aprendizaje_automatico_diego_beltran.jsonl
```

---

## 🔍 Fase actual: MVP Offline

| Módulo | Estado |
| --- | --- |
| Extracción | ✅ PyMuPDF + heurística de layout |
| Limpieza | ✅ Markdown-ready, preservación semántica |
| Clasificación | ✅ Dewey heurístico + título/autor |
| Exportación | ✅ AI-ready multiformato |
| Logger | ✅ Multilenguaje (es/en) |
| Testing | ✅ Pytest + GitHub Actions CI |

---

## 📄 Licencia

Este proyecto está licenciado bajo **Apache License 2.0**.  
Podés usar, modificar y distribuir libremente, siempre que incluyas la atribución correspondiente.

© 2024–2025 – *diegoabeltran_16*

---

## ✨ Contribuciones

Si compartís esta visión de acceso libre al conocimiento, podés:

- 💬 Abrir issues o sugerencias
- 🧪 Agregar tests o módulos nuevos
- 📚 Mejorar documentación o UX

> Este pipeline también es tuyo. Hagámoslo crecer juntos.  
> ✨ `openpages-pipeline` — para leer, pensar y compartir mejor.
# 📘 PDF Knowledge Pipeline

[![Run Parser Tests](https://github.com/diegoabeltran16/dewey-pipeline/actions/workflows/test.yml/badge.svg)](https://github.com/diegoabeltran16/dewey-pipeline/actions/workflows/test.yml)


Este es un proyecto personal y educativo que automatiza el procesamiento de archivos PDF con contenido científico o técnico. Está diseñado para ser simple, modular y totalmente offline. El sistema extrae texto de los documentos, sugiere una categoría temática (por ejemplo, Inteligencia Artificial o Física Cuántica) basada en palabras clave, y genera salidas listas para futuras aplicaciones en IA como embeddings o fine-tuning.

## 🎯 Objetivo
Crear una herramienta que facilite la organización y el análisis de textos académicos, priorizando el acceso libre y el respeto por los derechos de autor. Ideal para estudiantes, investigadores, autodidactas y desarrolladores interesados en ciencia, IA y computación.

## 🔧 ¿Qué hace este proyecto?
- Extrae texto desde archivos PDF colocados en la carpeta `/input`
- Sugiere una categoría temática y número Dewey Decimal aproximado
- Genera archivos en la carpeta `/output`:
  - `.txt`: texto plano completo
  - `.md`: versión en Markdown con encabezado
  - `.jsonl`: archivo por párrafos, ideal para IA (embeddings, NLP, etc.)

## 📁 Estructura del proyecto
```
pdf-intel/
├── input/             # PDFs originales a procesar
├── output/            # Archivos procesados
├── main.py            # Script principal que orquesta todo
├── parser.py          # Función de extracción de texto con PyMuPDF
├── classifier.py      # Lógica para asignar categoría y Dewey
├── exporter.py        # Guarda los archivos .txt, .md, .jsonl
├── README.md          # Este documento
```

## ▶️ ¿Cómo usarlo?
1. Asegurate de tener Python 3.8+ instalado
2. Instalá PyMuPDF:
```bash
pip install pymupdf
```
3. Copiá tus archivos PDF en la carpeta `input/`
4. Ejecutá el script:
```bash
python main.py
```
5. Revisa los archivos generados en `output/`

## 🚧 Notas técnicas
- El sistema actual usa reglas simples de palabras clave para clasificar el texto
- Las salidas están listas para ser usadas en tareas de IA (embeddings, clasificación, RAG)
- Todo el procesamiento se realiza localmente (no requiere conexión ni servicios externos)

## 🧠 Proyección futura
- Mejora del clasificador con NLP y embeddings
- Clasificación automática más precisa según contexto
- Interfaz web o CLI interactiva
- Publicación open source completa (GitHub + ENS domain)

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la Apache License 2.0.  
Podés usar, modificar y distribuir este código libremente, siempre que incluyas la atribución correspondiente.

© diegoabeltran_16 2024


## ✨ Contribuciones
Este proyecto es un paso hacia la construcción de herramientas de acceso libre al conocimiento. Si compartís esta visión, ¡contribuí, comentá o usalo como inspiración!


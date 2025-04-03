### 📌 Plan de Desarrollo del Proyecto OpenPages AI (Dewey-Pipeline)

El proyecto OpenPages AI se desarrollará en fases modulares y progresivas para garantizar un crecimiento funcional, seguro y sostenible. Cada etapa está diseñada para ser completada, validada y documentada antes de pasar a la siguiente, alineando la evolución del sistema con buenas prácticas de software, AI y ética del conocimiento.

---

## 🔹 Fase 1: MVP Offline de Procesamiento de PDF

📍 **Objetivo:** Procesar documentos PDF localmente y generar `.txt`, `.md`, `.jsonl` con clasificación Dewey y nombres estructurados.

**Incluye:**
- Script principal (`main.py`) con flujo modular
- Extracción de texto usando PyMuPDF
- Clasificador por palabras clave (categoría + Dewey)
- Generador de archivos en `/output/`
- Mensajes bilingües (ES/EN) en terminal

**Estructura de Archivos:**
```
openpages-ai/
├── input/         # PDFs a procesar
├── output/        # Archivos procesados
├── src/
│   ├── parser.py
│   ├── classifier.py
│   ├── exporter.py
│   ├── logger.py
│   └── utils.py
├── main.py
├── requirements.txt
├── README.md
```

---

## 🔹 Fase 2: CLI Extendida con Reportes y Export

📍 **Objetivo:** Permitir comandos personalizados desde terminal con flags como `--summary`, `--export`, `--language`.

**Incluye:**
- Handler CLI con `argparse`
- Módulo de resumen por categoría
- Exportador a CSV/JSON
- Manejo de configuraciones con `.env`

**Comandos Ejemplo:**
```bash
python main.py --summary
python main.py --export --format=csv
```

---

## 🔹 Fase 3: Validación, Logging y Seguridad

📍 **Objetivo:** Fortalecer la calidad del sistema mediante validación de datos, logs y controles de seguridad.

**Incluye:**
- Validación de tipo de archivo (solo PDF)
- Manejo de errores con mensajes claros
- Logging estructurado (errores, procesados)
- Sanitización de nombres de archivos y paths
- `.env.example` para manejo de credenciales y configuración

---

## 🔹 Fase 4: Internacionalización + Preferencias de Usuario

📍 **Objetivo:** Personalizar la experiencia según idioma y estilo de salida.

**Incluye:**
- Módulo de preferencias de usuario (`config/user_prefs.json`)
- Soporte completo para ES/EN
- Opciones de tono (formal, casual)
- Preparación para futura interfaz (modo web/UI)

---

## 🔹 Fase 5: Testing Automatizado + CI/CD

📍 **Objetivo:** Asegurar la calidad continua mediante pruebas y automatización.

**Incluye:**
- Suite de pruebas con `pytest`
- Pruebas para parser, clasificador, exportador y CLI
- Configuración de GitHub Actions para CI
- Cobertura de pruebas y badge en el README

---

## 🔹 Fase 6: Embeddings y Almacenamiento Vectorial *(Opcional)*

📍 **Objetivo:** Preparar los `.jsonl` para embedding y búsqueda semántica

**Incluye:**
- Módulo para generar embeddings (OpenAI/HuggingFace)
- Almacenamiento en FAISS, Weaviate o SQLite con `pgvector`
- Búsqueda por texto natural en CLI

---

## 🔹 Fase 7: Interfaz Web Minimal (FastAPI/Flask)

📍 **Objetivo:** Permitir carga de archivos PDF desde interfaz básica con respuestas visibles

**Incluye:**
- Drag-and-drop en navegador
- Mensajes de salida categorizados
- Selector de idioma
- Previsualización de resumen/export JSONL

---

## 🔹 Fase 8: Despliegue, Documentación y Dominio ENS

📍 **Objetivo:** Publicar el proyecto como herramienta ética, libre y educativa

**Incluye:**
- Repositorio GitHub bien documentado
- Licencia Apache 2.0 y Código de Conducta
- Dominio `.eth` o `.org` apuntando a la versión estática (si aplica)
- Blog/documentación estilo Wiki con ejemplos y capturas

---

## 🔹 Beneficios de este Enfoque

- **Modularidad Total:** Cada componente puede ser probado, escalado o mejorado por separado.
- **IA-Ready:** Los `.jsonl` sirven para embeddings, fine-tuning o búsquedas semánticas.
- **Multilingüe:** Desde el inicio, se contempla la diversidad lingüística.
- **Seguridad de Base:** Pensado como herramienta offline, ética y abierta.
- **Escalable:** Listo para convertir en API, app web o motor de conocimiento.

---

✨ *Este roadmap puede escalar según necesidades, manteniendo siempre la prioridad en el acceso abierto, la transparencia y la soberanía sobre los datos procesados.*


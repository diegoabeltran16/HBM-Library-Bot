# 📘 Logger – OpenPages-pipeline

Este módulo permite registrar todos los eventos clave del procesamiento de PDFs de forma visual (emoji en consola) y persistente (archivos `.log` y `.jsonl`), con soporte multilenguaje y trazabilidad por ejecución.

---

## 🎯 Objetivo

- Proveer retroalimentación amigable en tiempo real
- Generar trazas auditables por ejecución
- Facilitar debugging, revisión, métricas y transparencia

---

## 📁 Archivos generados

Todos los archivos se guardan automáticamente en la carpeta:

```
output/logs/
```

| Archivo | Descripción |
| --- | --- |
| `run_YYYY-MM-DD_HH-MM-SS.log` | Log plano legible para humanos |
| `run_YYYY-MM-DD_HH-MM-SS.jsonl` | Log estructurado en formato JSONL (1 línea = 1 evento) |
| `<nombre_archivo>.log` | Log individual por cada PDF procesado |

---

## 🔁 Formato JSONL estructurado

Cada línea representa un evento del pipeline:

```json
{
  "timestamp": "2025-04-10T15:42:21.543Z",
  "ejecucion": "c78fbccbeed045b5919e8a7e79dd4d73",
  "evento": "clasificado",
  "archivo": "input/Libro.pdf",
  "categoria": "Tecnología",
  "dewey": "600",
  "nivel": "INFO"
}
```

---

## 📦 Campos incluidos

| Campo | Significado |
| --- | --- |
| `timestamp` | Fecha y hora del evento |
| `ejecucion` | ID único para toda la ejecución del pipeline |
| `evento` | Nombre del evento registrado |
| `archivo` | Ruta del archivo procesado |
| `categoria` | Categoría asignada (si aplica) |
| `dewey` | Código Dewey (si aplica) |
| `nivel` | Nivel del log (`INFO`, `WARNING`, `ERROR`) |

---

## 🧠 Eventos disponibles

| Evento | Emoji | Nivel sugerido | Contexto |
| --- | --- | --- | --- |
| `procesar` | 📘  | INFO | Inicio del procesamiento de un PDF |
| `clasificado` | 📖  | INFO | Clasificación exitosa del documento |
| `export_ok` | ✔️  | INFO | Exportación finalizada correctamente |
| `warning_meta` | ⚠️  | WARNING | Metadatos faltantes o inválidos |
| `warning_texto_corto` | ⚠️  | WARNING | El texto extraído es muy breve |
| `error_parse` | ❌   | ERROR | Fallo al procesar o extraer texto |
| `archivo_inaccesible` | ❌   | ERROR | No se puede abrir el archivo |

---

## ⚙️ Personalización vía variables de entorno

| Variable | Descripción | Valor por defecto |
| --- | --- | --- |
| `LANG` | Idioma de mensajes (`es`, `en`) | `es` |
| `LOG_LEVEL` | Nivel mínimo a registrar | `INFO` |
| `EXECUTION_ID` | ID manual para auditoría externa | `auto-generado` |

---

## 📌 Recomendaciones

- Revisar `run_*.jsonl` para análisis estructurado (Python, jq, dashboards)
- Usar los `.log` individuales para depurar errores aislados
- Integrar los logs en herramientas externas si se requiere trazabilidad continua

---

## 🧪 Pruebas

El archivo `test_logger.py` incluye pruebas para:

- Mensajes visuales esperados
- Verificación de archivos `.jsonl`
- Logs individuales por PDF

---

> `logger.py` es el narrador silencioso del pipeline. Te dice qué pasó, cuándo y cómo — sin ruido, con trazabilidad y respeto.
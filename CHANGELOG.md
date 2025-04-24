# 📜 CHANGELOG – OpenPages Pipeline
> Registro evolutivo helicoidal del sistema, agrupado por vueltas (Vx) y genes funcionales.

---

## 📝 Changelog V3.R2.C1

### ✨ Nuevas funciones:

- `validar_documento()`: Coordinador tolerante con logging estructurado
  
- `validar_resumen()`, `validar_secciones()`, `validar_citas_referencias()`: Heurísticas semánticas
  
- `mapear_codigo()`, `clasificar_severidad()`, `detectar_zona()`: Trazabilidad ética
  

### 🧬 Nuevos archivos/tipos de exportación:

- `.jsonl` de errores semánticos por hash, con `zone`, `error_code`, `severity`, `razones`

### 🧪 Cobertura de tests:

- ✅ 100% cobertura funcional para cada subvalidador y flujo integrador

### 🔄 Mutaciones en módulos relacionados:

- `logger.py`: Agrega `log_validacion()` para eventos estructurados
  
- `utils.py`: Añade `calcular_hash_md5()` para trazabilidad por documento

---

## 📝 Changelog V3.R2.C2

### ✨ Nuevas funciones:

🧠 Gen `validator.py`

- `validar_documento()`: Coordinador tolerante con logging estructurado
  
- `validar_resumen()`, `validar_secciones()`, `validar_citas_referencias()`: Heurísticas semánticas
  
- `mapear_codigo()`, `clasificar_severidad()`, `detectar_zona()`: Trazabilidad ética
  

🧬 Gen `enhancer.py`

- `reparar_encoding()`, `reparar_cid()`, `reparar_ocr_simbolos()`, `normalizar_unicode()`
  
- `pipeline_hooked_enhancer()`: Reparador adaptativo por impacto
  
- `enriquecer_texto()`: Interfaz sencilla para limpieza semántica
  

🧩 Gen `enhancer_utils.py`

- `acumular_stats()`: Acumulación de métricas por función
  
- `aplicar_diccionario()`: Diccionario externo para OCR (`ocr_dict.json`)
  
### 🧬 Nuevos archivos/tipos de exportación:

- `.jsonl` de errores semánticos por hash, con `zone`, `error_code`, `severity`, `razones`
  
- `.md` enriquecido con encabezados YAML (`exporter.py`)
  
- `.jsonl` por párrafos listos para AI (`exportar_archivos()`)
  

### 🧪 Cobertura de tests:

- ✅ 100% cobertura funcional en `test_validator.py`, `test_enhancer.py`
  
- ✅ Validaciones de `hash`, encabezados, resumen y citas
  
- ✅ Test de impacto adaptativo (cuenta cuántas correcciones por paso)
  

### 🔄 Mutaciones en módulos relacionados:

- `logger.py`: Agrega `log_validacion()` para eventos estructurados
  
- `utils.py`: Añade `calcular_hash_md5()` para trazabilidad por documento
  
- `exporter.py`: Limpieza de exportación con `slugify()`, integración de hash + título
  

### 📈 Derivadas observadas

- **∆r = +6.0** → Nuevas funciones en tres genes (`validator`, `enhancer`, `utils`)
  
- **∆c = +8.0** → Trazabilidad total, fallback tolerante, interfaz modular y testable

---

## 📝 Changelog V3.R2.C3

### ✨ Nuevas funciones:

📦 Gen `exporter.py`

- `exportar_archivos()`: Exporta `.txt`, `.md`, `.jsonl` en rutas trazables y AI-ready
  
- `_guardar_txt()`, `_guardar_md()`, `_guardar_jsonl()`: Helpers limpios por tipo
  
- `slugify()`: Estandariza nombres de carpetas/archivos
  

🧠 Gen `logger.py`

- Mensaje visual y estructurado de exportación por documento

### 🧪 Cobertura de tests:

- ✅ Exportación verificada para cada tipo de archivo (`.txt`, `.md`, `.jsonl`)
  
- ✅ Testea que el contenido no esté vacío y que la estructura sea correcta
  
- ✅ Limpieza de directorios tras exportación para entornos CI
  
### 📈 Derivadas observadas

- **∆r = +3.0** → Nuevas funciones activadas por exportación estructurada
  
- **∆c = +3.0** → Modularidad, trazabilidad, test unitario por tipo de salida

---

## 📝 Changelog V3.R2.C4

### ✨ Nuevas funciones:

🧩 Gen `enhancer_utils.py`

- `acumular_stats()`: Fusiona métricas por tipo de corrección sin perder trazabilidad
  
- `aplicar_diccionario()`: Aplica diccionario OCR externo (`ocr_dict.json`) para correcciones ligadas al dominio visual
  

🧪 Gen `test_utils.py`

- `test_aplicar_diccionario()`: Valida reemplazo correcto a partir de un dict OCR
  
- `test_acumular_stats()`: Asegura combinación robusta de contadores en pipeline adaptativo
  

### 🧬 Nuevos usos/estructuras:

- Uso dinámico de `ocr_dict.json` en `pipeline_hooked_enhancer()` con fallback seguro
  
- Estadísticas detalladas por tipo de mutación textual registradas en `stats_global`
  

### 🧪 Cobertura de tests:

- ✅ Tests directos para ambos helpers en `test_utils.py`
  
- ✅ Integración comprobada dentro de `test_enhancer.py` vía stats acumuladas
  

### 🔄 Mutaciones en módulos relacionados:

- `enhancer.py`: Delegación de limpieza OCR y acumulación de impacto a `enhancer_utils`
  
- `main.py`: No requiere cambios – integración transparente
  

### 📈 Derivadas observadas:

- **∆r = +2.0** → Se introducen dos helpers clave para mejora semántica
  
- **∆c = +2.0** → Funciones reusables, documentadas y testeadas

---

## 📝 Changelog V3.R2.C5

### ✨ Nuevas funciones:

🧠 Gen `main.py`

- `main()`: Coordinador del pipeline con capacidad de validación semántica
  
- Integración de `validar_documento()` dentro del flujo, sin interrupciones
  
- Logs de procesamiento por documento, incluso con errores semánticos
  

### 🧪 Cobertura de tests:

- ✅ Flujo ejecutado completo con logs generados
  
- ✅ Comprobación manual de logs `.jsonl` y fallback no bloqueante
  

### 🔄 Mutaciones en módulos relacionados:

- `validator.py`: Invocado condicionalmente, sin alteración directa
  
- `logger.py`: Reutilización de `log_evento()` para trazabilidad
  

### 📈 Derivadas observadas

- **∆r = +2.0** → Expansión del flujo principal con validación integrada
  
- **∆c = +3.0** → Madurez funcional y trazabilidad alcanzada

---

## Cierre V.3

### 🎯 Mutaciones integradas:

- Validación semántica (`validator.py`) con trazabilidad por `zone`, `error_code`, `severity`, `razones`
  
- Corrección inteligente OCR con `ocr_dict.json`
  
- Exportación estructurada y AI-ready con carpetas por documento
  
- Orquestación tolerante vía CLI `--semantic-check`, `--tolerante`
  
- Hashing único por documento para evitar reprocesamientos
  

### 🧬 Genes mutados:

- `validator.py`, `enhancer.py`, `exporter.py`, `main.py`, `utils.py`, `enhancer_utils.py`, `logger.py`

### 🧪 Test y cobertura:

- ✅ 100% en `test_validator.py`, `test_enhancer.py`, `test_utils.py`, `test_exporter.py`

### 📦 Nuevos outputs:

- `.txt`, `.md`, `.jsonl` por hash
  
- `.jsonl` de errores semánticos
  
- `ocr_dict.json` para control OCR
  

### 📈 Derivadas observadas:

- **∆r = +5.0**
  
- **∆c = +6.0**
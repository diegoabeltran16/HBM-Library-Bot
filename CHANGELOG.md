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

## 📝 Changelog V3.R2.C1

### ✨ Nuevas funciones:

#### 🧠 Gen `validator.py`

- `validar_documento()`: Coordinador tolerante con logging estructurado
  
- `validar_resumen()`, `validar_secciones()`, `validar_citas_referencias()`: Heurísticas semánticas
  
- `mapear_codigo()`, `clasificar_severidad()`, `detectar_zona()`: Trazabilidad ética
  

#### 🧬 Gen `enhancer.py`

- `reparar_encoding()`, `reparar_cid()`, `reparar_ocr_simbolos()`, `normalizar_unicode()`
  
- `pipeline_hooked_enhancer()`: Reparador adaptativo por impacto
  
- `enriquecer_texto()`: Interfaz sencilla para limpieza semántica
  

#### 🧩 Gen `enhancer_utils.py`

- `acumular_stats()`: Acumulación de métricas por función
  
- `aplicar_diccionario()`: Diccionario externo para OCR (`ocr_dict.json`)
  

---

### 🧬 Nuevos archivos/tipos de exportación:

- `.jsonl` de errores semánticos por hash, con `zone`, `error_code`, `severity`, `razones`
  
- `.md` enriquecido con encabezados YAML (`exporter.py`)
  
- `.jsonl` por párrafos listos para AI (`exportar_archivos()`)
  

---

### 🧪 Cobertura de tests:

- ✅ 100% cobertura funcional en `test_validator.py`, `test_enhancer.py`
  
- ✅ Validaciones de `hash`, encabezados, resumen y citas
  
- ✅ Test de impacto adaptativo (cuenta cuántas correcciones por paso)
  

---

### 🔄 Mutaciones en módulos relacionados:

- `logger.py`: Agrega `log_validacion()` para eventos estructurados
  
- `utils.py`: Añade `calcular_hash_md5()` para trazabilidad por documento
  
- `exporter.py`: Limpieza de exportación con `slugify()`, integración de hash + título
  

---

### 📈 Derivadas observadas

- **∆r = +6.0** → Nuevas funciones en tres genes (`validator`, `enhancer`, `utils`)
  
- **∆c = +8.0** → Trazabilidad total, fallback tolerante, interfaz modular y testable
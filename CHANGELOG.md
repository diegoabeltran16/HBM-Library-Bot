# 📜 CHANGELOG – OpenPages Pipeline
> Registro evolutivo helicoidal del sistema, agrupado por vueltas (Vx) y genes funcionales.

---

## 🌀 Vuelta #3 – Validaciones Semánticas y Gen Trazador
📅 2025-04-24

### 🧠 Mutación semántica – `validator.py`
- Agrega `validar_resumen`, `validar_secciones`, `validar_citas_referencias`
- Detecta errores en resumen académico (longitud, ausencia)
- Verifica presencia de secciones clave y citas referenciales
- Exporta logs por `zone`, `severity` y `error_code`

### 🧩 Gen auxiliar nuevo – `utils.py`
- `es_pdf_complejo()`: activa fallback para OCR
- `contiene_formula()`: detecta simbología matemática sospechosa
- `normalizar_texto()`: mejora matching semántico
- `calcular_hash_md5()`: permite trazabilidad documental

### 🧬 Gen trazador – `logger.py`
- Nuevo `log_validacion()` → exporta errores semánticos como eventos AI-ready
- Crea archivo `.jsonl` por ejecución y por hash
- Estilo multilingüe y visual con emojis

### 🧪 Tests agregados
- `tests/test_utils.py`: 6 pruebas unitarias cubren estructura, fórmula y hash
- `tests/test_validator.py`: 6 pruebas unitarias + 1 documento real
- `tests/test_logger.py`: incluye validación por hash y severidad

### 🧬 Gen: enhancer
- **feat(D): `pipeline_hooked_enhancer()` con retry adaptativo y utils**
  - Se introduce un pipeline de enriquecimiento semántico con control de impacto.
  - Soporta reintentos basados en umbral de correcciones (`retry_umbral`) y OCR dictionary externo (`ocr_dict.json`).
  - Modularizado en `enhancer_utils.py` con separación de `acumular_stats` y `aplicar_diccionario`.
  - Todos los tests pasan satisfactoriamente. Cobertura de flujo asegurada.
  - `(V3.R3.C1 / gen=enhancer, b=2, ∆r=+1, ∆c=+0.6)`

---

> Cada cambio fue diseñado como una **mutación genética trazable**, midiendo ∂c/∂t (complejidad en el tiempo) y preparando el terreno para visualizaciones semánticas evolutivas.

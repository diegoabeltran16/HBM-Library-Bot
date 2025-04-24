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

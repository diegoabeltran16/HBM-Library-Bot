# 🤝 Guía para Contribuir a OpenPages-pipeline

¡Gracias por tu interés en colaborar!  
Este proyecto busca construir herramientas abiertas para organizar y analizar conocimiento técnico y científico, y cada contribución suma.

---

## 📦 ¿Cómo empezar?

1. **Haz un fork** de este repositorio.
2. Crea una nueva rama:  
  `git checkout -b feat/tu-mejora`
3. Realiza tus cambios localmente.
4. Sigue el formato de commits (abajo).
5. Abre un Pull Request claro y descriptivo. ¡Nos encantará revisarlo!

---

## ✅ Tipos de contribución bienvenidos

| Tipo | Ejemplos |
| --- | --- |
| Documentación | Mejoras en el README, nuevos ejemplos, tutoriales |
| Código | Nuevas funciones, refactor, optimizaciones |
| Testeo | Tests unitarios, cobertura, casos edge |
| Reportes | Issues bien descritos y reproducibles |
| Ideas | Propuestas en discusiones o nuevos módulos |

---

## 🧠 Formato de commits

> Sistema diseñado para facilitar:
> 
> - 🔍 Trazabilidad clara del desarrollo
> - 🧠 Metacognición del proceso (saber qué lo que se aprende y cuándo)
> - 📦 Refactorizaciones controladas y documentación sincronizada
> - 🚀 Escalabilidad futura para equipos y CI/CD

---

## 🧩 Estructura de un mensaje de commit

```
[tipo](estado): descripción breve - (C-#,m.#,b.#)
```

| **Sección** | **Significado** | **Ejemplo** |
| --- | --- | --- |
| `C-#` | Ciclo de desarrollo | `C-1` (Fase 1: MVP) |
| `m.#` | Módulo trabajado (parser=1, cleaner=2, ...) | `md.3` = `classifier.py` |
| `b.#` | Bloque funcional o acción puntual | `bloq.2` = `test` |
| `[tipo]` | Tipo de cambio (`feat`, `fix`, `refac`, `docs`, `test`) | `feat` = nueva función |
| `(estado)` | Estado actual del cambio (`(p)` progreso, `(D)` done) | `(D)` = terminado |

---

## 🛠 Tipos recomendados

| Tipo | Uso |
| --- | --- |
| `feat` | Nueva funcionalidad implementada |
| `fix` | Corrección de bug |
| `refac` | Refactorización de código sin cambiar funcionalidad |
| `test` | Test nuevo o ajustado |
| `docs` | Cambios en documentación |

---

## 🧠 Ejemplos de commits

```
feat(D): función extract_text() inicial - (C-1,m.1,b.1)
```

---

## 💬 ¿Dudas? ¿Ideas?

Podés:

- Abrir una [Issue](https://github.com/diegoabeltran16/OpenPages-pipeline/issues)
- Escribirnos directamente desde tu fork con sugerencias
- O dejar comentarios en tu PR

Gracias por construir conocimiento abierto con nosotr@s 🌍✨
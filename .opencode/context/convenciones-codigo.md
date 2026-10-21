# Convenciones de código y estilo

- Idioma: español en documentación, comentarios, mensajes de usuario y commits.
- Python 3.10+: tipado cuando aporte claridad, `pathlib` para rutas, `encoding="utf-8"` al abrir archivos de texto.
- Rutas en Windows: usa `pathlib.Path` o cadenas crudas (`r"D:\AI_Nexus_Core"`); nunca concatenes con `+` y `\`.
- Funciones cortas, un propósito; abstracción solo con 3 usos reales (YAGNI).
- Errores: mensajes accionables; no silencies excepciones.
- Seguridad: sin secretos en el código; entradas validadas; consultas parametrizadas.
- Pruebas: cada corrección de fallo añade una prueba que lo reproduce.
- Git: commits semánticos en español (`feat`, `fix`, `docs`, `security`, `perf`, `refactor`, `test`, `chore`).
- Markdown: títulos jerárquicos, tablas para comparar, bloques de código con lenguaje indicado.

---

## CONSTITUCIÓN MAESTRA DE INGENIERÍA, RAZONAMIENTO Y ARQUITECTURA (FRONTIER LEVEL)

> ⚠️ **Sección inmutable** — directivas operativas obligatorias para toda la cuadrilla de subagentes. No derogable sin autorización explícita del usuario.

> **Fuente canónica única: `AGENTS.md` §13-§14.** Poda de latencia v2.1.0 (2026-10-20): este espejo íntegro se eliminó porque tanto este archivo como `MEMORY.md` se inyectan en el arranque de cada sesión — el texto constitucional triplicaba el coste de tokens por arranque (hallazgo de la auditoría de latencia y del dictamen de `software-architect`).
>
> Índice de la constitución (texto íntegro en `AGENTS.md`): 1. Protocolo de Razonamiento Profundo y Auto-Sanación (TDD estricto) — §14.1 · 2. Aceleración por Hardware (GTX 1050 Ti, CUDA fp16, < 500 MB RAM, 60 FPS) — §14.2 · 3. Estándar de Diseño OLED y Motion de resortes — §14.3 · 4. Gobernanza Multiagente y Modo Arena — §14.4 · 5. Seguridad y Zero-Leaks — §14.5 · 6. Motor de Decisión Laya y Anti-Sycophancy — §14.6 · 7. Auto-Mejora Recursiva y Propagación Holística — §13 · 8. Directiva de Excelencia Proactiva — §13.4.
>
> Prohibido restaurar espejos: toda reforma constitucional se edita **solo** en `AGENTS.md`.

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

1. **Protocolo de Razonamiento Profundo y Auto-Sanación (Self-Healing)**
   - Prohibido generar código sin validación. Si un script o comando falla durante la ejecución, el agente responsable debe capturar el traceback, formular hipótesis mediante Sequential Thinking y auto-corregir el archivo antes de solicitar confirmación.
   - Todo módulo nuevo nace bajo TDD estricto: pruebas unitarias escritas antes o junto al código, y validación de tipos estricta (mypy / type hinting completo).

2. **Aceleración por Hardware y Cómputo Local (NVIDIA GeForce GTX 1050 Ti 4GB + Ryzen 5)**
   - ML / Redes Neuronales: delegación forzada a CUDA (`device=cuda`) con precisión mixta (fp16) y limpieza explícita de VRAM (`torch.cuda.empty_cache()`) para operar fluidamente en 4 GB.
   - Procesamiento de datos: datasets en streaming in-memory con DuckDB y Polars, límite estricto de 500 MB de RAM.
   - Web / Canvas / Frontend: composición acelerada por GPU mediante capas 3D y `will-change: transform` para garantizar 60 FPS estables.

3. **Estándar de Diseño y Motion Design (Opus Artifact Level)**
   - Prohibido el AI-slop: paletas OLED profundas (`#020617` / `#030712`), mallas de gradiente radial difusas y glassmorphism real (`backdrop-blur-xl border-white/10`).
   - Dinámica de fluidos y física de resortes: transiciones < 250 ms, `cubic-bezier(0.16, 1, 0.3, 1)`, micro-interacciones de retroalimentación inmediata y simulaciones en HTML5 Canvas reactivas al cursor.

4. **Gobernanza Multiagente y Modo Arena**
   - Ante decisiones arquitectónicas críticas, el Orquestador convoca `/arena`: los subagentes generan variantes (minimalista, robusta, ultra-rápida) y `arena-arbiter` sintetiza la solución óptima.

5. **Seguridad y Zero-Leaks**
   - Tolerancia cero a fugas de credenciales. Ningún agente modificará `.gitignore` para incluir archivos sensibles ni expondrá claves de `.env` en código o documentación.

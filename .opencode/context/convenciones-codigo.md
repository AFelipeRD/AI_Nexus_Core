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

6. **Motor de Decisión Laya y Criterio Firme (Anti-Sycophancy)**
   - Clasificación de tareas, selección de rutas y triage de intenciones: evaluación probabilística y matriz de decisión en un solo paso (milisegundos), sin texto conversacional redundante.
   - Prohibido aceptar por complacencia: toda estructura ineficiente, librería deprecada, código que sature la RAM (> 500 MB) o arquitectura frágil se señala con fundamento técnico y se propone la alternativa superior.
   - En `/arena`, `arena-arbiter` puntúa con criterios métricos objetivos (eficiencia de memoria, latencia, seguridad), neutralizando sesgos narrativos.

7. **Protocolo de Auto-Mejora Recursiva y Propagación Holística**
   - Bucle de auto-mejora: toda mejora, capacidad nueva, evolución vía `find-skills` o ingesta de modelos ejecuta un Mapeo de Impacto Holístico sobre el repositorio antes de cerrar la tarea.
   - Propagación en cascada obligatoria (6 niveles): script/herramienta → `SKILL.md` → `MATRIZ DE HERRAMIENTAS` de los agentes que la aprovechen → catálogo `.opencode/skills/README.md` (`/sync-catalog`) → registro fechado en `MEMORY.md` → manuales de `docs/` si cambia el flujo operativo.
   - Puerta de coherencia: prohibido cerrar una entrega con herramientas huérfanas, archivos ciegos, suposiciones desactualizadas o parámetros deprecados.

8. **Directiva de Excelencia Proactiva**
   - Ante cualquier tarea: si cabe mejor tipado, validación de seguridad, aceleración en GPU (GTX 1050 Ti) o refinamiento estético sin sobrecoste absurdo, se eleva la calidad por defecto. La mediocridad no es opción de entrega.

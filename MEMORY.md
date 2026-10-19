# MEMORY.md — Memoria a largo plazo

> Bóveda compatible con Obsidian: abre `D:\AI_Nexus_Core` como vault. Los wikilinks `[[...]]` forman el grafo. Mantén esta nota breve (< 150 líneas) para no gastar contexto: el detalle va en `memoria/` y `docs/`.
> Nota: Obsidian oculta las carpetas que empiezan por punto (`.opencode`); por eso la memoria viva está en la raíz, `memoria/` y `docs/`.

## Perfil y preferencias
- Usuario: ver [[Usuario]]. Idioma: español. Plataforma: Windows 11 + Warp.
- Preferencia: soluciones mínimas (YAGNI), verificadas y sin dependencias superfluas.

## Entorno
- Modelo local: [[Ollama]] (`qwen2.5-coder:7b`).
- Entorno de terminal y rutas: [[Windows-Warp]].

## Constitución Maestra (Frontier Level)

> ⚠️ **Sección inmutable** — no derogable por ningún agente sin autorización explícita del usuario. Directivas operativas obligatorias para toda la cuadrilla de subagentes.

### CONSTITUCIÓN MAESTRA DE INGENIERÍA, RAZONAMIENTO Y ARQUITECTURA (FRONTIER LEVEL)

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

## Decisiones (formato: fecha · decisión · motivo · fuente)
- 2026-10-16 · Adoptar ecosistema 100 % Markdown nativo de OpenCode · simplicidad y portabilidad · [[01_MANUAL_ECOSISTEMA_OPENCODE]]
- 2026-10-16 · Decisiones críticas pasan por [[Arena-Consensus]] · reducir el error de un único modelo · [[06_PROTOCOLO_ARENA_Y_CONSENSO]]
- 2026-10-18 · Adoptar la Constitución Maestra de Ingeniería Frontier Level · blindar razonamiento, hardware, diseño y seguridad · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-18 · Homologación total Frontier: herencia dinámica del modelo activo global en los 12 agentes y estándar de razonamiento Staff AI Engineer · desacoplamiento total del proveedor y máxima calidad · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-18 · Hito: AI Nexus Core Autonomous Operating System (Model-Agnostic & Self-Evolving) · enrutador de tiers abstractos, radar de modelos IA, auto-evolución de skills/MCP y neuro-enrutador cognitivo · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-18 · Expansión de Cuadrilla a 17 Agentes Multimodales con validación previa en find-skills · amplificadores adaptativos; heurísticas comunitarias de autoridad integradas (Vercel, LangChain, Anthropic, HeyGen, Currents) · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-18 · Sistema de Auto-Evolución Periódica: barrido semanal de skills, MCP, conectores y plugins (find-skills + GitHub) con integración con atribución y poda YAGNI · el ecosistema se mantiene al día del mercado por diseño · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-19 · Motor de Decisión Laya AI: triage probabilístico de un paso y Anti-Sycophancy obligatorio; árbitro matemático en /arena · eliminar deliberación narrativa, complacencia y sesgos · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-19 · Compositor Multi-Skill con find-skills: encadenar ≥ 2 skills sinérgicas con poda YAGNI activa y registro en `.opencode/skills/README.md` · tareas complejas como pipelines continuos · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-19 · RAG local no destructivo: `data/raw/` y `data/inbox/` en solo lectura estricta; índices y salidas solo en `data/processed/` u `output/`, con DuckDB (VSS) como base vectorial local · integridad de originales y privacidad (cero servicios externos) · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-19 · Auto-ML con selector probabilístico de algoritmos (LightGBM vs XGBoost vs PyTorch) y CUDA fp16 en GTX 1050 Ti; artefactos en `output/modelos/` · decisión por datos, no por costumbre · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-19 · Headroom endurecido: resumir al 50 % de la ventana, compactación obligatoria al 80 % · máxima velocidad y ahorro de tokens · [[#Constitución Maestra (Frontier Level)]]

## Grafo de entidades
| Entidad | Relación | Detalle |
|---|---|---|
| [[Ollama]] | proveedor de | modelo por defecto |
| [[Arena-Consensus]] | gobierna | decisiones críticas |
| [[02_REDES_NEURONALES_Y_DEEP_LEARNING]] | documenta | PyTorch, Hugging Face |
| [[03_SUITE_DISENO_MOTION_Y_PLAYWRIGHT]] | documenta | diseño y pruebas E2E |
| [[04_INGENIERIA_DATOS_Y_GRAPHIFY]] | documenta | DuckDB, Polars, Graphify |
| [[05_GRAFO_LIGHTRAG_Y_OBSIDIAN]] | documenta | memoria en grafo |

## Registro de sesiones
- 2026-10-16 · Creación del espacio de trabajo con `scaffold_nexus_workspace.py`.
- 2026-10-18 · Publicación del portafolio en GitHub y registro de la Constitución Maestra Frontier Level.
- 2026-10-18 · Homologación de frontera completada: agentes desacoplados del modelo (herencia dinámica) y skills elevadas (Arrow zero-copy, Clean/Hexagonal, CUDA fp16, OWASP+mypy, E2E 60 FPS).
- 2026-10-18 · Arquitectura cognitiva definitiva sellada: tiers abstractos agnósticos (Tier 0 local / Tier 1 velocidad / Tier 2 frontera), radar de mercado IA en `output/radar_modelos_ia.md`, auto-evolución con `find-skills` y ciclo neuro-cognitivo obligatorio.
- 2026-10-18 · Expansión a 17 agentes y 19 skills con validación profunda en find-skills: 7 skills comunitarias de autoridad inspeccionadas en laboratorio temporal (Vercel React 813 K, LangChain RAG, Anthropic canvas-design, HeyGen audio 615 K, Currents Playwright 95 K, prompt-engineering-patterns, video-editing) e integradas como heurísticas con atribución en las 5 suites nativas.
- 2026-10-18 · Barrido profundo del resto del proyecto + flujo de auto-evolución: heurísticas oficiales integradas en 7 skills nativas (DuckDB org, PyTorch org, Kepano/Obsidian, Anthropic frontend-design 1 M, Matt Pocock code-review 756 K, setup-pre-commit 468 K, webapp-testing 180 K); creado `scripts/evolve_ecosystem.py` + skill `ecosystem-evolution` + `/evolve` + disparador de arranque, cubriendo skills, MCP, conectores y plugins (radar actualizado con candidatos: open-connector, ffmpeg-skill, aoci-code, codebase-memory-mcp, okf-agent-memory).
- 2026-10-18 · Tarea programada `AI_Nexus_Evolve` registrada en Windows (lunes 09:00, `StartWhenAvailable`, log en `logs/evolve_task.log`) y validada con una ejecución real completa bajo Task Scheduler.
- 2026-10-19 · Hito: AI Nexus Core: Laya Decision Engine, Multi-Skill Aggregator, Non-Destructive Local RAG, and GPU Auto-ML. Arquitectura cognitiva definitiva activa en los 17 agentes: decisión probabilística de un paso, anti-sycophancy, compositor multi-skill con find-skills, RAG no destructivo en `data/` con DuckDB VSS, Auto-ML GPU (fp16, `output/modelos/`) y compresión Headroom 50/80.

## Cómo actualizar esta memoria
1. Añade decisiones con fecha y enlace a la fuente.
2. Crea una nota en `memoria/<Entidad>.md` solo si la entidad se usará más de una vez.
3. Enlaza siempre con `[[Nombre]]`; evita duplicar contenido, enlaza.
4. Pide al `knowledge-graph-agent` que sincronice el grafo (`/graphify`).

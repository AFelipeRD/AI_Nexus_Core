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

> **Fuente canónica única: `AGENTS.md` §13-§14.** Poda de latencia v2.1.0 (2026-10-20): este espejo íntegro se eliminó porque tanto este archivo como `MEMORY.md` se inyectan en el arranque de cada sesión — el texto constitucional triplicaba el coste de tokens por arranque (hallazgo de la auditoría de latencia y del dictamen de `software-architect`).
>
> Índice de la constitución (texto íntegro en `AGENTS.md`): 1. Protocolo de Razonamiento Profundo y Auto-Sanación (TDD estricto) — §14.1 · 2. Aceleración por Hardware (GTX 1050 Ti, CUDA fp16, < 500 MB RAM, 60 FPS) — §14.2 · 3. Estándar de Diseño OLED y Motion de resortes — §14.3 · 4. Gobernanza Multiagente y Modo Arena — §14.4 · 5. Seguridad y Zero-Leaks — §14.5 · 6. Motor de Decisión Laya y Anti-Sycophancy — §14.6 · 7. Auto-Mejora Recursiva y Propagación Holística — §13 · 8. Directiva de Excelencia Proactiva — §13.4.
>
> Prohibido restaurar espejos: toda reforma constitucional se edita **solo** en `AGENTS.md`.

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
- 2026-10-19 · Protocolo Constitucional de Auto-Mejora Recursiva y Propagación Holística (bucle de auto-mejora, cascada de 6 niveles y Puerta de Coherencia) inyectado en AGENTS.md, MEMORY.md y convenciones-codigo.md · cero herramientas huérfanas y cero archivos ciegos · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-19 · Laya AI v2: triage dinámico por vector técnico y selección autónoma desde el pool de opencode.json; generación de medios enrutada a scripts ejecutores del catálogo · agnosticismo y rotación total de modelos (cero anclajes en los 17 agentes) · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-19 · Ingesta autónoma de modelos desde data/inbox/ (auto-researcher) y poda activa de obsoletos/404 (auto-researcher + github-scout) · el pool rota sin dejar configuración muerta · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-19 · Suite multimodal conectada: scripts/nvidia_flux.py (FLUX 3 Klein 1024×1024 → output/images/) y scripts/nvidia_cosmos.py (Cosmos 3 Nano → output/videos/) reparado y sellado en skills y matrices de image-generative-designer y video-media-engineer · propagación en cascada aplicada sobre herramientas existentes · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-19 · Release v2.0.0 publicada en GitHub con tag anotado v2.0.0 · versionamiento semántico formal bajo Keep a Changelog · CHANGELOG.md
- 2026-10-20 · Parallel Multi-Phase DAG Engine: descomposición de peticiones multi-punto en unidades atómicas (T1…Tn), encadenado de dependientes con paso de artefactos, concurrencia inmediata de independientes, matriz granular de recursos por fase (complejidad 1-10, aislamiento atómico de herramientas) y síntesis holística con auto-sanación · reducción radical de latencia en sesiones multi-tarea · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-20 · Certificación de Trazabilidad Concurrente y Actualización de Metadatos GitHub v2.0.0: benchmark en vivo con despachos paralelos reales (streaming DuckDB Tier 1 con fallback dinámico de modelo por saturación del proveedor, auditoría de arquitectura Tier 2, cadena multimodal brief → timeline), README raíz v2.0.0 con badges y Mermaid, metadatos oficiales del repo vía API (descripción + 11 topics) y reporte de trazabilidad publicado en el repo · presencia pública y estado real sincronizados · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-20 · Navegación agéntica browser-use (observe/act/extract con poda de DOM, −85 % tokens) en playwright-testing y automation-browser; percepción de pantalla con scripts/screen_watcher.py para modelos con visión (efímera y bloqueada por .gitignore) · sesiones de navegador y arranques más ligeros sin perder criterio · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-20 · Poda de latencia v2.1.0: Constitución Maestra des-duplicada — fuente canónica única en AGENTS.md §13-§14, espejos de MEMORY.md y convenciones-codigo.md reducidos a puntero con índice · arranque de cada sesión ~2/3 más ligero en capa normativa (recomendación del dictamen de software-architect) · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-20 · Banner social Open Graph oficial (assets/social_preview.png, 1280×640, render PIL con spec de ui-ux-director) + skills comunitarias integradas con atribución (agent-browser, web-design-guidelines, hyperframes-animation, view-transitions, app-store-screenshots, session-compression) + MCP candidates context7 y magic-21st registrados dormants hasta validación de auto-researcher · find-skills v2.1.0 consultado (6 pasadas) · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-20 · Decisión YAGNI documentada: NO se crean agentes nuevos para los dominios web — la cuadrilla de 17 (fullstack-developer, ui-ux-director, automation-browser, ai-multimodal-engineer) ya los cubre; se fortalecen skills y matrices existentes en su lugar · evitar fricción de arranque contradictoria con el objetivo de latencia · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-20 · Release v2.1.0 publicada con tag anotado · 17-agent grid, social preview, browser-use, screen awareness y optimización de latencia · CHANGELOG.md
- 2026-10-23 · Suite visual `mods-visuales` (21 skills / 18 comandos) con cascada §13 cerrada y `.gitignore` endurecido (`!logs/evolve_task.log`, `.playwright-mcp/`) · corregir hallazgos de la validación integral y sincronizar la ingesta concurrente (skill `chat-visual` y comando `/visuales` retirados durante la iteración en paralelo) · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-23 · Migración multimodal decidida: `nvidia_flux.py`/`nvidia_cosmos.py` → Open Generative AI Studio (MIT, 31k estrellas, escritorio local) + `muapi.ai` vía MCP stdio oficial, nube-first y GLM 5.3 orquestando · dictamen VIABLE: GTX 1050 Ti no corre video local; créditos de bienvenida gratuitos confirmados · [[#Constitución Maestra (Frontier Level)]]

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
- 2026-10-19 · Reingeniería total v2.0.0: auto-mejora recursiva holística (§13 de AGENTS.md), Laya dinámico con enrutamiento autónomo de modelos, ingesta/poda de modelos desde `data/inbox/`, scripts multimodales conectados y reparados (`nvidia_cosmos.py` ya persiste el video), catálogos y manuales sincronizados, CHANGELOG v2.0.0, commit + tag anotado `v2.0.0` publicados en GitHub.
- 2026-10-20 · Hito: AI Nexus Core: Parallel Multi-Phase DAG Engine and Dynamic Granular Resource Routing. El Orquestador descompone peticiones multi-punto en DAG, ejecuta en paralelo lo independiente, puntúa cada fase (1-10) para asignar su paquete exclusivo (modelo + subagente + skills + MCPs) y consolida la salida con Self-Healing.
- 2026-10-20 · Hito: Certificación de Trazabilidad Concurrente y Actualización de Metadatos GitHub v2.0.0. Despacho concurrente real con modelos heterogéneos (DeepSeek v4.1 Flash saturado al primer intento → fallback dinámico al modelo de frontera activo), 3 subagentes en paralelo + 1 encadenado (brief → timeline), dictamen de arquitectura «aprobado con reservas», auditoría de colisiones y Constitución por `code-reviewer-security`, README v2.0.0 (badges + Mermaid + tabla de 17), metadatos oficiales vía API y publicación verificada en GitHub.
- 2026-10-20 · Hito: v2.1.0 — 17-Agent Grid, LinkedIn Social Preview, Browser-Use Lightweight Agent, Screen Awareness & Latency Optimization. Poda quirúrgica de output/, banner OG renderizado programáticamente (spec ui-ux-director → ejecución image-generative-designer), navegación agéntica con poda de DOM y primitivas observe/act/extract, screen_watcher.py probado con captura real (1920×1080) y borrado efímero, Constitución des-duplicada (canónica en AGENTS.md §14) y find-skills ×6 consultado con integraciones atribuidas. Pipeline imagen→video de la mascota ejecutado y certificado antes del release (nexus_mascot_3d.png + nexus_mascot_motion.mp4, 300 frames · 60 FPS). Sin crear agentes nuevos: decisión YAGNI documentada.

## Cómo actualizar esta memoria
1. Añade decisiones con fecha y enlace a la fuente.
2. Crea una nota en `memoria/<Entidad>.md` solo si la entidad se usará más de una vez.
3. Enlaza siempre con `[[Nombre]]`; evita duplicar contenido, enlaza.
4. Pide al `knowledge-graph-agent` que sincronice el grafo (`/graphify`).

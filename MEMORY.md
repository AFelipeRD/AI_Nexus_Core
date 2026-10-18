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

## Decisiones (formato: fecha · decisión · motivo · fuente)
- 2026-10-16 · Adoptar ecosistema 100 % Markdown nativo de OpenCode · simplicidad y portabilidad · [[01_MANUAL_ECOSISTEMA_OPENCODE]]
- 2026-10-16 · Decisiones críticas pasan por [[Arena-Consensus]] · reducir el error de un único modelo · [[06_PROTOCOLO_ARENA_Y_CONSENSO]]
- 2026-10-18 · Adoptar la Constitución Maestra de Ingeniería Frontier Level · blindar razonamiento, hardware, diseño y seguridad · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-18 · Homologación total Frontier: herencia dinámica del modelo activo global en los 12 agentes y estándar de razonamiento Staff AI Engineer · desacoplamiento total del proveedor y máxima calidad · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-18 · Hito: AI Nexus Core Autonomous Operating System (Model-Agnostic & Self-Evolving) · enrutador de tiers abstractos, radar de modelos IA, auto-evolución de skills/MCP y neuro-enrutador cognitivo · [[#Constitución Maestra (Frontier Level)]]
- 2026-10-18 · Expansión de Cuadrilla a 17 Agentes: Fullstack y Estudio Multimodal · amplificadores adaptativos de capacidad, no jaulas estáticas · [[#Constitución Maestra (Frontier Level)]]

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
- 2026-10-18 · Expansión a 17 agentes y 19 skills: fullstack-developer, ai-multimodal-engineer, video-media-engineer, image-generative-designer y audio-sound-engineer con sus 5 suites. `find-skills` consultado antes de crearlas: sin habilidades mantenidas aplicables en el registro (solo convex/agent-skills para fullstack, ajeno a nuestra arquitectura).

## Cómo actualizar esta memoria
1. Añade decisiones con fecha y enlace a la fuente.
2. Crea una nota en `memoria/<Entidad>.md` solo si la entidad se usará más de una vez.
3. Enlaza siempre con `[[Nombre]]`; evita duplicar contenido, enlaza.
4. Pide al `knowledge-graph-agent` que sincronice el grafo (`/graphify`).

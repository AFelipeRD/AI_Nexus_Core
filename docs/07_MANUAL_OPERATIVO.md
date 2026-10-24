# 07 · Manual operativo del ecosistema

Enlaces: [[MEMORY]] · [[01_MANUAL_ECOSISTEMA_OPENCODE]] · [[06_PROTOCOLO_ARENA_Y_CONSENSO]]

> Guía integral y manual operativo de AI Nexus Core, generada en la Sesión Maestra de Presentación (2026-10-19).
> Raíz: `D:\AI_Nexus_Core` · Windows 11 · terminal Warp · bóveda de Obsidian.
> **17 agentes · 21 skills · 18 comandos slash · 11 servidores MCP (5 activos) · 2 proveedores de modelos · 7 manuales**

## Contenido

1. ¿Qué es AI Nexus Core?
2. Cómo piensa y opera el sistema (el cerebro)
3. Catálogo de capacidades y subagentes
4. Política de libertad de modelos y diseño
5. Guía rápida de uso

---

## 1. ¿Qué es AI Nexus Core?

**Un sistema operativo autónomo de ingeniería con IA**: una cuadrilla de 17 agentes especializados que piensan, verifican y se auto-corrigen, coordinada por un Orquestador que clasifica cada petición, destila la orden técnica pura y la enruta al especialista correcto. No es un chatbot con plugins: es una arquitectura cognitiva completa.

### Propósito

- Convertir lenguaje natural en trabajo de ingeniería terminado y verificado: investigación, construcción, pruebas, seguridad y publicación.
- Cero fricción: el usuario da la orden; el sistema destila, delega, valida y entrega con evidencia.

### Local-first

- Todo el ecosistema vive en `D:\AI_Nexus_Core`, abierta como bóveda de Obsidian (memoria, grafo y manuales en Markdown).
- Fallback a costo cero con Ollama local (`http://127.0.0.1:11434/v1`): el sistema nunca queda bloqueado por una API externa.
- Los datos no salen de la máquina salvo que la tarea requiera web de forma explícita.

### Filosofía agnóstica de modelos

- Ningún agente ancla un proveedor concreto: todos heredan dinámicamente el modelo activo global definido en `opencode.json`.
- Cambiar de proveedor o añadir una API nueva es un cambio de configuración, nunca de código.
- La auto-percepción del sistema se recalibra al estándar del modelo más potente conectado en la sesión.

### Sin frameworks monolíticos

Regla innegociable nº 1 de `AGENTS.md`: prohibido `class Agent`, CrewAI, LangChain y wrappers de orquestación en Python.

| Entidad | Representación | Razón |
|---|---|---|
| Agente | `.md` con frontmatter YAML | Portable, auditable, versionable, editable por humanos |
| Habilidad | `<slug>\SKILL.md` | La inteligencia vive en protocolos, no en scaffolding |
| Comando | `.md` en `.opencode\commands\` | Cero lock-in a frameworks |

El resultado: el ecosistema funciona igual en OpenCode, Cursor o Warp, y ninguna dependencia puede morir arrastrando el sistema consigo.

### Auto-evolutivo

- La tarea programada de Windows `AI_Nexus_Evolve` (lunes 09:00, `StartWhenAvailable`) ejecuta `/evolve`: barrido semanal de skills, servidores MCP, conectores y plugins (find-skills + radar GitHub), con integración atribuida y poda YAGNI.
- El informe del barrido vive en `output/evolution_report.md`.
- **Ingesta de modelos**: la documentación de modelos o APIs depositada en `data/inbox/` es asimilada por `auto-researcher` (endpoints, ventanas de contexto, tool-calling), que propone la actualización de `opencode.json` y propaga el conocimiento en cascada (§13 de `AGENTS.md`).
- **Poda activa**: los modelos caducados, deprecados o caídos (404) se remueven de la configuración activa y de todo catálogo o manual que los cite.

---

## 2. Cómo piensa y opera el sistema (el cerebro)

El **neuro-enrutador** ejecuta un ciclo cognitivo obligatorio en tres fases ante cualquier petición.

### Fase 1 · Poda y destilación de intención

Los mensajes largos o coloquiales se destilan a la **orden técnica pura** antes de procesar.
Ejemplo: *"...me preguntaba si podrías echarle un vistazo a eso de las ventas que subí..."* → `ANALIZAR data/ventas → top categorías → informe`.
Menos tokens, menos ambigüedad.

### Fase 2 · Activación neurológica selectiva (Progressive Disclosure)

**Prohibido leer el repositorio completo.** Igual que el cerebro humano no activa todas las neuronas para una tarea simple, el sistema consulta el **mapa de sinapsis** — `MEMORY.md`, los `README.md` de catálogo y el grafo de wikilinks `[[...]]` de Obsidian — y enciende **únicamente** el subagente y la skill que exige el dominio de la tarea.

> Evidencia: la sesión que generó este manual documentó el ecosistema completo leyendo solo `opencode.json` y cuatro listados de directorios; ningún agente ni manual fue abierto.

### Fase 3 · Auto-sanación obligatoria (Self-Healing)

Ningún código se entrega sin validación. Si un script falla, el subagente responsable captura el traceback, formula hipótesis con el MCP Sequential Thinking y se auto-corrige antes de entregar. Los módulos nuevos nacen bajo TDD estricto con tipado completo.

### Clasificación y enrutado por tiers de capacidad

| Clasificación | Enrutado | Ejemplo |
|---|---|---|
| Cotidiana | Tier 0 — el Orquestador resuelve directo | Formateo, utilidades < 20 líneas, terminal |
| De utilidad | Tier 1 — síntesis y proceso masivo | Resumir documentos, consultar datos |
| Especializada | Delegación forzada al especialista | ML → `ml-deeplearning-specialist`; UI → `ui-ux-director` |
| Crítica | `/arena` obligatorio (arbitraje Tier 2) | Arquitectura, seguridad, 2+ alternativas |
| Ambigua / matemática | `/think` antes de delegar | Descomposición paso a paso |

| Tier | Perfil | Mapeo en `opencode.json` |
|---|---|---|
| Tier 0 | Ligero / costo cero / local | `small_model` |
| Tier 1 | Alta velocidad y utilidad | pool dinámico |
| Tier 2 | Frontera / razonamiento profundo | `model` (activo global) |

El triage no usa reglas rígidas: el **Motor de Decisión Laya AI** evalúa en un solo paso (milisegundos) el **vector técnico** de cada mensaje — complejidad algorítmica, riesgo, dependencias, consumo de RAM y GPU, criticidad irreversible — y selecciona el modelo óptimo del pool de `opencode.json`. La generación de medios (imagen, video, audio) no pasa por un LLM: se delega a los scripts ejecutores del catálogo (`scripts/nvidia_flux.py` → `output/images/`, `scripts/nvidia_cosmos.py` → `output/videos/`).

### Auto-mejora recursiva y propagación holística (§13 de `AGENTS.md`)

Toda mejora, herramienta o modelo nuevo se propaga en cascada por los seis niveles del sistema antes de cerrar la tarea: script/herramienta → `SKILL.md` → matrices de los subagentes que la aprovechen → catálogo central (`.opencode/skills/README.md` vía `/sync-catalog`) → registro fechado en `MEMORY.md` → manuales de `docs/` si cambia el flujo operativo. La **Puerta de Coherencia** veta entregas con herramientas huérfanas, suposiciones desactualizadas o parámetros deprecados, y la **Directiva de Excelencia Proactiva** eleva la calidad por defecto (tipado, seguridad, GPU, estética) sin sobrecoste absurdo.

### Motor de orquestación concurrente por fases (DAG)

Las peticiones multi-punto se descomponen en **unidades atómicas de trabajo (T1…Tn)** formando un grafo acíclico: las tareas con dependencia de datos se encadenan en secuencia pasando el artefacto resultante; las independientes se ejecutan **en paralelo de inmediato**, sin bloquear la sesión. Cada fase recibe una puntuación de complejidad (1-10) y su paquete exclusivo de recursos — **< 4**: acción directa con modelo ligero en segundos; **≥ 7**: subagente especialista con razonamiento profundo y Thinking — con **aislamiento atómico de herramientas** (solo los subagentes, skills y MCPs que esa fase exige). Las tareas ligeras de un mismo prompt corren en segundo plano mientras el flujo pesado continúa, y el Orquestador consolida todas las salidas con auto-sanación antes de entregar la respuesta unificada.

### Compresión de contexto (Headroom)

Al 50 % de la ventana: resumir. Al 80 %: compactación obligatoria (`/headroom`). Se conserva el objetivo, las decisiones, las rutas de archivos, los errores abiertos y los próximos pasos; se descarta el ruido.

### Latencia de arranque (v2.1.0)

La Constitución Maestra vive una única vez — canónica en `AGENTS.md` §13-§14 — y `MEMORY.md` / `convenciones-codigo.md` solo la referencian por puntero con índice: el texto normativo ya no se triplica en cada arranque de sesión (~2/3 menos en la capa constitucional, recomendación del dictamen de `software-architect`). La navegación agéntica con poda de DOM (`observe`/`act`/`extract`) reduce además ~85 % los tokens por interacción de navegador.

---

## 3. Catálogo de capacidades y subagentes

### Ingeniería de software

| Agente | Responsabilidad |
|---|---|
| `orchestrator` | El cerebro: clasifica, destila, enruta, valida y coordina. Punto de entrada de toda petición |
| `software-architect` | Arquitectura limpia, SOLID, minimalismo guiado por la escalera YAGNI |
| `fullstack-developer` | Next.js, React, TypeScript, Tailwind, FastAPI/Node, SQLite/PostgreSQL/DuckDB |
| `portfolio-git` | Commits semánticos en español y sincronización del portafolio con GitHub |
| `code-reviewer-security` | Auditoría OWASP Top 10, análisis estático, detección de fugas de credenciales |
| `auto-researcher` | Radar de modelos y benchmarks IA; valida documentación oficial antes de aprobar integraciones |
| `github-scout` | Vigila repos virales, releases y modelos nuevos; dispara notificaciones Toast de Windows |

### Datos, ML, diseño y media

| Agente | Dominio | Responsabilidad |
|---|---|---|
| `data-engineer` | Datos | Pipelines OLAP con DuckDB + Polars sobre CSV/Parquet locales, streaming < 500 MB de RAM |
| `ml-deeplearning-specialist` | ML | PyTorch, embeddings locales, CUDA fp16 y control de VRAM para la GTX 1050 Ti de 4 GB |
| `ui-ux-director` | Diseño | Tokens, criterio visual, micro-animaciones con física de resorte. Adaptativo a cualquier dominio estilístico |
| `image-generative-designer` | Imagen | Dirección artística, generación FLUX en NVIDIA Build (`scripts/nvidia_flux.py` → `output/images/`), Pillow/Canvas, SVG paramétrico |
| `audio-sound-engineer` | Audio | Web Audio API, TTS, Whisper, diseño sonoro micro-táctil de baja latencia |
| `video-media-engineer` | Video | Captura automatizada con Playwright, generación Cosmos (`scripts/nvidia_cosmos.py` → `output/videos/`), composición MoviePy/FFmpeg a 60 FPS |
| `ai-multimodal-engineer` | GenAI | IA generativa de frontera, RAG multimodal (texto + imagen + audio), flujos agénticos avanzados |
| `automation-browser` | Navegador | Navegación agéntica browser-use (`observe`/`act`/`extract`, −85 % tokens), Playwright E2E, Crawl4AI, n8n, percepción de pantalla (`scripts/screen_watcher.py`) |
| `knowledge-graph-agent` | Contexto | Grafo de dependencias y memoria persistente: LightRAG, Claude-Mem, Graphify, Obsidian, `MEMORY.md` |
| `arena-arbiter` | Gobernanza | Juez del Modo Arena: puntúa con la rúbrica y emite el dictamen final |

### Modo Arena — coordinación autónoma

Obligatorio (`/arena`) cuando la decisión: (a) define arquitectura o elige tecnología, (b) toca seguridad o credenciales, (c) es irreversible o destructiva, (d) implica un algoritmo o arquitectura neuronal, o (e) tiene dos o más alternativas razonables.

1. **Generación paralela**: 2 o 3 subagentes distintos crean variantes candidatas (minimalista, robusta, ultra-rápida).
2. **Crítica cruzada**: cada subagente ataca las variantes ajenas — fallos, riesgos, complejidad.
3. **Arbitraje**: `arena-arbiter` puntúa con la rúbrica (simplicidad, velocidad, seguridad, robustez). Seguridad ≤ 2 descalifica.
4. **Dictamen**: ganador claro o síntesis de lo mejor de cada variante, registrada en `MEMORY.md`.

### Habilidades (21 skills nativas)

| Suite | Skills |
|---|---|
| Gobernanza | `find-skills` · `ponytail-yagni` · `arena-consensus` · `sequential-thinking` · `headroom-context` · `ecosystem-evolution` |
| Datos | `duckdb-analytics` · `graphify-codebase` · `lightrag-knowledge` |
| ML | `neural-network-ml` · `auto-research` |
| Diseño | `ui-ux-design-suite` · `image-creative-suite` |
| Web y media | `fullstack-architecture` · `playwright-testing` · `video-processing-suite` · `audio-sound-suite` · `ai-multimodal-ops` |
| Visualización | `mods-visuales` |
| Utilidades | `git-portfolio-sync` · `windows-notifier` |

### Comandos slash (18)

| Comando | Propósito |
|---|---|
| `/think` | Descomposición secuencial de problemas complejos o ambiguos |
| `/arena` | Arbitraje de decisiones críticas |
| `/yagni` | Auditoría de alcance y poda de sobre-ingeniería |
| `/headroom` | Compresión de contexto |
| `/analyze-data` | Análisis DuckDB/Polars sobre archivos locales |
| `/train-model` | Entrenamiento ML con CUDA |
| `/craft` `/critique` `/taste` `/animate` | Construcción, crítica, criterio y movimiento de interfaces |
| `/browser-test` | Pruebas E2E en navegador real |
| `/research` `/scout` | Investigación validada · radar GitHub |
| `/security-audit` | Checklist OWASP + secretos antes de publicar |
| `/commit` | Commits semánticos en español |
| `/graphify` | Mapeo del grafo de dependencias |
| `/evolve` | Barrido de auto-evolución del ecosistema |
| `/sync-catalog` | Regenerar los `README.md` de catálogo |

### Servidores MCP

- **Activos (5)**: `github`, `filesystem`, `playwright`, `claude-mem`, `sequential-thinking`.
- **Dormant (6)**: `n8n`, `figma`, `mem0`, `huggingface`, `context7` (documentación actualizada para LLMs), `magic-21st` (generación de componentes UI; requiere `MAGIC_API_KEY` en entorno) — se activan con `"enabled": true` cuando el proyecto los necesita, previa validación de `auto-researcher`.

### Aceleración por hardware (Constitución §2)

- **GTX 1050 Ti 4 GB + Ryzen 5**: ML con `device=cuda`, precisión mixta fp16 y `torch.cuda.empty_cache()` tras cada fase.
- **Datos**: streaming in-memory DuckDB/Polars con límite estricto de 500 MB de RAM.
- **Web**: composición acelerada por GPU y capas 3D para 60 FPS estables.

---

## 4. Política de libertad de modelos y diseño

### Libertad de modelos — confirmada

- El ecosistema **no tiene modelos fijos**: `opencode.json` es la única fuente de verdad (`model`, `small_model` y el pool de proveedores).
- Proveedores configurados: NVIDIA Build NIM (GLM 5.3, Nemotron 3.5 Super VL 120B, DeepSeek v4.1 Flash) y Ollama local (Qwen2.5 Coder 7B); el pool rota con `/evolve` y la ingesta desde `data/inbox/`.
- Cambiar de proveedor: editar `opencode.json` → **todos los agentes heredan al instante**, sin tocar una línea de código de ningún agente.
- Escalera de fallback: modelo activo → Ollama local. El sistema nunca queda sin cerebro.
- Tras editar `opencode.json`, reinicia el servicio (`opencode service restart`) o reabre la terminal para que el cambio surta efecto: la configuración la posee el servicio en segundo plano.

### Política Zero-Leaks de credenciales

- Toda credencial vive en **variables de entorno** (de usuario de Windows y/o `.env`, que está en `.gitignore`) y se referencia en `opencode.json` con el patrón `{env:NOMBRE_DE_VARIABLE}`: `{env:NVIDIA_API_KEY}`, `{env:GITHUB_PERSONAL_ACCESS_TOKEN}`, `{env:OMNIROUTE_API_KEY}`, `{env:HF_TOKEN}`.
- Tolerancia cero a claves pegadas en archivos versionados (Constitución §5). `/security-audit` verifica el diff antes de cada publicación.
- Si una variable no existe, OpenCode la sustituye por cadena vacía (la autenticación fallaría de forma visible, nunca silenciosa).

### Libertad de diseño — confirmada

- **No hay paleta obligatoria.** La regla anti-slop prohíbe la plantilla genérica (degradados morados por defecto, tarjetas idénticas, `lorem ipsum`), no el estilo.
- El `ui-ux-director` define **tokens por proyecto adaptados al contexto real**: un dashboard fintech, un juego de terror y una app médica reciben paletas, tipografía y movimiento distintos.
- Innegociable de accesibilidad y movimiento: contraste WCAG AA (4.5:1 texto / 3:1 interfaz), transiciones < 250-300 ms con `cubic-bezier(0.16, 1, 0.3, 1)` y respeto a `prefers-reduced-motion`.

---

## 5. Guía rápida de uso — 5 órdenes en lenguaje natural

No hace falta memorizar comandos: habla normal, el Orquestador destila, enruta y la cuadrilla trabaja.

1. **Análisis de datos** — *"Analiza `data/ventas.csv`: dime las 5 categorías más rentables por trimestre y déjame un informe en `output/`."*
   → `data-engineer` + `duckdb-analytics`: pipeline en streaming, verificación contra los datos y entrega de la ruta del informe.
2. **ML local en GPU** — *"Entrena un clasificador de texto pequeño con los datos de `data/notas/` usando CUDA, cuidando que quepa en 4 GB de VRAM."*
   → `ml-deeplearning-specialist` + `neural-network-ml`: fp16, `empty_cache`, métricas reales y auto-sanación si la memoria revienta.
3. **Web completa y verificada** — *"Crea una landing para mi cafetería con carrito simple, y cuando la tengas ábrela en el navegador y comprueba que todo funciona."*
   → `fullstack-developer` construye → `ui-ux-director` critica (`/taste`) → `automation-browser` valida E2E → ciclo self-healing → capturas y veredicto.
4. **Investigación y decisión crítica** — *"¿Me conviene DuckDB o SQLite para mi inventario? Investiga y decide."*
   → `auto-researcher` valida fuentes → `/arena` genera variantes y crítica cruzada → `arena-arbiter` dictamina con rúbrica → veredicto registrado en `MEMORY.md`.
5. **Cierre de ciclo seguro** — *"Haz commit de lo que hicimos hoy y publícalo, pero antes revisa que no haya nada peligroso."*
   → `code-reviewer-security` audita el diff (secretos, OWASP) → `portfolio-git` redacta commits semánticos en español → `git push` requiere confirmación explícita del usuario.

### Atajos de precisión

`/think` descompone · `/arena` fuerza el arbitraje · `/yagni` poda alcance · `/headroom` comprime contexto · `/security-audit` audita · `/evolve` actualiza el ecosistema contra el mercado.

---

> **Mantenimiento**: este manual refleja el estado del ecosistema a 2026-10-19. Tras añadir o quitar agentes, skills o comandos, ejecuta `/sync-catalog`; tras decisiones relevantes, actualiza `MEMORY.md` (sección Decisiones y Registro de sesiones).

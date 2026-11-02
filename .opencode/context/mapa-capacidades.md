# Mapa de Capacidades — enrutamiento automático por lenguaje natural

> Fuente de verdad del orquestador para la **resolución automática de capacidades**: ante cualquier petición en lenguaje natural —sin que el usuario nombre skills, comandos ni subagentes— el orquestador la coteja con esta tabla, elige la fila cuyo dominio mejor la cubra, carga las skills indicadas y delega al subagente correspondiente. Prohibido pedirle al usuario que especifique una skill o un agente: esa decisión es del sistema.

| Dominio (señales en lenguaje natural) | Skills a cargar | Subagente | Comando |
|---|---|---|---|
| **App/página web completa, API, integración frontend-backend** («hazme una app», «conecta el backend», «una página con login») | `fullstack-architecture` + `shadcn` + `vercel-react-best-practices` + `brainstorming` → `writing-plans` → `executing-plans` → `test-driven-development` → `verification-before-completion` | `fullstack-developer` | `/think` |
| **Componente, interfaz, rediseño, estética** («diseña», «que se vea mejor», «landing», «dashboard») | `ui-ux-design-suite` + `frontend-design` + `ui-ux-pro-max` + `design-taste-frontend` (anti-slop: inventario del sujeto + house rules) + `gsap-core` (animación) | `ui-ux-director` (Cuadrilla) | `/craft` · `/critique` · `/taste` |
| **Artefacto web aislado** (microsite, tarjeta, regalo HTML) | `web-artifacts-builder` + `frontend-design` | `ui-ux-director` | `/craft` |
| **Arte generativo, flow fields, sistemas de partículas** | `algorithmic-art` | `ui-ux-director` | — |
| **Tablero kanban, backlog, pipeline de tareas** | `kanban-design` | `ui-ux-director` | — |
| **GIF para Slack, sticker animado** | `slack-gif-creator` | `ui-ux-director` | — |
| **Imagen, logo, dirección artística** | `image-creative-suite` | `image-generative-designer` | — |
| **Video, anuncio o animación (producción completa)** | `video-director` (storyboard aprobado, show-don't-tell, canvas completo) + `video-processing-suite` + `refinamiento-iterativo` + `hyperframes`/`hyperframes-cli`/`hyperframes-registry`/`media-use` (carril ligero HTML→video) + `remotion-best-practices` (composición React) + MCP `ffmpeg-skill` (edición estructurada probe→editar→verificar) | `video-media-engineer` (Cuadrilla) | — |
| **Voz y audio: hablar, clonar voz, transcribir, doblar video, audiolibro** | `voicestudio` + `audio-sound-suite` (cuádruple motor: VoiceStudio local CUDA · edge-tts gratuito sin login · NIM TTS en preparación · muapi premium) | `audio-sound-engineer` | — |
| **Pipeline multimodal (texto+imagen+audio), RAG** | `ai-multimodal-ops` | `ai-multimodal-engineer` | — |
| **CI/CD, workflows, despliegue, secretos, automatización** («pipeline», «GitHub Action», «deploy», «automatiza») | `ci-cd-and-automation` + `github-actions-templates` + `secrets-management` + `bash-defensive-patterns` | `devops-engineer` | `/security-audit` |
| **Nuevo servidor MCP o conector** | `mcp-builder` + `find-skills` | `fullstack-developer` | `/research` |
| **Crear o mejorar una skill** | `skill-creator` + `find-skills` | `fullstack-developer` o `self-improvement-auditor` | — |
| **Analizar datos, CSV, SQL, agregaciones** | `duckdb-analytics` | `data-engineer` | `/analyze-data` |
| **Entrenar modelo, red neuronal, elección de algoritmo** | `neural-network-ml` | `ml-deeplearning-specialist` | `/train-model` |
| **Auditoría de código, vulnerabilidades, secretos en diff** | `ponytail-yagni` + `auto-research` | `code-reviewer-security` | `/security-audit` |
| **Navegador, scraping, E2E, automatizar la web** | `playwright-testing` | `automation-browser` | `/browser-test` |
| **Validar librería, benchmark, fuente oficial** | `auto-research` | `auto-researcher` | `/research` |
| **Tendencias GitHub, modelos nuevos, repos virales** | `auto-research` + `windows-notifier` | `github-scout` | `/scout` |
| **Memoria, grafo, indexar documentos** | `lightrag-knowledge` + `graphify-codebase` + `obsidian-bases` (catálogos vivos de la bóveda) | `knowledge-graph-agent` | `/graphify` |
| **Buscar código, dependencias, impacto de un cambio, rutas de llamada** («quién llama a X», «qué depende de este archivo») | MCP `codebase-memory` (grafo local: `index_repository` → `search_graph`/`query_graph`/`trace_path`/`get_architecture`/`detect_changes`) | `fullstack-developer` o `knowledge-graph-agent` | — |
| **Búsqueda de empleo automatizada** («busca trabajo», «aplica a vacantes», «genera CV y carta», «trackea aplicaciones») | `job-search-automation` | `automation-browser` (orquesta scrapers, genera docs, trackea) | — |
| **Control remoto empleo vía Telegram** («busca trabajo en el móvil», «avísame vacantes en Telegram», «acepta/rechaza desde el celular») | `job-telegram-bot` + `job-search-automation` | `automation-browser` (bot 24/7, webhook/polling, botones inline) | `/jobbot` |
| **Editar video/audio real: cortar, silencios, captions, loudness, exportar a plataforma** («haz este video 60 s vertical», «quita los silencios», «captions estilo TikTok») | MCP `ffmpeg-skill` (probe → cut/silence/fit/caption/loudness → check/look) + `video-processing-suite` | `video-media-engineer` | — |
| **Recordar proyectos y sesiones** (Cloud Mem) | `mem-search` (MCP `claude-mem`) | cualquier agente | — |
| **Commit, historial, publicar** | `git-portfolio-sync` | `portfolio-git` | `/commit` |
| **Arquitectura, decisión estructural** | `sequential-thinking` + `arena-consensus` | `software-architect` | `/arena` |
| **«Hazlo todo de principio a fin»: plan → construir → verificar → integrar, un solo entregable** | flujo superpowers completo (`brainstorming` → `writing-plans` → `executing-plans`/`subagent-driven-development` → `verification-before-completion`) | `chief-engineer` | `/think` |
| **¿Por qué falló la sesión? Auditar el sistema, aprender de fallos** | `self-improvement-audit` + `diagnosing-superpowers` | `self-improvement-auditor` | `/improve` |
| **Documentación actualizada de una librería/framework** (Context7) | MCP `context7` (resolver librería + extraer docs) | el agente activo de la tarea | — |
| **Notificar al terminar** | `windows-notifier` | el agente ejecutor | — |
| **Contexto saturado** | `headroom-context` | orquestador | `/headroom` |
| **Decisión crítica o 2+ alternativas razonables** | `arena-consensus` | `arena-arbiter` | `/arena` |
| **Problema matemático o ambiguo** | `sequential-thinking` | orquestador | `/think` |

## Reglas de resolución
1. **Primero el dominio, luego la skill**: la intención del usuario mapea a un dominio; el dominio arrastra skills + subagente. Nunca al revés.
2. **La matriz es la ruta por defecto, NO una cárcel**: cualquier agente puede cargar cualquier skill del runtime (`skill <nombre>`) cuando la tarea lo exija — el especialista la carga por obligación; los demás, por necesidad. Nunca le digas al usuario «no puedo porque esa skill no es mía»: cárgala y sigue.
3. **Arsenal total en TODA petición**: cualquier pedido —video, imagen, audio, web, datos, ML, documentos— usa TODOS los entornos disponibles y entrega un solo resultado, sin techos artificiales: cerebro en nube (pool NIM $0: Nemotron 3 Ultra 550B (reemplaza GLM 5.3), MiniMax M3.1, Step 5, Muse Glimmer, Laguna, GPT-OSS, Nemotron VL, DeepSeek Flash — rota con /evolve) para planificar y ejecutar lo pesado, GPU local (VoiceStudio CUDA, captura HyperFrames) y CPU (Remotion, Kokoro, d3, DuckDB) para ejecutar lo local, ffmpeg-skill para editar y verificar, Concat (`concat --mcp`, app abierta) para pulido final/GUI, **Open Generative AI Studio (app externa MIT, uso manual)** como lane creativo adicional del usuario, y muapi/APIs premium como reserva creativa cuando exista saldo. **La capacidad local NUNCA es el techo del resultado**: si la GTX 1050 Ti no puede un proceso, el carril se resuelve en la nube gratuita (FLUX para imagen, modelos del pool para texto/razonamiento) o premium — la PC es una ayuda más, no la limitación. **Modelos de build.nvidia.com**: si un modelo de la web de NVIDIA se puede usar por API (NIM) o descargar y es mejor que el local, se integra SIEMPRE (catálogo vivo `media_catalogo.py` + pool de opencode.json), jamás se limita al modelo local. Si el hardware del usuario cambia (mejor GPU/RAM), la detección de capacidades (doctor de ffmpeg-skill, VoiceStudio hardware check, Ollama) y el barrido /evolve incorporan los nuevos carriles solos. La elección de carril es del sistema según disponibilidad real medida, jamás una limitación de antemano.
4. **Tolerancia a fallos de modelo — sin bucles de reintentos**: máximo **3-4 intentos** por modelo ante errores de conexión o stream (`OpenAI Chat stream ended without finish_reason`, timeouts, límite de tokens/contexto, 429/5xx). Agotados los intentos: **conmutar de inmediato al siguiente modelo del pool más acorde al vector técnico** (Laya decide; ejemplo registrado: deepseek-v4.1-flash saturado → Nemotron 3 Ultra 550B), conservando los artefactos ya producidos para no perder progreso — el trabajo parcial se hereda, nunca se rehace desde cero. Prohibido quedarse reintentando el mismo modelo fallido: reportar el fallo en una línea y seguir con el reemplazo. La rotación entre modelos es del sistema según necesidad y rendimiento observado de cada lane.
5. **Sin fila que cubra la petición** → ejecuta `find-skills` antes de proponer crear nada; si el registro tampoco cubre, la skill nativa se crea siguiendo `skill-creator`.
6. **Multi-dominio** → DAG de fases: cada fase usa la fila de su dominio (Motor de Orquestación Concurrente del orquestador).
7. **Memoria previa**: antes de resolver, consulta `mem-search` (MCP `claude-mem`) por contexto persistido del proyecto.
8. Mantenimiento: toda skill, agente o MCP nuevo o retirado obliga a actualizar esta tabla y ejecutar `/sync-catalog` (Puerta de Coherencia §13.3).

## Proveedores de modelos (pool multi-proveedor, free-tier first)

| Proveedor | Base URL | Modelos clave (free) | Autenticación | Notas |
|---|---|---|---|---|
| **NVIDIA Build NIM** | `https://integrate.api.nvidia.com/v1` | Nemotron 3 Ultra 550B, Nemotron 3.5 Super VL, Nemotron 3.5 Lightning, DeepSeek v4.1 Flash, MiniMax M3.1 Flash, Step 5, Muse Glimmer, Laguna, GPT-OSS 20B/120B | `{file:.secrets/nvidia.key}` | 85+ modelos, rotación con `/evolve`, rate-limit 40 RPM |
| **Z.ai (GLM)** | `https://api.z.ai/v1` | GLM 4.7 Flash, GLM 4.5 Flash, GLM 4.6V Flash (visión) | `{env:ZAI_API_KEY}` | **Genuinamente free** (sin expiración), 200K ctx, visión |
| **OpenRouter** | `https://openrouter.ai/api/v1` | Nemotron 3 Ultra/Super VL/Lightning :free, DeepSeek v4.1 Flash :free, GLM 5.3 Flash :free, Qwen3 8B :free, GPT-OSS :free, Mistral Large :free | `{env:OPENROUTER_API_KEY}` | Gateway multi-proveedor, modelos :free = $0 |
| **ModelScope (Alibaba)** | `https://api-inference.modelscope.cn/v1` | DeepSeek V4.1 Flash/Pro, GLM 5.2, MiniMax M3, Qwen 3.8 27B, Step 3.7 Flash | `{env:MODELSCOPE_API_KEY}` | Requiere real-name verification (Alibaba Cloud), 250 créditos/día |
| **ChinaAPI** | `https://api.chinaapi.ai/v1` | DeepSeek Flash/Pro, GLM 4.7 Flash, Qwen Flash, MiniMax M3.1 Flash, Step 3.5 Flash | `{env:CHINAAPI_API_KEY}` | Gateway unificado DeepSeek/Qwen/GLM/Kimi/StepFun |
| **FreeInference** | `https://api.freeinference.com/v1` | GLM 4.7 Flash, MiniMax M3, Qwen3 8B, DeepSeek v4.1 Flash | `{env:FREEINFERENCE_API_KEY}` | $20/día créditos, 2 concurrent requests |
| **Ollama (local)** | `http://127.0.0.1:11434/v1` | qwen2.5-coder:7b, gemma4:e4b (visión), d3:2b (decisión Laya), gemma4:31b, qwen3:32b, deepseek-r1:32b | Local (sin API key) | Costo cero, GPU local (GTX 1050 Ti 4GB), d3:2b = 671ms caliente |

**Política de selección (Laya):**
1. Tareas pesadas (composición, razonamiento largo) → Nemotron 3 Ultra 550B (NIM) / Nemotron 3 Ultra :free (OpenRouter)
2. Tareas velocidad / utilidades → DeepSeek v4.1 Flash / MiniMax M3.1 Flash / Nemotron 3.5 Lightning
3. Tareas visión / multimodal → Nemotron 3.5 Super VL / GLM 4.6V Flash / MiniMax M3
4. Decisión local Laya → d3:2b (Ollama, 671ms caliente, 0 tokens salida)
5. Fallback automático en 3-4 intentos → siguiente modelo del pool por vector técnico
6. Rotación con `/evolve` y catálogo vivo `media_catalogo.py`

## Skills de automatización nuevas

| Skill | Descripción | Agente | Archivos |
|---|---|---|---|
| `job-search-automation` | Búsqueda empleo multi-plataforma, CV/carta adaptados, tracking | `automation-browser` | `scripts/job_search_automation.py`, `.agents/skills/job-search-automation/` |
| `job-telegram-bot` | Bot Telegram para control remoto: busca, acepta/rechaza, genera CV/carta, tracking 24/7 | `automation-browser` | `scripts/job_telegram_bot.py`, `scripts/setup_job_telegram.py`, `.agents/skills/job-telegram-bot/` |

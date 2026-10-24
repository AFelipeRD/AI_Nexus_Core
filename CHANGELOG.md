# Registro de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versionado semántico.

## [Sin publicar]
### Añadido
- **MCP `muapi`** (24 herramientas: imagen, video, audio, lipsync, upscale, face swap, social publishing) cableado en `opencode.json` vía stdio (`npx -y muapi-cli mcp serve`, `MUAPI_API_KEY` por entorno) — **tier premium** de generación multimodal del doble motor (el stack NVIDIA NIM permanece como motor gratuito Tier 0); clave en `.secrets/muapi.key` (Zero-Leaks).
- **Open Generative AI Studio** (Anil-matcha, MIT, 31k estrellas) instalado como proyecto externo (`%LocalAppData%\Programs\Open Generative AI`) — alternativa open-source a Higgsfield con 14 estudios, Cinema Studio y 420+ modelos vía muapi.
- **Suite visual `mods-visuales`** (21 skills / 18 comandos): tema OLED cyberpunk para Open Code (tema `ai-nexus-core` + plugin `oc-plugin-rainbow`) y para Warp (tema y workflows en `assets/warp/`), aplicado de forma predeterminada y automática, sin comandos que ejecutar; instalador `scripts/instalar_mods_visuales.ps1` — 0 tokens, renderizado 100 % del lado del cliente.
- **Cuadrilla de Diseño unificada**: canon de tokens compartido `.opencode/context/tokens-diseno.md` (paleta OLED, resortes, tipografía Impeccable) extendido a TODO medio (web, imagen, video, audio) con protocolo de equipo multiagente (`ui-ux-director` + especialistas) enrutable desde Laya.
- **Piso Remotion local** (`D:\Nexus_Remotion`, proyecto hermano): video programático con React (licencia Free individual), render Chromium en CPU con `concurrency 2` (GTX 1050 Ti libre), puente de keyframes IA (`npm run sync`), composición demo `NexusShowcase` con tokens del canon.
- **Ingestas concurrentes registradas al sellar** (sesiones paralelas): bucle de auto-mejora — agente `self-improvement-auditor` + skill `self-improvement-audit` + comando `/improve` + registro persistente `output/auditoria_sesiones.md` (no versionado), con heurísticas atribuidas de mattpocock/skills@retro (276 K) y affaan-m/ecc@agent-self-evaluation —; agente `devops-engineer` (CI/CD, release engineering con idempotencia y cero Docker) y skill `kanban-design` (tableros con la estética del canon de tokens); mapa de capacidades `.opencode/context/mapa-capacidades.md`; recuentos reales **19/23/19** sellados en `AGENTS.md`, `README.md` y `docs/07`.
### Cambiado
- Skills `image-creative-suite`, `video-processing-suite`, `audio-sound-suite` y `ai-multimodal-ops` + matrices de `image-generative-designer`, `video-media-engineer`, `audio-sound-engineer` y `ai-multimodal-engineer` re-apuntadas al **doble motor multimodal**: **Tier 0 gratuito NVIDIA NIM por defecto** — motor de medios de **catálogo vivo, modelo-agnóstico** (`scripts/media_catalogo.py` + `--modelo`): imagen multi-modelo probada en vivo (flux-3-image-klein y flux.2-klein-4b) vía pexec por function_id; video de catálogo listo — hoy 0 funciones entitled en la cuenta (cosmos3-nano retirado por NVIDIA) con rutas de desbloqueo informadas por el propio script — + **MCP `muapi` premium** para variaciones creativas avanzadas (GTX 1050 Ti 4 GB insuficiente para los motores locales de video del Studio).
- **`scripts/nvidia_flux.py` y `scripts/nvidia_cosmos.py` se preservan y re-etiquetan como Tier 0 (motor gratuito, $0)** tras la prueba en vivo del 2026-10-23 (imagen FLUX 3 Klein generada en `output/images/nexus_nim_test.png` con la clave existente de `.secrets/nvidia.key`): la retirada previa queda revertida por directiva del usuario (**generación 100 % gratuita por defecto**); skills, matrices, orquestador, `docs/07` y `README` documentan el doble motor (NIM gratuito por defecto + muapi premium con saldo $0 pendiente de recarga).
### Corregido
- **Cascada §13 de `mods-visuales`** (hallazgo de la validación integral del 2026-10-23): recuentos reales 21/18 aplicados en `AGENTS.md`, `README.md` y `docs/07` (incluida la tabla de suites); suite registrada en `MEMORY.md`; fecha de v2.1.0 unificada con la del tag real (2026-10-20).
- `.gitignore`: negación `!logs/evolve_task.log` para que el historial de auto-evolución sea auditable en el repo, y cobertura de los temporales `.playwright-mcp/`.

## [v2.1.0] - 2026-10-20 — 17-Agent Grid, LinkedIn Social Preview, Browser-Use Lightweight Agent, Screen Awareness & Latency Optimization
### Añadido
- **Browser-Use Agentic Navigation** en `playwright-testing` y `automation-browser`: poda de DOM (árbol de accesibilidad / elementos interactivos numerados), primitivas `observe()` / `act(indice, accion)` / `extract(esquema)` con objetivo de −85 % de tokens por interacción, y supervisión Laya contra clics destructivos y extracción de datos privados.
- **Screen Awareness**: `scripts/screen_watcher.py` — instantáneas ligeras y efímeras de pantalla o ventana activa (`assets/temp_screen.png`) para auditoría visual por modelos con visión (Nemotron 3.5 Super VL); probado con captura real 1920×1080; sellado en las matrices de `automation-browser` y `knowledge-graph-agent`.
- **Social Preview oficial (Open Graph)**: `assets/social_preview.png` (1280×640) — wordmark, cuadrícula de los 17 subagentes en tarjetas de cristal y chips de Laya AI · DuckDB · CUDA · Multi-Model; render programático PIL a 2× con reducción LANCZOS (spec de `ui-ux-director`, ejecución de `image-generative-designer`).
- **17-Agent Grid consolidado**: README reestructurado en formato modular (tarjetas de métricas verificadas, secciones desplegables, esqueleto de diseño de `ui-ux-director`) con la cuadrilla completa de 17 subagentes en tabla, Mermaid y banner.
- **Parallel Multi-Phase DAG Engine** (promovido de Sin publicar): descomposición en unidades atómicas T1…Tn, concurrencia inmediata de independientes, matriz granular de recursos por fase (complejidad 1-10, aislamiento atómico de herramientas) y síntesis holística con auto-sanación.
- **Vigilancia find-skills v2.1.0** con atribución: `vercel-labs/agent-browser` (1.1 M), `vercel-labs/web-design-guidelines` (762 K), `heygen-com/hyperframes-animation` (980 K), `vercel-react-view-transitions` (161 K), `transitions.dev`, `101-skills/app-store-screenshots` (52 K) y conectores de compresión de contexto (`session-compression` 639, `context-compression` 431) integrados en `ui-ux-design-suite`, `playwright-testing` y `headroom-context`.
- **MCP dormants**: `context7` (documentación actualizada para LLMs) y `magic-21st` (generación de componentes UI; requiere `MAGIC_API_KEY`) añadidos desactivados en `opencode.json` — 11 servidores totales (5 activos) — hasta su validación por `auto-researcher`.

### Optimizado
- **Latencia de arranque de sesión**: la Constitución Maestra vivía triplicada en archivos inyectados en cada arranque (`AGENTS.md` + `MEMORY.md` + `convenciones-codigo.md`). Poda: texto íntegro canonicalizado en `AGENTS.md` §14; espejos sustituidos por puntero con índice — ~2/3 del coste constitucional por arranque recuperado (recomendación del dictamen de `software-architect`).
- **Poda de `output/`**: eliminados artefactos temporales del benchmark de trazabilidad y del pipeline de motion (benchmark/, motion_work/, videos de prueba antiguos); se conservan entregables, documentos vivos y carpetas estructurales.
- **Reparación de coherencia**: bullets de «Errores a evitar» huérfanos en `playwright-testing/SKILL.md` devueltos a su sección; línea de metadatos del banner corregida en el render v2 (el conteo de MCP se omite por diseño: el pool rota).

### Seguridad
- `assets/temp_screen*.png` bloqueado en `.gitignore`: las capturas de percepción de pantalla son efímeras y jamás se versionan.
- Auditoría Zero-Leaks previa a la publicación: `.env`, `.secrets/` y `opencode.json` confirmados fuera de staging; sin patrones de credenciales en el diff final.

## [v2.0.0] - 2026-10-19
### Añadido
- **Motor de Decisión Laya AI**: triage dinámico por vector técnico (complejidad algorítmica, riesgo, dependencias, RAM/GPU) evaluado en un solo paso y en milisegundos; selección autónoma del modelo óptimo desde el pool de `opencode.json` (cero reglas rígidas, cero modelos quemados en los 17 agentes).
- **Protocolo Constitucional de Auto-Mejora Recursiva y Propagación Holística** (§13 de `AGENTS.md`): Mapeo de Impacto Holístico obligatorio, cascada de 6 niveles (script → `SKILL.md` → matrices de agentes → catálogo → `MEMORY.md` → `docs/`) y Puerta de Coherencia del repositorio.
- **Directiva de Excelencia Proactiva**: tipado, validación de seguridad, aceleración GPU (GTX 1050 Ti) y refinamiento estético por defecto, sin sobrecoste absurdo.
- **Ingesta autónoma de modelos**: la documentación depositada en `data/inbox/` se asimila por `auto-researcher`, actualiza `opencode.json` y se propaga a las skills; poda activa de modelos obsoletos o caídos (404) con alertas de `github-scout`.
- **Suite multimodal conectada**: `scripts/nvidia_flux.py` (FLUX 3 Klein, 1024×1024 → `output/images/`) y `scripts/nvidia_cosmos.py` (Cosmos 3 Nano → `output/videos/`) documentados con invocación en terminal, parámetros en inglés, resolución y rutas de salida, y sellados en las matrices de `image-generative-designer` y `video-media-engineer`.
- **Compositor Multi-Skill** y **herencia dinámica de modelos** consolidados como columnas vertebrales del sistema operativo autónomo.

### Corregido
- `scripts/nvidia_cosmos.py` no persistía el video: ahora guarda el artefacto (URL o base64) en `output/videos/` y avisa con `[AVISO]` si la API no devuelve artefacto descargable; ambos scripts con tipado completo, timeouts y códigos de salida.
- `image-creative-suite/SKILL.md` restaurado íntegro (gramática visual, composición, referencias validadas) y fusionado con la herramienta oficial FLUX; frontmatter completo, versión 1.1.
- `requirements.txt`: declarada la dependencia `requests` que requieren ambos scripts de NVIDIA Build.
- Coherencia de catálogos y manuales: recuentos reales (20 skills, 18 comandos), proveedores vigentes del pool y prohibición de anclar modelos por agente en el frontmatter, aplicados en `AGENTS.md`, `docs/01` y `docs/07`.

### Seguridad
- Auditoría Zero-Leaks previa a la publicación: `.env`, `.secrets/` y `opencode.json` confirmados como ignorados por Git; las claves solo se leen en tiempo de ejecución desde `.secrets/nvidia.key` y variables de entorno.

## [0.1.0] - 2026-10-16
### Añadido
- Estructura inicial del ecosistema AI_Nexus_Core, 100 % Markdown, nativa para OpenCode.
- 12 agentes con matriz de herramientas obligatorias, 14 habilidades, 17 comandos slash.
- Configuración `opencode.json` con Ollama local, OmniRoute como fallback y 8 servidores MCP.
- Manuales `docs/01` a `docs/06`, contexto estable y utilerías en `scripts/`.

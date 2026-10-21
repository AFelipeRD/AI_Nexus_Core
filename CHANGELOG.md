# Registro de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versionado semántico.

## [Sin publicar]

## [v2.1.0] - 2026-10-19 — 17-Agent Grid, LinkedIn Social Preview, Browser-Use Lightweight Agent, Screen Awareness & Latency Optimization
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
- Manuales `docs/01` a `docs/06`, con
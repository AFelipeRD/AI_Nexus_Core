# Mapa de Capacidades — enrutamiento automático por lenguaje natural

> Fuente de verdad del orquestador para la **resolución automática de capacidades**: ante cualquier petición en lenguaje natural —sin que el usuario nombre skills, comandos ni subagentes— el orquestador la coteja con esta tabla, elige la fila cuyo dominio mejor la cubra, carga las skills indicadas y delega al subagente correspondiente. Prohibido pedirle al usuario que especifique una skill o un agente: esa decisión es del sistema.

| Dominio (señales en lenguaje natural) | Skills a cargar | Subagente | Comando |
|---|---|---|---|
| **App/página web completa, API, integración frontend-backend** («hazme una app», «conecta el backend», «una página con login») | `fullstack-architecture` + `brainstorming` → `writing-plans` → `executing-plans` → `test-driven-development` → `verification-before-completion` | `fullstack-developer` | `/think` |
| **Componente, interfaz, rediseño, estética** («diseña», «que se vea mejor», «landing», «dashboard») | `ui-ux-design-suite` + `frontend-design` + `ui-ux-pro-max` | `ui-ux-director` (Cuadrilla) | `/craft` · `/critique` · `/taste` |
| **Artefacto web aislado** (microsite, tarjeta, regalo HTML) | `web-artifacts-builder` + `frontend-design` | `ui-ux-director` | `/craft` |
| **Arte generativo, flow fields, sistemas de partículas** | `algorithmic-art` | `ui-ux-director` | — |
| **Tablero kanban, backlog, pipeline de tareas** | `kanban-design` | `ui-ux-director` | — |
| **GIF para Slack, sticker animado** | `slack-gif-creator` | `ui-ux-director` | — |
| **Imagen, logo, dirección artística** | `image-creative-suite` | `image-generative-designer` | — |
| **Video, clip, motion** | `video-processing-suite` | `video-media-engineer` | — |
| **Sonido, TTS, audio de interfaz** | `audio-sound-suite` | `audio-sound-engineer` | — |
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
| **Memoria, grafo, indexar documentos** | `lightrag-knowledge` + `graphify-codebase` | `knowledge-graph-agent` | `/graphify` |
| **Recordar proyectos y sesiones** (Cloud Mem) | `mem-search` (MCP `claude-mem`) | cualquier agente | — |
| **Commit, historial, publicar** | `git-portfolio-sync` | `portfolio-git` | `/commit` |
| **Arquitectura, decisión estructural** | `sequential-thinking` + `arena-consensus` | `software-architect` | `/arena` |
| **¿Por qué falló la sesión? Auditar el sistema, aprender de fallos** | `self-improvement-audit` + `diagnosing-superpowers` | `self-improvement-auditor` | `/improve` |
| **Documentación actualizada de una librería/framework** (Context7) | MCP `context7` (resolver librería + extraer docs) | el agente activo de la tarea | — |
| **Notificar al terminar** | `windows-notifier` | el agente ejecutor | — |
| **Contexto saturado** | `headroom-context` | orquestador | `/headroom` |
| **Decisión crítica o 2+ alternativas razonables** | `arena-consensus` | `arena-arbiter` | `/arena` |
| **Problema matemático o ambiguo** | `sequential-thinking` | orquestador | `/think` |

## Reglas de resolución
1. **Primero el dominio, luego la skill**: la intención del usuario mapea a un dominio; el dominio arrastra skills + subagente. Nunca al revés.
2. **Sin fila que cubra la petición** → ejecuta `find-skills` antes de proponer crear nada; si el registro tampoco cubre, la skill nativa se crea siguiendo `skill-creator`.
3. **Multi-dominio** → DAG de fases: cada fase usa la fila de su dominio (Motor de Orquestación Concurrente del orquestador).
4. **Memoria previa**: antes de resolver, consulta `mem-search` (MCP `claude-mem`) por contexto persistido del proyecto.
5. Mantenimiento: toda skill, agente o MCP nuevo o retirado obliga a actualizar esta tabla y ejecutar `/sync-catalog` (Puerta de Coherencia §13.3).

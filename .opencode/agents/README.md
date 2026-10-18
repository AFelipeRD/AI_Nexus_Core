---
description: "Catálogo de agentes (documento informativo, no es un agente)"
mode: subagent
hidden: true
---
# Catálogo de agentes

Cada agente es un archivo `.md` con frontmatter YAML (`description`, `mode`, `model`, `temperature`, `permission`) y un cuerpo con su rol, reglas y la sección **MATRIZ DE HERRAMIENTAS Y SKILLS OBLIGATORIAS**.

## Modos
- `primary`: agente con el que conversas directamente (cambia con `Tab`).
- `subagent`: especialista invocado con `@nombre` o delegado por otro agente mediante la herramienta Task.

## Tabla de responsabilidades
| Agente | Responsabilidad principal | Skills | MCP |
|---|---|---|---|
| `orchestrator` | Clasificar la petición (cotidiana, especializada o crítica) antes de actuar. | `find-skills`, `ponytail-yagni`, `headroom-context`, `arena-consensus`, `sequential-thinking` | `sequential-thinking`, `filesystem` |
| `arena-arbiter` | Verificar que existan 2 o 3 variantes genuinamente distintas y sus críticas cruzadas. | `arena-consensus`, `sequential-thinking`, `ponytail-yagni` | `sequential-thinking` |
| `ml-deeplearning-specialist` | Buscar en el Hub (MCP de Hugging Face) arquitecturas, modelos preentrenados y datasets antes de construir desde cero. | `neural-network-ml`, `sequential-thinking`, `auto-research` | `huggingface`, `sequential-thinking`, `filesystem` |
| `code-reviewer-security` | Revisar el diff y el código afectado contra OWASP Top 10. | `ponytail-yagni`, `graphify-codebase`, `auto-research` | `github`, `filesystem` |
| `ui-ux-director` | Definir tokens de diseño (color, tipografía, espaciado, radios, movimiento) antes de maquetar. | `ui-ux-design-suite`, `playwright-testing`, `find-skills`, `ponytail-yagni` | `figma`, `playwright` |
| `software-architect` | Proponer la estructura mínima de módulos y sus responsabilidades. | `ponytail-yagni`, `graphify-codebase`, `sequential-thinking`, `arena-consensus`, `find-skills` | `sequential-thinking`, `filesystem`, `github` |
| `data-engineer` | Inspeccionar esquema, tipos y calidad de los datos antes de transformar. | `duckdb-analytics`, `ponytail-yagni`, `sequential-thinking` | `filesystem`, `sequential-thinking` |
| `knowledge-graph-agent` | Indexar documentos y notas en el grafo entidad-relación de LightRAG. | `lightrag-knowledge`, `graphify-codebase`, `headroom-context` | `claude-mem`, `filesystem` |
| `automation-browser` | Escribir y ejecutar pruebas E2E con Playwright (navegación, clics, formularios, capturas). | `playwright-testing`, `auto-research` | `playwright`, `n8n`, `filesystem` |
| `auto-researcher` | Localizar la documentación oficial y el repositorio de cada dependencia. | `auto-research`, `sequential-thinking`, `find-skills` | `github`, `huggingface`, `sequential-thinking` |
| `github-scout` | Consultar la API de GitHub con `scripts/github_api.py` (token en `GITHUB_TOKEN`). | `windows-notifier`, `auto-research` | `github` |
| `portfolio-git` | Revisar `git status` y `git diff --staged` antes de proponer un commit. | `git-portfolio-sync`, `ponytail-yagni` | `github` |

## Detalle por agente
### `orchestrator`
- **Propósito:** Enrutador maestro y triage del ecosistema. Clasifica cada petición, aplica YAGNI y Headroom, resuelve lo cotidiano con Ollama local y convoca /arena o al subagente especialista en lo complejo.
- **Modo:** `primary` · **Temperatura:** 0.2 · **Permisos:** edit `ask`, bash `ask`, webfetch `allow`
- **Skills obligatorias:** `find-skills`, `ponytail-yagni`, `headroom-context`, `arena-consensus`, `sequential-thinking`
- **MCP obligatorios:** `sequential-thinking`, `filesystem`
- **Comandos:** `/arena`, `/think`, `/headroom`, `/yagni`, `/sync-catalog`
- **Modo de uso:** Es el agente por defecto; cambia de agente primario con `Tab`.

### `arena-arbiter`
- **Propósito:** Juez de la Arena. Modera el debate entre soluciones candidatas, puntúa con la rúbrica (simplicidad, velocidad, seguridad, robustez) y emite el dictamen final o la síntesis óptima.
- **Modo:** `subagent` · **Temperatura:** 0.1 · **Permisos:** edit `deny`, bash `deny`, webfetch `deny`
- **Skills obligatorias:** `arena-consensus`, `sequential-thinking`, `ponytail-yagni`
- **MCP obligatorios:** `sequential-thinking`
- **Comandos:** `/arena`, `/think`, `/yagni`
- **Modo de uso:** Invócalo con `@arena-arbiter <petición>` o deja que el `orchestrator` lo delegue.

### `ml-deeplearning-specialist`
- **Propósito:** Ingeniero de redes neuronales y Deep Learning. PyTorch, Hugging Face MCP, optimización de VRAM/CUDA, embeddings locales y diseño de arquitecturas.
- **Modo:** `subagent` · **Temperatura:** 0.2 · **Permisos:** edit `allow`, bash `ask`, webfetch `allow`
- **Skills obligatorias:** `neural-network-ml`, `sequential-thinking`, `auto-research`
- **MCP obligatorios:** `huggingface`, `sequential-thinking`, `filesystem`
- **Comandos:** `/train-model`, `/think`, `/research`
- **Modo de uso:** Invócalo con `@ml-deeplearning-specialist <petición>` o deja que el `orchestrator` lo delegue.

### `code-reviewer-security`
- **Propósito:** Auditor de código y seguridad. Análisis estático, OWASP Top 10, detección de fugas de credenciales y auditoría de pruebas.
- **Modo:** `subagent` · **Temperatura:** 0.1 · **Permisos:** edit `deny`, bash `ask`, webfetch `allow`
- **Skills obligatorias:** `ponytail-yagni`, `graphify-codebase`, `auto-research`
- **MCP obligatorios:** `github`, `filesystem`
- **Comandos:** `/security-audit`, `/yagni`, `/graphify`, `/research`
- **Modo de uso:** Invócalo con `@code-reviewer-security <petición>` o deja que el `orchestrator` lo delegue.

### `ui-ux-director`
- **Propósito:** Director de diseño. Integra UI/UX Pro Max, Frontend Design, Awesome Design Patterns, Impeccable, Taste y Emil Kowalski para interfaces modernas con Tailwind CSS, micro-animaciones fluidas y Figma MCP.
- **Modo:** `subagent` · **Temperatura:** 0.4 · **Permisos:** edit `allow`, bash `ask`, webfetch `allow`
- **Skills obligatorias:** `ui-ux-design-suite`, `playwright-testing`, `find-skills`, `ponytail-yagni`
- **MCP obligatorios:** `figma`, `playwright`
- **Comandos:** `/craft`, `/critique`, `/taste`, `/animate`, `/browser-test`
- **Modo de uso:** Invócalo con `@ui-ux-director <petición>` o deja que el `orchestrator` lo delegue.

### `software-architect`
- **Propósito:** Arquitecto de software. Arquitectura limpia, principios SOLID y desarrollo minimalista guiado por la escalera YAGNI de Ponytail.
- **Modo:** `subagent` · **Temperatura:** 0.2 · **Permisos:** edit `allow`, bash `ask`, webfetch `allow`
- **Skills obligatorias:** `ponytail-yagni`, `graphify-codebase`, `sequential-thinking`, `arena-consensus`, `find-skills`
- **MCP obligatorios:** `sequential-thinking`, `filesystem`, `github`
- **Comandos:** `/yagni`, `/graphify`, `/arena`, `/think`
- **Modo de uso:** Invócalo con `@software-architect <petición>` o deja que el `orchestrator` lo delegue.

### `data-engineer`
- **Propósito:** Ingeniero de datos. Pipelines analíticos OLAP con DuckDB y Polars a hipervelocidad sobre CSV y Parquet locales.
- **Modo:** `subagent` · **Temperatura:** 0.1 · **Permisos:** edit `allow`, bash `ask`, webfetch `deny`
- **Skills obligatorias:** `duckdb-analytics`, `ponytail-yagni`, `sequential-thinking`
- **MCP obligatorios:** `filesystem`, `sequential-thinking`
- **Comandos:** `/analyze-data`, `/yagni`, `/think`
- **Modo de uso:** Invócalo con `@data-engineer <petición>` o deja que el `orchestrator` lo delegue.

### `knowledge-graph-agent`
- **Propósito:** Guardián de contexto. LightRAG, Claude-Mem y Graphify: mantiene el grafo de dependencias, la memoria persistente y el mapa visual de Obsidian.
- **Modo:** `subagent` · **Temperatura:** 0.1 · **Permisos:** edit `allow`, bash `ask`, webfetch `deny`
- **Skills obligatorias:** `lightrag-knowledge`, `graphify-codebase`, `headroom-context`
- **MCP obligatorios:** `claude-mem`, `filesystem`
- **Comandos:** `/graphify`, `/headroom`, `/sync-catalog`
- **Modo de uso:** Invócalo con `@knowledge-graph-agent <petición>` o deja que el `orchestrator` lo delegue.

### `automation-browser`
- **Propósito:** Automatización de navegador. Pruebas E2E con Playwright, scraping con Crawl4AI y flujos de trabajo en n8n.
- **Modo:** `subagent` · **Temperatura:** 0.2 · **Permisos:** edit `allow`, bash `ask`, webfetch `allow`
- **Skills obligatorias:** `playwright-testing`, `auto-research`
- **MCP obligatorios:** `playwright`, `n8n`, `filesystem`
- **Comandos:** `/browser-test`, `/research`
- **Modo de uso:** Invócalo con `@automation-browser <petición>` o deja que el `orchestrator` lo delegue.

### `auto-researcher`
- **Propósito:** Investigador autónomo. Valida documentación oficial, compatibilidad de librerías y solidez técnica antes de aprobar integraciones.
- **Modo:** `subagent` · **Temperatura:** 0.2 · **Permisos:** edit `deny`, bash `ask`, webfetch `allow`
- **Skills obligatorias:** `auto-research`, `sequential-thinking`, `find-skills`
- **MCP obligatorios:** `github`, `huggingface`, `sequential-thinking`
- **Comandos:** `/research`, `/think`
- **Modo de uso:** Invócalo con `@auto-researcher <petición>` o deja que el `orchestrator` lo delegue.

### `github-scout`
- **Propósito:** Centinela de tendencias en GitHub. Usa el PAT para detectar repositorios virales de IA y dispara notificaciones Toast de Windows.
- **Modo:** `subagent` · **Temperatura:** 0.3 · **Permisos:** edit `deny`, bash `ask`, webfetch `allow`
- **Skills obligatorias:** `windows-notifier`, `auto-research`
- **MCP obligatorios:** `github`
- **Comandos:** `/scout`, `/research`
- **Modo de uso:** Invócalo con `@github-scout <petición>` o deja que el `orchestrator` lo delegue.

### `portfolio-git`
- **Propósito:** Gestor de portafolio Git. Genera commits semánticos en español (feat, fix, docs, security, perf) y sincroniza el portafolio en GitHub.
- **Modo:** `subagent` · **Temperatura:** 0.1 · **Permisos:** edit `ask`, bash `ask`, webfetch `deny`
- **Skills obligatorias:** `git-portfolio-sync`, `ponytail-yagni`
- **MCP obligatorios:** `github`
- **Comandos:** `/commit`, `/security-audit`
- **Modo de uso:** Invócalo con `@portfolio-git <petición>` o deja que el `orchestrator` lo delegue.

## Cómo añadir un agente
1. Crea `.opencode/agents/<nombre>.md` con frontmatter (`description` obligatorio, `mode`, `model`, `permission`).
2. Incluye la sección `### MATRIZ DE HERRAMIENTAS Y SKILLS OBLIGATORIAS` con skills, MCP y comandos.
3. Ejecuta `/sync-catalog` para refrescar la tabla automática y actualiza el detalle de este archivo.

## Catálogo (generado)
<!-- CATALOGO:INICIO -->
| Agente | Modo | Modelo | Descripción |
|---|---|---|---|
| `arena-arbiter` | subagent | heredado | Juez de la Arena. Modera el debate entre soluciones candidatas, puntúa con la rúbrica (simplicidad, velocidad, seguridad, robustez) y emite el dictamen final o la síntesis óptima. |
| `auto-researcher` | subagent | heredado | Investigador autónomo y radar de modelos IA. Valida documentación oficial, vigila nuevos modelos de frontera, benchmarks, servidores MCP y habilidades comunitarias antes de aprobar integraciones. |
| `automation-browser` | subagent | heredado | Automatización de navegador. Pruebas E2E con Playwright, scraping con Crawl4AI y flujos de trabajo en n8n. |
| `code-reviewer-security` | subagent | heredado | Auditor de código y seguridad. Análisis estático, OWASP Top 10, detección de fugas de credenciales y auditoría de pruebas. |
| `data-engineer` | subagent | heredado | Ingeniero de datos. Pipelines analíticos OLAP con DuckDB y Polars a hipervelocidad sobre CSV y Parquet locales. |
| `github-scout` | subagent | heredado | Centinela de tendencias en GitHub. Detecta repositorios virales de IA, releases de nuevos modelos y benchmarks, y servidores MCP; dispara notificaciones Toast de Windows. |
| `knowledge-graph-agent` | subagent | heredado | Guardián de contexto. LightRAG, Claude-Mem y Graphify: mantiene el grafo de dependencias, la memoria persistente y el mapa visual de Obsidian. |
| `ml-deeplearning-specialist` | subagent | heredado | Ingeniero de redes neuronales y Deep Learning. PyTorch, Hugging Face MCP, optimización de VRAM/CUDA, embeddings locales y diseño de arquitecturas. |
| `orchestrator` | primary | heredado | Enrutador maestro y neuro-enrutador del ecosistema. Destila la intención pura, clasifica cada petición por tier abstracto de capacidad, aplica YAGNI y Headroom, y convoca /arena o al subagente especialista en lo complejo. |
| `portfolio-git` | subagent | heredado | Gestor de portafolio Git. Genera commits semánticos en español (feat, fix, docs, security, perf) y sincroniza el portafolio en GitHub. |
| `software-architect` | subagent | heredado | Arquitecto de software. Arquitectura limpia, principios SOLID y desarrollo minimalista guiado por la escalera YAGNI de Ponytail. |
| `ui-ux-director` | subagent | heredado | Director de diseño. Integra UI/UX Pro Max, Frontend Design, Awesome Design Patterns, Impeccable, Taste y Emil Kowalski para interfaces modernas con Tailwind CSS, micro-animaciones fluidas y Figma MCP. |
<!-- CATALOGO:FIN -->

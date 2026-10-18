---
description: "Catálogo de comandos slash (documento informativo, no es un comando)"
agent: orchestrator
---
# Comandos slash

Cada comando es un archivo `.md`: el nombre del archivo es el nombre del comando. El frontmatter admite `description`, `agent`, `subtask` y `model`; el cuerpo es el prompt. En el cuerpo, `$ARGUMENTS` recibe lo escrito tras el comando y `!`orden`` inserta la salida de un comando de shell.

## Tabla resumen
| Comando | Sintaxis | Agente que despierta | Skills que carga |
|---|---|---|---|
| `/arena` | `/arena <problema o decisión>` | `orchestrator` | `arena-consensus`, `sequential-thinking` |
| `/think` | `/think <problema>` | `orchestrator` | `sequential-thinking` |
| `/train-model` | `/train-model <tarea> [dataset]` | `ml-deeplearning-specialist` | `neural-network-ml`, `sequential-thinking` |
| `/craft` | `/craft <qué diseñar>` | `ui-ux-director` | `ui-ux-design-suite`, `playwright-testing`, `find-skills` |
| `/critique` | `/critique <archivo o URL>` | `ui-ux-director` | `ui-ux-design-suite`, `playwright-testing` |
| `/taste` | `/taste <archivo o componente>` | `ui-ux-director` | `ui-ux-design-suite` |
| `/animate` | `/animate <componente> [efecto]` | `ui-ux-director` | `ui-ux-design-suite` |
| `/browser-test` | `/browser-test <url> [escenario]` | `automation-browser` | `playwright-testing` |
| `/research` | `/research <pregunta o dependencia>` | `auto-researcher` | `auto-research`, `sequential-thinking` |
| `/yagni` | `/yagni [archivos o diff]` | `software-architect` | `ponytail-yagni` |
| `/headroom` | `/headroom [foco]` | `knowledge-graph-agent` | `headroom-context` |
| `/graphify` | `/graphify [ruta]` | `knowledge-graph-agent` | `graphify-codebase`, `lightrag-knowledge` |
| `/security-audit` | `/security-audit [alcance]` | `code-reviewer-security` | `ponytail-yagni`, `auto-research` |
| `/analyze-data` | `/analyze-data <archivo> <pregunta>` | `data-engineer` | `duckdb-analytics` |
| `/scout` | `/scout [tema] [días]` | `github-scout` | `windows-notifier`, `auto-research` |
| `/commit` | `/commit [mensaje o tipo]` | `portfolio-git` | `git-portfolio-sync`, `ponytail-yagni` |
| `/sync-catalog` | `/sync-catalog` | `orchestrator` | `find-skills` |

## Modo de uso
En OpenCode escribe `/` seguido del nombre. Ejemplos:
```
/arena ¿SQLite o DuckDB para análisis local?
/craft panel de métricas con modo oscuro
/commit feat
```

## Cómo añadir un comando
1. Ejecuta `find-skills` por si ya existe.
2. Crea `.opencode/commands/<nombre>.md` con `description` y `agent`.
3. Escribe el prompt con pasos numerados y `$ARGUMENTS`.
4. Ejecuta `/sync-catalog`.

## Catálogo (generado)
<!-- CATALOGO:INICIO -->
| Comando | Agente | Descripción |
|---|---|---|
| `/analyze-data` | `data-engineer` | Lanza análisis SQL local con DuckDB y Polars. |
| `/animate` | `ui-ux-director` | Inyecta micro-animaciones con curvas de resorte estilo Emil Kowalski. |
| `/arena` | `orchestrator` | Somete un problema a debate entre subagentes; arena-arbiter determina la mejor solución o una síntesis. |
| `/browser-test` | `automation-browser` | Lanza Playwright para validar la aplicación en un navegador real. |
| `/commit` | `portfolio-git` | Redacta un commit semántico en español y actualiza el portafolio en GitHub. |
| `/craft` | `ui-ux-director` | Orquesta el flujo completo de diseño visual: UI/UX Pro Max, Tailwind y animación. |
| `/critique` | `ui-ux-director` | Audita la interfaz aplicando las heurísticas de Taste e Impeccable. |
| `/evolve` | `auto-researcher` | Barrido de evolución del ecosistema: busca oro comunitario en find-skills, lo evalúa e integra con atribución. |
| `/graphify` | `knowledge-graph-agent` | Genera o actualiza el grafo de dependencias del repositorio. |
| `/headroom` | `knowledge-graph-agent` | Inspecciona el uso de tokens y comprime el contexto activo. |
| `/research` | `auto-researcher` | Ejecuta investigación técnica autónoma para contrastar una solución con fuentes oficiales. |
| `/scout` | `github-scout` | Busca repositorios virales de IA en GitHub y emite una notificación Toast. |
| `/security-audit` | `code-reviewer-security` | Ejecuta una auditoría estricta de seguridad y parámetros antes de confirmar cambios. |
| `/sync-catalog` | `orchestrator` | Re-escanea las carpetas y actualiza los README.md e índices automáticamente. |
| `/taste` | `ui-ux-director` | Refina estética, espaciado y contraste visual. |
| `/think` | `orchestrator` | Activa el pensamiento secuencial estructurado para problemas complejos. |
| `/train-model` | `ml-deeplearning-specialist` | Genera y lanza plantillas de redes neuronales optimizadas en PyTorch para la GPU local. |
| `/yagni` | `software-architect` | Audita el código recién escrito para recortar líneas superfluas con Ponytail. |
<!-- CATALOGO:FIN -->

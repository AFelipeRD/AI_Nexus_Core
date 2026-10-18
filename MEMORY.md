# MEMORY.md — Memoria a largo plazo

> Bóveda compatible con Obsidian: abre `D:\AI_Nexus_Core` como vault. Los wikilinks `[[...]]` forman el grafo. Mantén esta nota breve (< 150 líneas) para no gastar contexto: el detalle va en `memoria/` y `docs/`.
> Nota: Obsidian oculta las carpetas que empiezan por punto (`.opencode`); por eso la memoria viva está en la raíz, `memoria/` y `docs/`.

## Perfil y preferencias
- Usuario: ver [[Usuario]]. Idioma: español. Plataforma: Windows 11 + Warp.
- Preferencia: soluciones mínimas (YAGNI), verificadas y sin dependencias superfluas.

## Entorno
- Modelo local: [[Ollama]] (`qwen2.5-coder:7b`).
- Entorno de terminal y rutas: [[Windows-Warp]].

## Decisiones (formato: fecha · decisión · motivo · fuente)
- 2026-10-16 · Adoptar ecosistema 100 % Markdown nativo de OpenCode · simplicidad y portabilidad · [[01_MANUAL_ECOSISTEMA_OPENCODE]]
- 2026-10-16 · Decisiones críticas pasan por [[Arena-Consensus]] · reducir errores de un modelo pequeño · [[06_PROTOCOLO_ARENA_Y_CONSENSO]]

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

## Cómo actualizar esta memoria
1. Añade decisiones con fecha y enlace a la fuente.
2. Crea una nota en `memoria/<Entidad>.md` solo si la entidad se usará más de una vez.
3. Enlaza siempre con `[[Nombre]]`; evita duplicar contenido, enlaza.
4. Pide al `knowledge-graph-agent` que sincronice el grafo (`/graphify`).

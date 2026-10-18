# 05 · Grafo LightRAG y bóveda de Obsidian

Enlaces: [[MEMORY]] · [[04_INGENIERIA_DATOS_Y_GRAPHIFY]] · [[Ollama]]

## Capas de memoria
| Capa | Herramienta | Contenido |
|---|---|---|
| Corto plazo | Conversación + Headroom | Tarea en curso |
| Persistente | MCP `claude-mem` (o `mem0`) | Hechos y preferencias entre sesiones |
| Notas | `MEMORY.md` y `memoria/` | Decisiones y entidades con `[[wikilinks]]` |
| Grafo | LightRAG (`.lightrag/`) | Entidades, relaciones y vectores |
| Código | Graphify (`.graphify/`) | Dependencias y estructura |

## Obsidian
1. En Obsidian elige *Abrir carpeta como bóveda* → `D:\AI_Nexus_Core`.
2. Abre la vista de grafo: `MEMORY`, `memoria/` y `docs/` aparecen conectados.
3. Obsidian **no indexa carpetas que empiezan con punto** (`.opencode`, `.lightrag`): por eso la memoria viva está fuera de ellas.
4. `.obsidian/app.json` ya excluye `data/`, `output/`, `logs/` y `.venv/`.

## LightRAG
- Instalación: `pip install lightrag-hku`; embeddings: `ollama pull nomic-embed-text`.
- Modos de consulta: `local` (entidades), `global` (temas), `hybrid` (recomendado).
- La API cambia entre versiones: consulta su README antes de usar el ejemplo de `skills/lightrag-knowledge/SKILL.md`.

## Convenciones de notas
- Una nota por entidad: `memoria/<Entidad>.md`, con relaciones `[[Otra]]` y fecha de la fuente.
- Enlaza, no copies. Sin secretos.
- Mantén `MEMORY.md` bajo ~150 líneas.

---
name: lightrag-knowledge
description: "Indexación en grafo de conocimiento de doble nivel (entidad-relación + vectores) con LightRAG y persistencia estilo Obsidian con wikilinks. Úsala para recordar proyectos, documentos y decisiones sin perder contexto."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Lightrag Knowledge

## Cuándo usar esta skill
- Indexar documentación o notas nuevas.
- Responder preguntas sobre el proyecto con contexto amplio.
- Sincronizar entidades con `memoria/`.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `fuente` | carpeta o archivos a indexar |
| `consulta` | pregunta al grafo |
| `modo` | naive, local, global o hybrid (por defecto hybrid) |

## Procedimiento
1. **Requisitos**: `pip install lightrag-hku`; en Ollama ejecuta `ollama pull nomic-embed-text` (embeddings, 768 dimensiones). La API cambia entre versiones: revisa `pip show lightrag-hku` y su README.
2. **Directorio de trabajo**: `.lightrag/` (ignorado por Git).
3. **Insertar** textos con `rag.insert(...)`; indexa Markdown de `docs/`, `memoria/` y `MEMORY.md`.
4. **Consultar** con `QueryParam(mode="hybrid")`: *local* para entidades concretas, *global* para temas amplios.
5. **Espejo en Obsidian**: por cada entidad relevante crea o actualiza `memoria/<Entidad>.md` con relaciones como `[[OtraEntidad]]` y fecha de la fuente. Sintaxis validada por el CEO de Obsidian: `[[wikilinks]]` para notas internas (Obsidian rastrea renombres automáticamente) y `[texto](url)` solo para URLs externas; callouts `> [!tipo]` para destacados; IDs de bloque `^id` para referencias puntuales; frontmatter con propiedades (title, tags, aliases).
6. **Higiene**: sin secretos en lo indexado; reindexa solo archivos cambiados.

## Ejemplo
```python
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

HOST = "http://127.0.0.1:11434"

async def main():
    rag = LightRAG(
        working_dir=".lightrag",
        llm_model_func=ollama_model_complete,
        llm_model_name="qwen2.5-coder:7b",
        llm_model_kwargs={"host": HOST, "options": {"num_ctx": 8192}},
        embedding_func=EmbeddingFunc(
            embedding_dim=768, max_token_size=8192,
            func=lambda textos: ollama_embed(textos, embed_model="nomic-embed-text", host=HOST)),
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()
    await rag.ainsert(open("MEMORY.md", encoding="utf-8").read())
    print(await rag.aquery("¿Qué decisiones se tomaron?", param=QueryParam(mode="hybrid")))

asyncio.run(main())
```

## Errores a evitar
- Indexar secretos o `.env`.
- Usar un modelo de embeddings distinto al del índice existente.
- Duplicar contenido en lugar de enlazar con wikilinks.

## Referencias comunitarias validadas (find-skills)
- `kepano/obsidian-skills` — **Steph Ango (CEO de Obsidian) oficial**: `obsidian-markdown` (90 K), `obsidian-cli`, `obsidian-bases`, `json-canvas` — sintaxis autoritativa de wikilinks, embeds, callouts y propiedades.
- `mattpocock/skills@obsidian-vault` — 195 K instalaciones: gestión de bóvedas Obsidian.
- `graphify-labs/graphify@graphify` — **Graphify oficial** (la herramienta estructural que ya usa este ecosistema).
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

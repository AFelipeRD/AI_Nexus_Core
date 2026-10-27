---
name: lightrag-knowledge
description: "Indexación en grafo de conocimiento de doble nivel (entidad-relación + vectores) con LightRAG y persistencia estilo Obsidian con wikilinks. Ingestión no destructiva: data/raw/ y data/inbox/ en solo lectura estricta; índices y salidas solo en data/processed/ u output/. Úsala para recordar proyectos, documentos y decisiones sin perder contexto."
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

## Ingestión no destructiva (privacidad local)
- **Solo lectura estricta**: todo archivo del usuario en `data/raw/` o `data/inbox/` (PDFs, CSVs, Parquet, código, notas) es inmutable; nunca se modifica, renombra ni elimina.
- **Salidas segregadas**: índices vectoriales, optimizaciones y archivos transformados se escriben exclusivamente en `data/processed/` o `output/`, garantizando la integridad de los originales.
- **Base vectorial embebida local**: búsqueda semántica e indexación en disco D: con DuckDB (VSS) u otro almacenamiento vectorial local; cero salida a servicios externos.

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
- Escribir, renombrar o eliminar archivos de `data/raw/` o `data/inbox/`: los originales son inmutables.

## Referencias comunitarias validadas (find-skills)
- `kepano/obsidian-skills` — **Steph Ango (CEO de Obsidian) oficial**: `obsidian-markdown` (90 K), `obsidian-cli`, `obsidian-bases`, `json-canvas` — sintaxis autoritativa de wikilinks, embeds, callouts y propiedades.
- `mattpocock/skills@obsidian-vault` — 195 K instalaciones: gestión de bóvedas Obsidian.
- `graphify-labs/graphify@graphify` — **Graphify oficial** (la herramienta estructural que ya usa este ecosistema).
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

## Referencias comunitarias validadas (find-skills 2026-10-27)
- **Transclusión con embeds** `![[Nota#Sección]]`: compón notas de índice y de entidad reutilizando secciones de otras notas sin duplicar bytes — materializa el «enlaza, no dupliques» de `MEMORY.md` con un mecanismo real: la bóveda renderiza el contenido enlazado en el punto del embed.
- **Enlaces con nombre de sección** `[[Nota#Sección]]`: cita el apartado exacto, no la nota entera, al referenciar una decisión concreta; la regla de elección del paso 5 se mantiene (wikilinks solo para notas internas — Obsidian re-rastrea renombres —, `[texto](url)` solo para URLs externas).
- **Block IDs** `^id` (al final del párrafo, o en línea propia tras listas y citas): ancla estable para citar una decisión exacta de `MEMORY.md` desde `memoria/*.md` (`[[MEMORY#^id]]`) aunque los headings cambien — más fino que `[[Nota#Heading]]`, que se rompe al renombrar un título.
- **Callouts tipados y plegables** `> [!info]`, `> [!warning]`, `> [!danger]` (con `-`/`+` tras el tipo se pliegan por defecto): semántica visual dentro de las notas de la bóveda, en lugar de blockquotes planos sin tipo.

_Atribución: kepano/obsidian-skills@obsidian-markdown (oficial de Obsidian)._

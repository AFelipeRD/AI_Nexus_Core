---
name: ai-multimodal-ops
description: "Heurísticas de encadenamiento multimodal (texto, imagen, audio), prompts basados en esquemas JSON y benchmarks de calidad para sistemas generativos reproducibles. Úsala al diseñar pipelines de IA generativa o RAG."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Ai Multimodal Ops

## Cuándo usar esta skill
- Diseñar un pipeline de IA generativa o un flujo agéntico.
- Construir RAG multimodal (texto + imagen + audio).
- Estructurar prompts con salidas JSON fiables.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `tarea` | qué debe resolver el pipeline |
| `modalidades` | texto, imagen, audio o combinación |
| `criterio` | métrica y umbral de aceptación |

## Procedimiento
1. **Criterio de éxito primero**: métrica, umbral y conjunto de evaluación (aunque sean 10 casos) antes de elegir modelo.
2. **Cadena mínima**: ingesta → extracción/normalización → modelo → validación de esquema → salida; cada eslabón es reemplazable.
3. **Prompts estructurales**: system prompt con rol y restricciones; salida exigida como JSON validada contra esquema (pydantic/zod); temperatura baja para tareas deterministas.
4. **RAG multimodal** (pipeline LangChain): Index (cargar → dividir → embeber → almacenar) → Retrieve → Generate. División con `RecursiveCharacterTextSplitter` (chunk ~500, solapamiento ~50); embeddings por modalidad; recuperación con citación de fuente; sin cita, no hay respuesta. Vector store proporcional: InMemory para pruebas, FAISS local de alto rendimiento, Chroma para desarrollo, Pinecone para producción gestionada.
5. **Patrones de prompt** (validados en comunidad): few-shot con selección por similitud semántica; cadena de pensamiento con auto-consistencia (múltiples rutas de razonamiento votadas); salida JSON validada contra esquema pydantic/zod con manejo de errores de formato; A/B de variantes midiendo exactitud, consistencia y latencia.
6. **Seleccionar modelo**: Hub de Hugging Face (MCP) contrastando capacidades, licencia y coste; preentrenado antes que fine-tuning.
7. **Evaluar y trazar**: ejecuta el conjunto de evaluación, registra métricas, coste y latencia; itera sobre los peores casos.

## Ejemplo
```json
{
  "rol": "extractor de facturas",
  "salida": {
    "schema": {
      "proveedor": "string",
      "total_centavos": "integer",
      "lineas": [{ "concepto": "string", "monto_centavos": "integer" }]
    },
    "reglas": ["sin campos inventados", "monto nulo si ilegible"]
  }
}
```

## Errores a evitar
- Prompt libre sin esquema de salida.
- Elegir modelo sin conjunto de evaluación.
- Cadenas monolíticas imposibles de reemplazar por eslabones.
- Responder sin citar la fuente recuperada.

## Referencias comunitarias validadas (find-skills)
- `langchain-ai/langchain-skills@langchain-rag` — **LangChain oficial**: pipeline completo de RAG (loaders, splitters, embeddings, vector stores) con tabla de selección FAISS/Chroma/Pinecone.
- `wshobson/agents@prompt-engineering-patterns` — patrones de producción: few-shot dinámico, CoT con auto-consistencia, JSON mode, optimización iterativa.
- `anthropics/skills@claude-api` — Anthropic oficial: uso correcto de la API para salidas estructuradas.
- `huggingface/skills@transformers-js` y `@train-sentence-transformers` — Hugging Face oficial: embeddings en JS y entrenamiento de sentence-transformers.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

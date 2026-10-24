---
name: ai-multimodal-ops
description: "Heurísticas de encadenamiento multimodal (texto, imagen, audio), prompts basados en esquemas JSON, benchmarks de calidad para sistemas generativos reproducibles y orquestación de medios con doble motor (Tier 0 gratuito NVIDIA NIM por defecto + premium MCP muapi). Úsala al diseñar pipelines de IA generativa o RAG."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.3"
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

## Orquestación de medios generativos (doble motor)

Patrón del ecosistema para pipelines texto → imagen/video/audio, en **dos niveles**:

**Flujo por defecto — Tier 0 gratuito (costo $0, NVIDIA NIM):**
1. **Keyframe**: `python scripts\nvidia_flux.py "<prompt_en_ingles>" "<archivo.png>" [--modelo <nombre>]` — imagen multi-modelo (`--modelo`; default `flux_3_image_klein`; catálogo: `scripts/media_catalogo.py`) 1024×1024 → `output/images/`.
2. **Animación**: `python scripts\nvidia_cosmos.py "<prompt_en_ingles>" "<archivo.mp4>" [--modelo <nombre>]` — video de catálogo NIM (`--modelo`; sujeto a las funciones entitled del momento — hoy 0; rutas de desbloqueo en el propio script) o premium muapi → `output/videos/`.
3. **Descarga y verificación**: cada eslabón valida su entrada antes de pasarla al siguiente; verifica existencia y peso del artefacto antes de entregar.

**Flujo premium — MCP `muapi`** (kling/veo/lipsync/upscale; variaciones creativas avanzadas):
1. **Chequeo previo obligatorio**: `muapi_account_balance` antes de jobs costosos (el video es el medio más caro: $0.30-$2.5 por clip).
2. **Prompt cinematográfico**: el modelo activo (GLM) construye el prompt en inglés con gramática visual (sujeto → acción → luz → encuadre → estilo → parámetros técnicos).
3. **Submit + poll**: `muapi_image_generate` / `muapi_video_generate` / `muapi_audio_create` devuelven un `request_id`; sondea con `muapi_predict_result` hasta el estado final.
4. **Descarga y verificación**: artefacto a `output/images/`, `output/videos/` o `output/`; verifica existencia y peso antes de entregar.
5. **Cadena multimodal premium**: imagen → `muapi_video_from_image` (i2v) → `muapi_edit_lipsync`; cada eslabón valida su entrada antes de pasarla al siguiente.

**Pipeline unificado de diseño (Cuadrilla de Diseño)**: para piezas con motion, extiende el flujo gratuito heredando los tokens del canon (`.opencode/context/tokens-diseno.md`): keyframe multi-modelo NIM ($0) → composición Remotion (`D:\Nexus_Remotion`, motion local en CPU) → opción premium muapi para variaciones creativas avanzadas.

**Regla de enrutado**: el motor gratuito es el por defecto; muapi premium solo cuando el usuario lo pida o la tarea requiera capacidades exclusivas (lipsync, upscale, face swap, modelos de frontera) — siempre con chequeo de saldo previo.

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

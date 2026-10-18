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
4. **RAG multimodal**: chunking con solapamiento, embeddings por modalidad, recuperación con citación de fuente; sin cita, no hay respuesta.
5. **Seleccionar modelo**: Hub de Hugging Face (MCP) contrastando capacidades, licencia y coste; preentrenado antes que fine-tuning.
6. **Evaluar y trazar**: ejecuta el conjunto de evaluación, registra métricas, coste y latencia; itera sobre los peores casos.

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

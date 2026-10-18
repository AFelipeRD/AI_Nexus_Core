---
name: neural-network-ml
description: "Diseño y entrenamiento eficiente de redes neuronales con PyTorch en GPU local: precisión mixta fp16/bf16, control de VRAM en CUDA, cuantización y consumo del MCP de Hugging Face. Úsala al diseñar, entrenar o depurar modelos."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Neural Network Ml

## Cuándo usar esta skill
- Al diseñar o elegir una arquitectura neuronal.
- Al entrenar, afinar (fine-tuning) o depurar un modelo.
- Al quedarse sin VRAM o al acelerar un entrenamiento lento.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `tarea` | clasificación, regresión, secuencia, visión o fine-tuning |
| `dataset` | ruta local o id del Hub de Hugging Face |
| `vram_gb` | VRAM disponible (si se omite, detectarla con torch.cuda) |
| `objetivo` | métrica y valor que se desea alcanzar |

## Procedimiento
1. **Detectar hardware**: `torch.cuda.is_available()` y `torch.cuda.get_device_properties(0).total_memory`.
2. **Buscar antes de construir**: con el MCP `huggingface` busca arquitectura, modelo preentrenado y dataset. Prefiere fine-tuning a entrenar desde cero.
3. **Línea base mínima**: modelo pequeño y prueba de sobreajuste de un solo batch para validar la tubería.
4. **Precisión mixta**: `torch.autocast` con fp16 y `GradScaler`; usa bf16 (sin scaler) en GPU Ampere o superior.
5. **Control de VRAM**: batch dinámico, acumulación de gradientes, gradient checkpointing, `pin_memory=True`; `torch.cuda.empty_cache()` solo entre fases.
6. **Cuantización**: `torch.ao.quantization.quantize_dynamic` para inferencia en CPU; para LLM usa modelos cuantizados GGUF vía Ollama.
7. **Reproducibilidad**: semilla fija, división train/val/test, checkpoints en `output/`.
8. **Windows**: protege el punto de entrada con `if __name__ == "__main__":` si usas `num_workers > 0`.
9. **Reportar**: curva de pérdida, métrica en validación y consumo máximo de VRAM (`torch.cuda.max_memory_allocated()`).

## Ejemplo
```python
import torch

dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
modelo = modelo.to(dispositivo)
optimizador = torch.optim.AdamW(modelo.parameters(), lr=3e-4)
escalador = torch.cuda.amp.GradScaler(enabled=(dispositivo == "cuda"))

for x, y in cargador:
    x, y = x.to(dispositivo, non_blocking=True), y.to(dispositivo, non_blocking=True)
    optimizador.zero_grad(set_to_none=True)
    with torch.autocast(device_type=dispositivo, dtype=torch.float16, enabled=(dispositivo == "cuda")):
        perdida = criterio(modelo(x), y)
    escalador.scale(perdida).backward()
    escalador.step(optimizador)
    escalador.update()
```

## Errores a evitar
- Llamar a `.item()` en cada iteración (fuerza sincronización con la GPU).
- Evaluar sin `model.eval()` y `torch.no_grad()`.
- Entrenar desde cero cuando existe un modelo preentrenado adecuado.
- Dar una métrica sin conjunto de validación separado.

---
name: neural-network-ml
description: "Diseño y entrenamiento eficiente de redes neuronales con PyTorch en GPU local: selector probabilístico de algoritmos (LightGBM/XGBoost/PyTorch), precisión mixta fp16/bf16, control de VRAM en CUDA, cuantización y consumo del MCP de Hugging Face. Úsala al elegir algoritmo, entrenar o depurar modelos."
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
- Al elegir entre LightGBM, XGBoost y redes neuronales PyTorch con el selector probabilístico.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `tarea` | clasificación, regresión, secuencia, visión o fine-tuning |
| `dataset` | ruta local o id del Hub de Hugging Face |
| `vram_gb` | VRAM disponible (si se omite, detectarla con torch.cuda) |
| `objetivo` | métrica y valor que se desea alcanzar |

## Selector probabilístico de algoritmos (Laya)
- Analiza el dataset en `data/processed/` (dimensionalidad, volumen, tipo de objetivo) y estima la probabilidad de éxito y rendimiento entre **LightGBM**, **XGBoost** y redes neuronales **PyTorch**; entrena el argmax.
- Heurística: datos tabulares de volumen medio → gradient boosting (más rápido y menor VRAM); alta dimensionalidad no estructurada (texto, imagen) o gran volumen → PyTorch en GPU (CUDA fp16).

## Procedimiento
1. **Detectar hardware**: `torch.cuda.is_available()` y `torch.cuda.get_device_properties(0).total_memory`.
2. **Buscar antes de construir**: con el MCP `huggingface` busca arquitectura, modelo preentrenado y dataset. Prefiere fine-tuning a entrenar desde cero.
3. **Línea base mínima**: modelo pequeño y prueba de sobreajuste de un solo batch para validar la tubería.
4. **Precisión mixta (obligatoria en CUDA)**: delegación forzada `device=cuda` cuando esté disponible; `torch.autocast` con fp16 y `GradScaler`; usa bf16 (sin scaler) en GPU Ampere o superior.
5. **Control de VRAM**: batch dinámico, acumulación de gradientes, gradient checkpointing, `pin_memory=True`; `torch.cuda.empty_cache()` tras cada fase para operar fluidamente en 4 GB.
6. **Cuantización**: `torch.ao.quantization.quantize_dynamic` para inferencia en CPU; para LLM usa modelos cuantizados GGUF vía Ollama.
7. **Reproducibilidad** (patrón comunitario): semilla completa — `torch.manual_seed(seed)` + `torch.cuda.manual_seed_all(seed)` — división train/val/test, checkpoints y métricas en `output/modelos/`; código agnóstico de dispositivo (`torch.device("cuda" if torch.cuda.is_available() else "cpu")`), nunca `.cuda()` incrustado.
8. **Windows**: protege el punto de entrada con `if __name__ == "__main__":` si usas `num_workers > 0`.
9. **Reportar métricas formales**: curva de pérdida por época, métrica en validación, semilla fija, división train/val/test y consumo máximo de VRAM (`torch.cuda.max_memory_allocated()`).

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

## Referencias comunitarias validadas (find-skills)
- `pytorch/pytorch` — **PyTorch oficial**: convenciones de contribución, docstrings y revisión de PRs del propio framework.
- `affaan-m/ecc@pytorch-patterns` — patrones de entrenamiento reproducible, código agnóstico de dispositivo y gestión de VRAM.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

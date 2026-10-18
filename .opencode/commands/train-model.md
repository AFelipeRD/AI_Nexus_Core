---
description: "Genera y lanza plantillas de redes neuronales optimizadas en PyTorch para la GPU local."
agent: ml-deeplearning-specialist
---
Sigue la skill `neural-network-ml` para esta tarea de entrenamiento:

$ARGUMENTS

1. Detecta el hardware con `torch.cuda` e informa la VRAM disponible.
2. Con el MCP `huggingface` busca un modelo preentrenado y un dataset adecuados.
3. Genera `output/entrenamiento/entrenar.py` con precisión mixta, control de VRAM, semilla fija y división train/val/test.
4. Prueba primero el sobreajuste de un batch; luego pide confirmación antes de lanzar el entrenamiento completo.
5. Reporta métricas, consumo máximo de VRAM y ruta de los checkpoints.

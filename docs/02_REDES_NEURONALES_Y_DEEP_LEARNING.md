# 02 · Redes neuronales y Deep Learning

Enlaces: [[01_MANUAL_ECOSISTEMA_OPENCODE]] · [[04_INGENIERIA_DATOS_Y_GRAPHIFY]]

## Agente y herramientas
- Agente: `ml-deeplearning-specialist`. Skill: `neural-network-ml`. Comando: `/train-model`.
- MCP `huggingface` (remoto, requiere `HF_TOKEN`): busca modelos, datasets y papers del Hub.
- MCP `sequential-thinking` y comando `/think`: descomponer matemáticas y algoritmos.

## Flujo recomendado
1. **Hardware**: `python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"`.
2. **Buscar**: con el MCP de Hugging Face localiza un modelo preentrenado; el fine-tuning casi siempre supera al entrenamiento desde cero con pocos datos.
3. **Línea base**: modelo mínimo, sobreajuste de un batch.
4. **Entrenar** con precisión mixta (fp16 o bf16) y `GradScaler` si usas fp16.
5. **Evaluar** en validación y prueba separadas; guarda resultados en `output/`.

## Control de VRAM
| Técnica | Ahorro | Coste |
|---|---|---|
| Precisión mixta | ~40–50 % de activaciones | Mínimo |
| Acumulación de gradientes | Permite batch efectivo mayor | Más tiempo por época |
| Gradient checkpointing | Gran ahorro de activaciones | ~20–30 % más lento |
| Cuantización (inferencia) | Menor tamaño de modelo | Posible pérdida de precisión |

## Instalación en Windows
Instala PyTorch con el índice CUDA oficial antes del resto de dependencias (ver cabecera de `requirements.txt`). Con `num_workers > 0`, protege el punto de entrada con `if __name__ == "__main__":`.

## Razonamiento secuencial
Para derivaciones (formas de tensores, funciones de pérdida, complejidad) usa `/think`: numera pensamientos, formula hipótesis, verifica con un caso pequeño.

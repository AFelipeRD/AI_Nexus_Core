---
name: video-processing-suite
description: "Captura automatizada de video a 60 FPS con Playwright, generación de video con NVIDIA Cosmos vía scripts/nvidia_cosmos.py, composición con MoviePy/FFmpeg, manejo de streams y transcodificación ligera sin pérdida perceptual. Úsala al generar clips programáticos."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.1"
---

# Video Processing Suite

## Cuándo usar esta skill
- Grabar la pantalla o una escena web como video.
- Generar un clip o simulación física desde cero (Cosmos en NVIDIA Build).
- Componer, cortar o sincronizar clips.
- Exportar WebM/MP4 optimizados.

## Herramienta oficial de generación (Cosmos en NVIDIA Build)
Cuando el clip nace generado (simulación física) y no capturado del navegador, invoca en terminal (`bash`) desde la raíz, con parámetros en inglés:

```bash
python scripts/nvidia_cosmos.py "<PROMPT_EN_INGLES>" "<NOMBRE_ARCHIVO.mp4>"
```

| Parámetro | Descripción |
|---|---|
| `PROMPT_EN_INGLES` | descripción de la simulación física o escena en inglés |
| `NOMBRE_ARCHIVO.mp4` | archivo de salida (por defecto `cosmos_sim.mp4`) |

- Requiere la clave en `.secrets/nvidia.key`; el destino es `output/videos/<NOMBRE_ARCHIVO.mp4>`.
- Si la API devuelve solo metadatos sin artefacto descargable, el script avisa con `[AVISO]`: inspecciona la respuesta antes de prometer un archivo al usuario.
- No mezcles este origen con la captura Playwright en un mismo re-encode (regla del único re-encode).

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `fuente` | URL/escena a capturar o clips a componer |
| `duracion` | segundos objetivo |
| `salida` | formato (webm/mp4), resolución y FPS |

## Procedimiento
1. **Captura con Playwright**: `record_video_dir` + `record_video_size` al viewport exacto; espera por condición (nunca `sleep` fijo); cierra el contexto para volcar el archivo.
2. **Verificar la captura**: duración, resolución y FPS reales con `ffprobe` antes de editar.
3. **Componer por capas** (heurística comunitaria): cada capa tiene un solo trabajo — captura → FFmpeg → composición/timeline → voz/música → pulido final; no saltes capas ni pidas a una herramienta el trabajo de otra. El valor está en comprimir y estructurar material real, no en generar desde cero.
4. **Sincronización audiovisual**: ancla el audio al primer frame; una desincronización perceptible (> 40 ms) se corrige, no se entrega.
5. **Checkpoints versionados**: guarda y verifica un checkpoint del proyecto antes y después de cada cambio estructural; una lectura de API demuestra el estado en memoria, no que se guardó en disco.
6. **Exportar ligero**: un solo re-encode; CRF 18-23 (H.264/VP9) según destino; `+faststart` para web en MP4.
7. **Verificación final nativa**: `ffprobe` del archivo entregado (duración, FPS, peso) + reproducción de control — parsear un XML o un contenedor no demuestra que la salida es audible y visible; revísala como la vería el usuario.

## Ejemplo
```python
ctx = nav.new_context(viewport={"width": 1280, "height": 720},
                      record_video_dir="assets/video",
                      record_video_size={"width": 1280, "height": 720})
```

## Errores a evitar
- Esperas fijas durante la captura.
- Re-encodar en cada paso (degradación acumulada).
- Recortar sin respetar keyframes al copiar directo.
- Entregar sin verificar FPS y duración reales.

## Referencias comunitarias validadas (find-skills)
- `affaan-m/ecc@video-editing` — pipeline por capas (captura → FFmpeg → Remotion → voz → pulido) con checkpoints versionados y validación nativa de exportes.
- `currents-dev/playwright-best-practices-skill@playwright-best-practices` — Currents (95 K instalaciones): monitoreo de errores de consola, regresión visual y canvas/WebGL en pruebas de navegador.
- `microsoft/playwright-cli@playwright-cli` — Microsoft oficial: CLI de Playwright para flujos de captura.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

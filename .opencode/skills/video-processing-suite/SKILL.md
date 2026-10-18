---
name: video-processing-suite
description: "Captura automatizada de video a 60 FPS con Playwright, composición con MoviePy/FFmpeg, manejo de streams y transcodificación ligera sin pérdida perceptual. Úsala al generar clips programáticos."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Video Processing Suite

## Cuándo usar esta skill
- Grabar la pantalla o una escena web como video.
- Componer, cortar o sincronizar clips.
- Exportar WebM/MP4 optimizados.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `fuente` | URL/escena a capturar o clips a componer |
| `duracion` | segundos objetivo |
| `salida` | formato (webm/mp4), resolución y FPS |

## Procedimiento
1. **Captura con Playwright**: `record_video_dir` + `record_video_size` al viewport exacto; espera por condición (nunca `sleep` fijo); cierra el contexto para volcar el archivo.
2. **Verificar la captura**: duración, resolución y FPS reales con `ffprobe` antes de editar.
3. **Componer**: MoviePy para timelines legibles (cortes, overlays, texto); FFmpeg directo para operaciones simples y rápidas.
4. **Sincronización audiovisual**: ancla el audio al primer frame; una desincronización perceptible (> 40 ms) se corrige, no se entrega.
5. **Exportar ligero**: un solo re-encode; CRF 18-23 (H.264/VP9) según destino; `+faststart` para web en MP4.
6. **Verificación final**: `ffprobe` del archivo entregado (duración, FPS, peso) + reproducción de control.

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

---
name: video-processing-suite
description: "Captura automatizada de video a 60 FPS con Playwright, doble motor de generación (Tier 0 gratuito: catálogo vivo NVIDIA NIM con rotación `--modelo` vía scripts/nvidia_cosmos.py por defecto + premium MCP muapi: veo3, kling, wan, seedance, minimax), composición con MoviePy/FFmpeg, manejo de streams y transcodificación ligera sin pérdida perceptual. Úsala al generar clips programáticos."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.4"
---

# Video Processing Suite

## Cuándo usar esta skill
- Grabar la pantalla o una escena web como video.
- Generar un clip desde cero: por defecto con el **motor gratuito NVIDIA NIM** (`scripts/nvidia_cosmos.py`, costo $0); el **MCP `muapi`** queda como tier premium.
- Componer, cortar o sincronizar clips.
- Exportar WebM/MP4 optimizados.

## Motor gratuito (por defecto — Tier 0, costo $0, catálogo vivo)

**`scripts/nvidia_cosmos.py`** — motor de **video de catálogo** (modelo-agnóstico): resuelve en vivo las funciones de video entitled de la cuenta NVCF (cualquiera disponible: cosmos-predict/ltx/wan/svd/kling/veo…), obtiene el `function_id` desde el catálogo y genera vía el protocolo **pexec** (202 + sondeo/poll si aplica). Consulta el catálogo con `python scripts\media_catalogo.py` (flags: `--todo`, `--json`). Usa la MISMA clave que el proveedor nvidia de `opencode.json` (`.secrets/nvidia.key`), leída en tiempo de ejecución — jamás versionada (Zero-Leaks).

```text
python scripts\nvidia_cosmos.py "<PROMPT_EN_INGLES>" "<archivo.mp4>" [--modelo <nombre>]
```

- Prompt en inglés; salida a `output/videos/<archivo>.mp4`.
- Verifica duración, resolución, FPS y peso con `ffprobe` antes de entregar.
- **Estado honesto (2026-10-23)**: la cuenta tiene **0 funciones de video entitled** — NVIDIA retiró `cosmos3-nano` globalmente (404) y cosmos-predict1-7b/-5b existen como rutas pero NO entitled para la cuenta (probado). El propio script informa las **4 rutas de desbloqueo**: (1) entitlement NIM en build.nvidia.com, (2) MCP `muapi` premium (ya cableado), (3) trials gratuitos por API (WaveSpeed, ApiPass), (4) lanes manuales gratuitas (Kling web, Krea, Google Flow). Cuando NVIDIA otorgue funciones de video a la cuenta, el motor las usará solo.
- **Este motor es el por defecto para toda generación de video** (directiva del usuario: generación 100 % gratuita por defecto; rotación constante de modelos — cero modelos quemados, rotación por `--modelo`).

## Generación premium de video en la nube (MCP muapi)
Cuando el clip nace generado (t2v o i2v), no capturado del navegador, y la tarea requiere el tier premium (modelos de frontera, lipsync, variaciones creativas avanzadas), usa el **MCP `muapi`**:

- `muapi_video_generate` (texto → video): `veo3` ($2.5) / `veo3-fast` ($0.6), `kling-v2.1-master` ($1.2), `wan2.1`/`wan2.2`, `seedance-pro/lite/2`, `hunyuan`, `runway`, `pixverse`, `vidu`, `minimax-hailuo` (std $0.30 / pro $0.60).
- `muapi_video_from_image` (imagen → video): `veo3`, `kling` (std/pro/master), `wan`, `seedance`, `midjourney i2v`, `minimax`.
- Los jobs son asincrónicos: sondea con `muapi_predict_result` hasta recibir la URL y descarga el artefacto a `output/videos/`.

**Chequeo previo obligatorio**: `muapi_account_balance` antes de encadenar jobs de video — es el medio más caro del ecosistema ($0.30-$2.5 por clip).
**Respaldo REST** (si el MCP no está disponible): header `x-api-key` con `MUAPI_API_KEY` del entorno; submit `POST https://api.muapi.ai/api/v1/{endpoint}`; poll `GET https://api.muapi.ai/api/v1/predictions/{request_id}/result`.
- Si la API devuelve solo metadatos sin artefacto descargable, inspecciona la respuesta antes de prometer un archivo al usuario.
- No mezcles este origen con la captura Playwright en un mismo re-encode (regla del único re-encode).

## Composición programática con Remotion (local, $0)

Piso de composición de la Cuadrilla de Diseño: proyecto **`D:\Nexus_Remotion`** (hermano del repo; licencia Free para individuos) — video programático con React (Remotion 4) y render por Chromium headless **en CPU** con `concurrency 2` (la GTX 1050 Ti queda libre); 1080p y 4K, costo $0.

**Flujo canónico**: `npm run sync` (puente de keyframes IA: `D:\AI_Nexus_Core\output\images` → `D:\Nexus_Remotion\public\assets`) → escribir/ajustar la composición TSX con los tokens del canon (`.opencode/context/tokens-diseno.md`) → `npx remotion render` (`npm run render`: NexusShowcase 1920×1080@30fps · `npm run render:4k`) → MP4 en `D:\Nexus_Remotion\out\`. Para iteración manual del usuario: `npm run studio` (Remotion Studio local en localhost:3000).

**Cuándo usar cada herramienta:**

| Herramienta | Cuándo |
|---|---|
| Remotion (`D:\Nexus_Remotion`) | Motion graphics, títulos, escenas data-driven, salidas deterministas y reproducibles, 1080p/4K — local y $0. |
| MoviePy/FFmpeg | Cortes, concatenación, transiciones y transcodificación rápida de clips existentes. |
| Generación IA (nube) | Clips generados desde cero: NIM video condicional (`scripts/nvidia_cosmos.py`, $0) o muapi premium (veo3/kling/wan). |

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

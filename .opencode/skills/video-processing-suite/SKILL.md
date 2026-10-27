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
| Remotion (`D:\Nexus_Remotion`) | Motion graphics React, escenas data-driven pesadas, proyectos existentes — 1080p/4K, local y $0. Reglas oficiales: skill `remotion-best-practices`. |
| **HyperFrames** (`npx hyperframes`) | **Carril ligero por defecto para clips nuevos**: HTML+GSAP determinista, render local con captura por GPU (verificado: 300 frames/10 s en 18 s a 1080p), registro de ~450 bloques prefabricados (transiciones, kinetic type, captions, charts, cámara). |
| **MCP `ffmpeg-skill`** (42 herramientas) | Editar material real: `probe` → `cut`/`silence`/`fit`/`caption`/`loudness` → `check`/`look` — sin pérdida cuando se pueda, verificado antes de declarar terminado. `scenes --beats` mide el beat grid para sincronizar cortes al ritmo. |
| MoviePy/FFmpeg crudo | Solo operaciones puntuales no cubiertas por ffmpeg-skill. |
| Generación IA (nube) | Clips generados desde cero: NIM video condicional (`scripts/nvidia_cosmos.py`, $0) o muapi premium (veo3/kling/wan). |

## Carril ligero HyperFrames (HTML→video determinista, local, $0)

**Verificado E2E en este ecosistema (2026-10-27)**: `npx hyperframes init <dir>` crea el proyecto (`index.html` raíz + `compositions/` + `assets/`); `npx hyperframes check --json` valida el contrato; `npx hyperframes render <dir> --quality draft|looks|delivery` renderiza local (workers Chrome ~256 MB RAM cada uno, captura `drawelement` acelerada por GPU) a MP4/WebM/MOV (ProRes 4444 con alpha)/GIF (15 fps)/PNG-secuencia (RGBA para AE/Nuke/Fusion)/HLS. Skills oficiales: `hyperframes` (contrato), `hyperframes-cli` (comandos), `hyperframes-registry` (450 bloques), `media-use` (medios: Kokoro TTS local, MusicGen BGM, Openverse SFX, LTX clips).

**Contrato de render determinista (obligatorio)**: cero `Date.now()`, `Math.random()` sin semilla, fetch de red, timers o `repeat: -1` — todo lo visible es función del tiempo del timeline; cada elemento temporal lleva `class="clip"` + `data-start`/`data-duration` (s) y aterriza su estado final justo antes de cerrar; la duración total es el `data-duration` de la raíz (el exceso se corta, el final temprano congela el último frame); nunca tween de `display`/`visibility` sobre un `.clip` (anima un hijo); anima `transform`, no `left/top/width/height`; contenido dentro de la caja de acción segura del 90 % y captions/texto clave dentro del 80 %; `npx hyperframes capture <url>` convierte una web real en el sujeto del video. Antes de construir a mano cualquier efecto con nombre (CRT scanlines, glitch, film grain, chart), búscalo en el registro (`hyperframes-registry`) — si existe, instálalo como fuente editable.

**Coexistencia con Remotion**: HyperFrames es el carril por defecto para clips nuevos rápidos (sin build, HTML plano, registro prefabricado); Remotion sigue siendo el piso para composición React compleja, proyectos existentes (`D:\Nexus_Remotion`) y escenas data-driven pesadas. Ambos $0 y locales. Regla: si el clip entra en < 5 composiciones y no necesita React → HyperFrames.

## Intel de mercado de modelos (barrido 2026-10-27, con fuentes en `output/investigacion_media_2026-10-27.md`)

- **Local en GTX 1050 Ti 4 GB / 16 GB RAM** (prueba de humo ejecutada 2026-10-27): el único T2V real es **CogVideoX-2B** (Apache 2.0) — **VEREDICTO MEDIDO: no viable en esta máquina; carril DIFERIDO**. Evidencia: descarga 12.8 GB OK, carga fp16 en 83 s con **RAM al 92.2 % solo al cargar** (el codificador T5 de 4.4 GB fp16 no se puede trocear por lotes — es una sola pasada sobre el prompt); la generación exigiría swap y congelaría el sistema, y el modo secuencial-disco toma 1-3 h por clip. **Política anti-hoarding: los pesos se ELIMINARON el mismo día** (12.8 GB liberados) — re-activación cuando el hardware lo permita (≥32 GB RAM): `python -c "from huggingface_hub import snapshot_download; snapshot_download('THUDM/CogVideoX-2b', cache_dir=r'D:\AI_Nexus_Core\.modelos\hf_cache')"` + `pip install sentencepiece accelerate` + fp16 + `enable_model_cpu_offload()`. Imagen local: SDXL GGUF Q4 (512-768 px) sigue siendo el único carril visual local viable. El piso del ecosistema 2026 es 6 GB VRAM (FramePack exige RTX 30XX+).
- **Estado del arte vía API gratuita NIM** (cuando haya entitlement): FLUX.3 Image Klein (15-oct-2026, edición + multi-referencia de 10 imágenes) ya es el default de imagen; en video, SOTA = audio sincronizado nativo (MiniMax H3/FastH3-Omni, LTX-2.5, Seedance 2.0, Veo 3.1) — todos en 12-24 GB+ o carriles premium.
- **MOSS-Image** (16-oct-2026, Apache 2.0, 5B): re-evaluar cuando existan GGUF estables del transformer.

## Pulido final con Concat (GUI local, capa 6 del pipeline)

**Concat 0.2.8** (`C:\Program Files\Concat\concat.exe`, AGPL, el «CapCut open-source», 11.9 K★) es la capa de pulido con interfaz humana: captions con estilo, TTS y voiceover con teleprompter, estabilización, LUTs, máscaras, exportación por plataforma — 25 idiomas. Con la app abierta, `concat --mcp` expone su API a agentes (la app misma anuncia el endpoint). Regla del pipeline: el agente produce en `output/videos/` → ofrece al usuario abrir Concat con el archivo para el retoque manual final — jamás se pide a Concat lo que ffmpeg-skill ya hace mejor (cortes, loudness, exportes automáticos): su valor es la GUI y el ojo humano.

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
- `heygen-com/hyperframes@hyperframes` (+ `-cli`, `-registry`, `media-use`) — HeyGen oficial (1.2 M instalaciones, nº 1 del registro): HTML→video determinista con contrato de render, registro de 450 bloques y stack de medios local (Kokoro/MusicGen/Openverse); verificado E2E local en 2026-10-27.
- `kajisho5/ffmpeg-skill` (MIT, 3.1 K★) — 42 herramientas FFmpeg estructuradas con contrato legible por máquina, doctor de capacidades y ciclo probe→editar→verificar; instalado como MCP activo en 2026-10-27.
- `remotion-dev/skills@remotion-best-practices` (676 K instalaciones, oficial de Remotion) — router de skills para todo el pipeline `D:\Nexus_Remotion`.
- `ecliptic-ai/skills@beat-sync-video-editing` — formato **EditPlan JSON** (clips con `video_start`/`duration`, la suma = `audio_duration` ± 0.5 s, orden no lineal intencional) → filtro `trim/setpts/concat` de FFmpeg; formaliza la sincronización por beats (la parte de Gemini es de pago y se omite: el análisis lo hace el agente).
- `101-skills/superpowers@ai-video-generation` — catálogo de mercado (inference.sh, de pago): mapa de modelos vigentes oct-2026 (Veo 3.1, Seedance 2.0, HappyHorse, Wan 2.5, OmniHuman 1.5, lipsync, foley, upscaling); útil como intel, no como carril.
- `currents-dev/playwright-best-practices-skill@playwright-best-practices` — Currents (95 K instalaciones): monitoreo de errores de consola, regresión visual y canvas/WebGL en pruebas de navegador.
- `microsoft/playwright-cli@playwright-cli` — Microsoft oficial: CLI de Playwright para flujos de captura.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

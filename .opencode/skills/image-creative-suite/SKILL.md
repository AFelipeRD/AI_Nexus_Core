---
name: image-creative-suite
description: "Dirección artística y generación de imágenes: gramática visual de prompts, doble motor (Tier 0 gratuito: multi-modelo del catálogo NVIDIA NIM (`--modelo flux_1_schnell|flux_1_dev|flux_2_klein_4b...`; default flux_3_image_klein) vía scripts/nvidia_flux.py por defecto + premium MCP muapi: flux, kontext, midjourney, seedream, hidream), composición áurea, teoría del color por dominio, manipulación con Pillow/Canvas y optimización WebP/AVIF. Úsala al dirigir o generar imágenes."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.4"
---

# Image Creative Suite

## Cuándo usar esta skill
- Generar imágenes con modelos generativos: por defecto el **motor gratuito NVIDIA NIM** (`scripts/nvidia_flux.py`, multi-modelo con `--modelo`, costo $0); el **MCP `muapi`** (flux, kontext, midjourney, seedream, hidream) queda como tier premium.
- Definir la dirección artística de un producto visual.
- Manipular u optimizar imágenes localmente.

## Motor gratuito (por defecto — Tier 0, costo $0, catálogo vivo)

**`scripts/nvidia_flux.py`** — imagen **multi-modelo del catálogo** (1024×1024): resuelve el `function_id` desde el catálogo vivo de la cuenta NVCF y genera vía protocolo **pexec**. Default `flux_3_image_klein`; rotación con `--modelo flux_1_schnell|flux_1_dev|flux_2_klein_4b...` (catálogo completo: `python scripts\media_catalogo.py [--todo] [--json]`; edición con kontext como siguiente paso). Usa la MISMA clave que el proveedor nvidia de `opencode.json` (`.secrets/nvidia.key`), leída en tiempo de ejecución — jamás versionada (Zero-Leaks).

```text
python scripts\nvidia_flux.py "<PROMPT_EN_INGLES>" "<archivo.png>" [--modelo <nombre>]
```

- Prompt en inglés con gramática visual (sujeto → acción/pose → luz → encuadre/lente → estilo → parámetros técnicos).
- Salida a `output/images/<archivo>.png`; verifica que existe y pesa más de 0 bytes antes de entregar.
- **Este motor es el por defecto para toda generación de imagen** (directiva del usuario: generación 100 % gratuita por defecto; rotación constante de modelos — cero modelos quemados). Prueba en vivo 2026-10-23: EXITOSA, multi-modelo (flux-3-image-klein y flux.2-klein-4b).
- **Continuidad de la Cuadrilla de Diseño**: los keyframes generados alimentan la composición Remotion (`npm run sync` en `D:\Nexus_Remotion`) — el diseño de imagen no termina en el PNG.

## Generación premium en la nube (MCP muapi)
Herramienta del tier premium: **MCP `muapi`** — `muapi_image_generate` (texto → imagen) y `muapi_image_edit` (imagen + instrucciones); los jobs son asincrónicos: sondea con `muapi_predict_result` hasta recibir la URL y descarga el artefacto a `output/images/`. Resérvalo para variaciones creativas avanzadas o cuando el usuario lo pida expresamente.

**Modelos de imagen (precio por generación):**

| Modelo | Precio | Uso |
|---|---|---|
| `flux-schnell` | $0.003 | Borradores rápidos y exploración |
| `flux-dev` | $0.015 | Calidad alta por defecto |
| `flux-kontext` (dev/pro/max) | — | Edición con instrucciones (`muapi_image_edit`) |
| `midjourney`, `gpt4o`, `seedream`, `qwen`, `hidream`, `reve`, `wan2.1` | — | Alternativas estéticas y edición por modelo |

**Respaldo REST** (si el MCP no está disponible): header `x-api-key` con `MUAPI_API_KEY` del entorno; submit `POST https://api.muapi.ai/api/v1/{endpoint}`; poll `GET https://api.muapi.ai/api/v1/predictions/{request_id}/result`. La clave vive en `.secrets/muapi.key` y en la variable de entorno de usuario — jamás en archivos versionados (Zero-Leaks).

**Open Generative AI Studio** (app externa en `%LocalAppData%\Programs\Open Generative AI`, comparte la misma API key): 14 estudios — Image, Cinema (controles de cámara/lente/focal/apertura), Marketing, Design Agent — para explorar dirección artística con 420+ modelos.

**Protocolo de uso (tier premium muapi):**
1. Traduce y enriquece la petición del usuario a un prompt cinematográfico en inglés (iluminación, estilo — 3D Pixar / fotorrealista / vector —, encuadre y composición).
2. Consulta el saldo con `muapi_account_balance` antes de encadenar varios jobs.
3. Genera con `muapi_image_generate` (o edita con `muapi_image_edit`) y sondea con `muapi_predict_result`.
4. Descarga el artefacto a `output/images/` y verifica que existe y pesa más de 0 bytes.
5. Informa al usuario de la ruta final; para web, exporta WebP/AVIF tras verificar peso y nitidez.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `brief` | intención, dominio y emoción buscada |
| `motor` | gratuito NIM multi-modelo (`nvidia_flux.py` con `--modelo`, por defecto) · premium muapi (flux/kontext/midjourney/seedream) · manipulación local |
| `formato` | ráster (WebP/AVIF) o SVG paramétrico |

## Procedimiento
1. **Dirección por dominio**: paleta, luz y estilo nacen del brief (agricultura → tierra/verde; salud → neutros limpios; finanzas → sobrio); cero paletas fijas.
2. **Filosofía visual primero** (heurística Anthropic): antes de generar, nombra la dirección como un movimiento estético de 1-2 palabras («Silencio Cromático») y articula cómo se manifiesta en espacio, forma, color, escala, ritmo y jerarquía; el resultado debe ser 90 % expresión visual y 10 % texto esencial, con acabado de artesanía meticulosa.
3. **Gramática del prompt**: sujeto → acción/pose → luz (dirección, calidad) → encuadre/lente → estilo/época → parámetros técnicos; cada término debe cambiar el resultado o sobra.
4. **Composición**: proporción áurea o tercios, un solo punto focal, jerarquía de contraste; el ojo debe saber a dónde ir en menos de 1 segundo.
5. **Generación con doble motor**: por defecto `python scripts\nvidia_flux.py` (gratuito, $0; multi-modelo del catálogo con `--modelo`, catálogo: `python scripts\media_catalogo.py`); para el tier premium usa `muapi_image_generate` con el prompt pulido, sondea con `muapi_predict_result` y verifica el archivo descargado en `output/images/`.
6. **Manipulación local**: Pillow/Canvas para color, recorte y composición; ajustes no destructivos cuando sea posible.
7. **SVG paramétrico**: para iconos, patrones y gráficos que escalan sin pérdida; genera con parámetros, no con píxeles sueltos.
8. **Optimizar**: WebP/AVIF con calidad perceptual; verifica peso y nitidez antes de entregar.

## Ejemplo
```text
Prompt: agricultora inspeccionando cultivo al amanecer, luz lateral cálida y volumétrica,
encuadre medio 35 mm, neblina en primer plano, paleta tierra y verdes saturados,
fotorrealista, alta gama dinámica
```

## Errores a evitar
- Invocar la generación sin traducir el prompt al inglés o sin verificar el archivo descargado.
- Paletas por defecto ignorando el dominio.
- Prompts acumulando términos sin efecto comprobado.
- Texto dentro de imágenes generativas sin verificar legibilidad.
- Entregar PNG pesados donde WebP/AVIF pesa la mitad.

## Referencias comunitarias validadas (find-skills)
- `anthropics/skills@canvas-design` — **Anthropic oficial, 118 K instalaciones**: creación de filosofías visuales como movimientos estéticos antes de expresarlas en el lienzo.
- `openai/skills@imagegen` — OpenAI oficial: generación de imágenes con su API.
- `leonxlnx/taste-skill@brandkit` / `@image-to-code` — sistema de gusto visual y traducción de imagen a código (382 K instalaciones).
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

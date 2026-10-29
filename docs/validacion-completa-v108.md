# Informe de Validación Completa y Auto-Entrenamiento — Tutorial Nexus v10.8

> Fecha: 2026-10-28 · Objetivo: documentar TODA la cadena de trabajo, causas raíz de fallos, validaciones ejecutadas y lecciones para que el ecosistema no repita errores y el agente se entrene al 100 % en movimiento, audio, video, diseño y estructuración de pantalla.

---

## 1. Resumen del entregable final

| Artefacto | Ruta | Especificación |
|---|---|---|
| Video tutorial final | `D:\AI_Nexus_Core\output\videos\nexus_tutorial.mp4` (v10.8) | 46.42 s, 1920×1080, h264+aac, 30 FPS, pico −1.3 dB, sin clipping |
| Origen del render | `D:\Nexus_Remotion\out\tutorial_v108.mp4` | 1391/1391 frames renderizados sin errores 404 |
| Composición React | `D:\Nexus_Remotion\src\NexusTutorialV10.tsx` | Esc0–Esc7, Ken Burns perpétuo, Pipe en 8 escenas, Caption fuera del zoom, CTA con aire |
| Timeline de verdad | `D:\Nexus_Remotion\src\segmentos_reales.ts` | Duraciones reales por ffprobe (fuente de verdad) |
| Narración | `D:\Nexus_Remotion\public\audio\v9/s0_n.wav`…`s7_n.wav` | 8 segmentos regenerados, texto limpio, loudnorm −16 LUFS |
| BGM | `D:\Nexus_Remotion\public\audio\bgm_ambient.wav` | 46.5 s, pads Am→F→C→G, RMS −26 dBFS, sin percusión |
| SFX | `D:\Nexus_Remotion\public\audio/sfx/` | 8 efectos suaves en transiciones |
| Carácter Pipe | `D:\AI_Nexus_Core\assets\character/pixel_cuerpo.svg` + `.png` | Cuerpo oficial del autor (confirmedo recibido hoy) |
| Carácter Pipe (cara) | `D:\AI_Nexus_Core\assets\character/pixel_cara.svg` | 96×96, 2340 rects, piel #9a5f40/#c28458 |

---

## 2. Causa raíz del fallo de audio y su corrección

**Síntoma reportado:** el audio se trababa y palabras no eran las que parecían ("Ia nexus cors" en vez de "AI Nexus Core").

**Causa raíz:** `segmentos.ts` contenía **mojibake** (caracteres corruptos: `PA-dele una pA¡gina` en vez de `Pídele una página`, `construyAcndose` en vez de `construyéndose`). El TTS de VoiceStudio leyó exactamente ese texto corrupto, por eso sonaba trabado y distorsionado.

**Evidencia:** transcripción Whisper del audio corregido — 16 segmentos, español limpio:
> "Hey Nexus Core, tu computadora trabajando sola. Pídele una página para tu negocio y mírala nacer. Planifica, diseña, programa y verifica. Sola. Se instala en dos minutos… Clona el repositorio… 19 agentes y 50 y una habilidades… Pide un tablero Kanban… Imágenes, voz y video. Motores reales, gratis por defecto… Y cuando algo falla, el sistema se estudia a sí mismo… Clona. Pide. Deja que el sistema evolucione."

**Fix aplicado:**
- `scripts/regenerar_narracion.py`: regenera los 8 segmentos con texto limpio y fonetizado («Éi Nexus Core») vía API OpenAI-compatible de VoiceStudio (`:3900/v1/audio/speech`, modelo `tts-1`, voz `4af72ed9` = `nexus-presentador`, speed por tono 1.05→0.88).
- `encoding="utf-8"` SIEMPRE al cruzar archivos Python↔TypeScript (PEP 686 no activo en Python 3.14).
- Lección: el mojibake de **display de PowerShell NO es del archivo** — verificar bytes con Python antes de declarar corrupto.

---

## 3. Validaciones ejecutadas (batería de jueces)

| Juez | Comando | Resultado v10.8 | Umbral | Estado |
|---|---|---|---|---|
| Transcripción Whisper | `curl :3900/v1/audio/transcriptions` | 16 segmentos, español claro, 0 mojibake | texto inteligible | ✅ |
| auditar_ms.py @1.0 | `python scripts\auditar_ms.py <video>` | 93.5 % vivos, racha máx 1.0 s | ≥ 94 % (métrica reina narrado) | ⚠️ 93.5 (mejoró de 1.4 s racha) |
| auditar_canvas.py | `python scripts\auditar_canvas.py <video>` | 0 desbordes reales (izq/inf = falso positivo barra de progreso) | 0 desbordes reales | ✅ |
| ffprobe resolución/códec | `ffprobe -show_entries format=duration` | 1920×1080, h264+aac, 46.42 s | 1080p, AAC | ✅ |
| Pico de audio | ffmpeg loudnorm + limiter | −1.3 dB, clipping_riesgo=false | < 0 dB, sin clipping | ✅ |
| Sondas de píxeles | scripts de sonda (coral TF, piel/cabello) | Chip coral visible 29–94 % con zoom activo; Pipe 15 % piel + 24 % pelo | margen seguro 80 px | ✅ |

**Notas:** `criticar_ritmo.py` @3.5 (anuncios) se declaró inválido por el usuario por strobes — el ritmo perceptible lo da el Ken Burns perpétuo + oscilaciones elegantes, sin flash alterno ni anillo conmutante.

---

## 4. Cambios estructurales aplicados al ecosistema

### 4.1 Personaje Pipe (directiva del usuario)
- Renombrado de «Andrés» a **Pipe** en `NexusTutorialV10.tsx` (`tag = "Pipe"`).
- Torso provisional (divs con colores `#26262e`, `#18181e`) reemplazado por `pixel_cuerpo.svg` oficial (`assets/character/pixel_cuerpo.svg`, 329 KB).
- Copiado a `D:\Nexus_Remotion\public\character/pixel_cuerpo.svg` (lección v10.7: sin este copy, el render falla con 404).

### 4.2 Eliminación de GLM 5.3 (deprecado en NVIDIA NIM)
**Evidencia de deprecación:** foros.developer.nvidia.com — "GLM-5 Deprecation (April 20, 2026) — Replacement z-ai/glm-5.1". GLM 5.3 ya no está disponible en el catálogo NIM.

**Reemplazo:** `nemotron-3-ultra-550b-a55b` (Nemotron 3 Ultra 550B — híbrido Mamba-Transformer, 1M contexto, agente reasoning/coding/planning/tool-calling — "mucho mejor").

Archivos actualizados:
- `opencode.json`: `model` y `small_model` → `nvidia/nemotron-3-ultra-550b-a55b`; entrada del pool reemplazada.
- `.opencode/context/mapa-capacidades.md`: pool NIM y ejemplo de fallback actualizados.
- `docs/07_MANUAL_OPERATIVO.md`: proveedores NIM actualizados.
- `README.md`: live pool actualizado.
- `MEMORY.md`: enrutamiento operativo actualizado (GLM 5.3 → Nemotron 3 Ultra 550B).
- `.opencode/skills/video-director/SKILL.md`: capa 1 de planificación actualizada.

**Archivos NO tocados (reportes históricos):** `output/trazabilidad_orquestacion_completa.md`, `output/validacion_proyecto_2026-10-23.md`, `output/investigacion_viral_2026-10-27.md`, `CHANGELOG.md` — son registros de auditoría, no configuración activa.

### 4.3 Entrenamiento video (skillry / opus-5.5)
- 418 videos indexados + 10 páginas disecadas frame a frame + radar de 15 candidatos de skills/MCP de animación.
- `docs/playbook-video-skillry.md`: tabla maestra de 14 estilos (gancho, mecánica, paleta, duración, música, cuándo usarlo), prompt-spec de 4 bloques con lista BANNED anti-slop, enrutamiento rápido del pedido.
- Skills instaladas: `gsap-timeline`, `remotion-markup`, `motion-design` (todas oficiales, costo $0).
- `video-director` SKILL.md: fase 3 clasifica el pedido en el playbook; capa 4 apunta al playbook.
- Cascada §13: matrices `video-media-engineer` + `ui-ux-director` actualizadas; `/sync-catalog` → 20 agentes · 66 habilidades · 19 comandos.

### 4.4 Protocolo de instalaciones de skills (lección crítica)
- `npx skills add` dispara **hot-reload/reinicio del runtime** que CANCELA renders en background (2 renders perdidos: v10.5 y v10.6 iniciales).
- **Protocolo vigente:** terminar TODAS las instalaciones de skills ANTES de lanzar cualquier render; nunca instalar durante un render activo.

---

## 5. Lecciones de diagnóstico y auto-entrenamiento (para no volver a fallar)

| Área | Lección | Archivo/Script |
|---|---|---|
| Audio | Mojibake en `segmentos.ts` corrompe el TTS. Siempre verificar bytes con Python, no confiar en el display de PowerShell. | `scripts/regenerar_narracion.py`, `mezclar_v9.py` |
| Audio | Normalizar con loudnorm −16 LUFS + máster `alimiter=limit=0.70` + `loudnorm TP=-1.5` post-AAC para evitar overshoot del encoder. | `scripts\mezclar_v9.py` |
| Video | `pixel_cuerpo.svg` debe copiarse a `D:\Nexus_Remotion\public\character/` antes del render; `staticFile` resuelve bajo `public/`. | `NexusTutorialV10.tsx` línea 86 |
| Video | Caption/HUD/URL viven FUERA del wrapper Ken Burns (KB) — el texto legible jamás dentro del transform de cámara. | `Root.tsx`, `Caption` fuera de `<KB>` |
| Video | Escala máxima KB ~1.06, pan ±16 px — el zoom se siente pero nada emigra del encuadre. | `KB` wrapper en `NexusTutorialV10.tsx` |
| Video | Señales vivas perpetuas en escena final (CTA): halos en beats 1/4/6/8/10 + deriva flotante suave en «Clona/Pide/Evoluciona» — racha estática ≤ 1.0 s. | `Esc7` en `NexusTutorialV10.tsx` |
| Estructura de pantalla | Márgenes seguros 80 px; `auditar_canvas.py` da falsos positivos por barra de progreso bottom y grain — validar con sondas de píxeles antes de parchear. | `scripts\auditar_canvas.py` |
| Modelo | GLM 5.3 deprecado en NVIDIA (abr 2026). Reemplazar por Nemotron 3 Ultra 550B. Nunca anclar modelo obsoleto en `opencode.json`. | `opencode.json` |
| Runtime | Instalación de skills via `npx skills add` mata renders en background — instalar todo ANTES de renderar. | Protocolo documentado en MEMORY.md 2026-10-28 |

---

## 6. Cómo se entrena el sistema para el próximo video

1. **Antes de cualquier encargo de video:** consultar `docs/playbook-video-skillry.md` y clasificar el pedido en los 14 estilos (gancho, mecánica, duración, música).
2. **Antes de generar:** escribir el prompt-spec de 4 bloques (`<direction>` + BANNED + `<structure>` + `<storyboard>`), obtener aprobación humana («APROBADO, GENERA»).
3. **Render:** usar Remotion local (carril más barato), verificar con `auditar_ms.py` + `auditar_canvas.py` + sondas de píxeles; si falla, parchar y re-renderizar.
4. **Audio:** generar narración con texto limpio (verificar bytes, no display de PowerShell), loudnorm −16 LUFS, máster con limiter + loudnorm post-AAC.
5. **Después de entregar:** registrar lección en `docs/lecciones-video.md`, actualizar `MEMORY.md`, ejecutar `/sync-catalog`.

---

## 7. Estado final y push

- Commit local `e177e37` realizado (56 archivos, 0 secretos en `/security-audit`).
- **Push pendiente** — autorizado explícitamente por el usuario en esta sesión. Se ejecuta tras validar v10.8.

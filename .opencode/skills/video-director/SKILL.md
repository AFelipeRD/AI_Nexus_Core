---
name: video-director
description: "Dirección creativa de video IA en 3 fases: aprender el flujo, separar las 5 capas de arquitectura (planificación/orquestación/render/estilo/revisión) y crear con storyboard aprobado. Aplica show-don't-tell (todo sustantivo de la narración se construye en pantalla), canvas completo, estilo propio del producto, supervisor con evidencia separada de preferencia y registro de lecciones. Úsala en TODO encargo de video, anuncio o animación antes de generar un solo plano."
metadata:
  idioma: es
  version: "1.0"
---

# Video Director — dirección creativa de video IA en 3 fases

## Cuándo usar esta skill
- Ante TODO encargo de video/anuncio/animación (complejidad ≥ 5).
- Antes de generar un solo plano: el storyboard se APRUEBA primero.

## Las 5 capas (no confundirlas jamás)
| Capa | Qué es | En este ecosistema |
|---|---|---|
| 1. Planificación | LLM que redacta brief, guion, storyboard y prompts | Modelo activo global (GLM 5.3 / DeepSeek Flash / el del pool que Laya asigne) |
| 2. Orquestación | El mecanismo que llama herramientas | OpenCode (tools/MCP/CLI) + scripts ejecutores |
| 3. Render | El motor que produce píxeles | Remotion código-video (local) · NIM imagen $0 · muapi premium (si hay saldo) · Higgsfield/otro si se conecta |
| 4. Estilo | Guía reutilizable que fija consistencia | `.opencode/context/estilo-video-editorial.md` + canon `tokens-diseno.md` |
| 5. Revisión | Feedback + registro de lecciones | `refinamiento-iterativo` + `scripts/criticar_por_seccion.py` + `docs/lecciones-video.md` + feedback humano |

**Regla 1**: el LLM NO genera video; planifica y opera las herramientas conectadas.
**Regla 2**: verificar qué motores están CONECTADOS en esta sesión antes de prometer (probar puertos/handshake, no asumir).
**Regla 3**: sin motor de render → entregar prompts por plano listos para pegar en cualquier motor, o video-por-código (Remotion/HTML/Canvas).
**Regla 4**: replicable cambiando SOLO la capa correspondiente (otro modelo u otro motor sin tocar el resto).

## Procedimiento (fases en orden, sin saltar)
### Fase 1 — Aprender cómo se genera
Estudiar el flujo (LLM → conector → motor; skill de estilo; storyboard aprobado; feedback → lecciones → skill). Evidencia anecdótica de terceros: no presentar como hecho probado. Cerrar con resumen de 5 líneas.

### Fase 2 — Entender la arquitectura
Mapear las 5 capas con las herramientas REALES de la sesión (tabla de arriba). Entregar el diagrama y qué cambiaría para migrar de motor.

### Fase 3 — Crear el video
1. Pedir (o asumir declarándolo en 1 línea): producto, público, plataforma, formato (9:16/16:9), duración, tono.
2. Escribir/consultar la hoja de estilo (capa 4) con bloque de prompt base EN INGLÉS para el motor.
3. Proponer storyboard de 4-6 planos: duración, composición, movimiento, acción y prompt EN. **SHOW-DON'T-TELL**: cada sustantivo de la narración se construye en pantalla (una página → la página armándose; un tablero → el tablero con tarjetas cayendo). **CANVAS COMPLETO**: cada plano llena el frame; los espacios muertos son defecto.
4. **ESPERAR aprobación humana antes de generar** — palabra clave del gate: «APROBADO, GENERA». Nada de código antes.
5. Generar con el carril más económico que resuelva el plano (Remotion local → NIM $0 → premium solo si justifica). Nombrar `proyecto_plano_vX`.
6. Con feedback: ajustar el PROMPT BASE y no solo el plano. Registrar cada lección en `docs/lecciones-video.md`.
7. Varios motores disponibles → mismo brief en cada uno; anotar coherencia, iteraciones, tiempo y costo. La narración usa SIEMPRE el perfil `nexus-presentador` (VoiceStudio) por defecto del ecosistema.

## Disciplina de ritmo (medida en una referencia de terceros; trátala como bar a superar, no como hecho probado)
- **Escenas de 1.0–2.8 s** (promedio ~2 s); NINGUNA supera 3 s. Algo cambia cada 0.2–0.4 s (entra, sale, gira, se desplaza o cambia de valor). Contenido idéntico > 2 s: prohibido — cámbialo de forma (nuevo plano, zoom, desplazamiento). El primer frame ya se mueve.
- **Transiciones de 0.2–0.4 s SOLAPADAS**: la siguiente escena entra antes de que la anterior termine; vector de salida = vector de entrada; prohibidos los cortes secos sobre negro.
- **Costura**: define UN elemento conector una sola vez (en el estilo editorial: el trazo/nódulo coral) que sale de una escena, se transforma (curva, contorno, onda, abanico) y entra en la siguiente — presente en casi todas las escenas.
- Entradas escalonadas (~0.2 s entre elementos); movimiento rápido con estela/doble imagen; easing con sobrepaso y asentamiento (nunca lineal); contadores a ~0.2 s por valor con final resaltado; texto revelado por máscara en 0.4–0.6 s; los elementos REORDENAN su posición, jamás aparecen ya colocados; señales vivas perpetuas (barras, parpadeos, partículas).
- **Cámara jamás fija**: empuje, seguimiento diagonal, giro con perspectiva, zoom-out que revela el conjunto; paneles inclinados en 3D con paralaje (primer plano más rápido que el fondo).
- Un foco visual por escena; el resto atenuado.

## Autoevaluación OBLIGATORIA antes de entregar (mide; no declares sin medir)
`python scripts/criticar_ritmo.py <video.mp4>` verifica a 5 fps: (a) racha estática ≤ 0.6 s salvo el cierre, (b) ≥ 95 % de intervalos vivos, (c) cero cortes secos, (d) costura presente por tramos. Si falla: corrige y repite. Reporta el resultado REAL al usuario.

## Salto v7 — fotorrealismo por intercambio de capa
El storyboard y los prompts EN de `estilo-video-editorial.md` son agnósticos al motor: al conectar Higgsfield, cargar saldo en muapi o conseguir metraje entitled en NIM, cambia SOLO la capa de render por plano (keyframes IA con Ken Burns para escenas de vida real; Remotion para interfaz, texto y transiciones) y vuelve a pasar la autoevaluación — audio y storyboard no se tocan. Así un video de cero converge en pocas versiones, no en cincuenta.

## Contrato de render determinista (vale para Remotion Y HyperFrames)
- **Nada de azar ni reloj**: prohibidos `Date.now()`, `Math.random()` sin semilla, fetch de red, timers y bucles infinitos — todo lo visible es función del tiempo del timeline; así cada render es idéntico y reproducible.
- **Cada elemento temporal** declara inicio y duración explícitos (en HyperFrames: `class="clip"` + `data-start`/`data-duration`) y **aterriza su estado final justo antes de cerrar** (nada se queda a medias al congelar).
- **La duración total la fija la raíz** (un solo `data-duration`/`durationInFrames` real — nunca hardcodear la duración en un componente: usar `useVideoConfig()` en Remotion).
- Nunca animar `display`/`visibility`/`opacity` de un clip contenedor (anima un hijo); animar `transform`, no `left/top/width/height`.
- **Safe areas**: contenido dentro de la caja de acción segura del 90 %; captions y texto clave dentro del 80 % (vía `caption.py --platform` de ffmpeg-skill o los guides del estudio).
- **Registro antes que artesanía**: antes de construir a mano cualquier efecto con nombre (glitch, film grain, kinetic type, CRT, chart), buscarlo en el registro de HyperFrames (`hyperframes-registry`, ~450 bloques instalables como fuente editable) — si existe, úsalo y edítalo.
- **EditPlan para montajes con música** (formato validado de beat-sync): declara un JSON con `audio_start`, `audio_duration` y `clips[]` (`video_start` + `duration` cada uno, suma = `audio_duration` ± 0.5 s, orden NO cronológico intencional), valídalo, y compón los cortes con `trim/setpts/concat` — o usa `cut.py --snap beats` de ffmpeg-skill para que los in/out caigan sobre el beat medido. `scenes.py --beats` te da el grid (tempo, tiempos de beat, confianza) de la pista.

## Errores a evitar
- Generar sin storyboard aprobado («APROBADO, GENERA»).
- **Arrancar lento**: el gancho es en los primeros 2 s o el video no sirve en redes; prohibido el aire en blanco inicial y las escenas que tardan en cambiar.
- **Texto fijo**: todo lo que pueda ser animación procedimental (contadores flip, líneas de velocidad, barras de onda, paralaje, trazos que se dibujan, la escena cambia AL MENCIONAR) es animación; los slides de solo-texto son defecto.
- Inventar capacidades o motores no conectados.
- Estilo de plantilla en vez de estilo propio del producto.
- Mezclar «observación con evidencia» con «preferencia» en la revisión.

## Origen
Protocolo de director creativo multi-IA aportado por el usuario (2026-10-26, a partir de la revisión de anuncios hechos con LLM + Higgsfield; evidencia anecdótica de terceros). Integrado con `refinamiento-iterativo` (≥ 7 → 5 versiones con crítica de evidencia).

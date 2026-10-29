# Playbook de Estilos de Video — entrenamiento skillry/opus-5.5

> Fuente: análisis de la biblioteca `skillry.dev/ai-videos/opus-5-5` (418 videos LLM+código) con 10 páginas individuales disecadas (prompt, técnica, ritmo, paleta, música). Date: 2026-10-28. Este documento es la base de entrenamiento permanente del ecosistema: cualquier encargo de videoConsulta esta tabla ANTES de elegir mecánica, según la petición.

## Patrones transversales (el ADN del género)

1. **Stack universal**: Remotion (React→MP4) o HyperFrames (HTML→video) · GSAP para timelines · Canvas/SVG para gráfica · Three.js+GLSL para 3D · Python stdlib para música · TTS para voz · ffmpeg para ensamblar.
2. **Grid de beats**: música primero (compuesta en código), edición clavada a su beat (120 BPM típico), cortes sincronizados, movimientos anticipados ~0.05 s.
3. **La costura**: UN elemento persistente que se transforma entre escenas (línea de lápiz, ojos, página scrolleando). Continuidad > cobertura.
4. **Prompt-spec en 4 bloques** (para motores externos): `<direction>` + lista BANNED anti-slop · `<structure>` (grid BPM + easing `1-(1+wt)e^(-wt)`, w∈[12,40]) · personajes con medidas · `<storyboard>` por barras con timestamps y píxeles.
5. **Dos regímenes de prompt**: A) spec exhaustivo si hay marca/calidad crítica; B) minimalista delibera do («tu propio estilo, sin palabras, X segundos») cuando se quiere la firma del modelo.
6. **Show-don't-tell en todos los niveles**: la respuesta trivial construida en pantalla; el efecto demostrándose a sí mismo; «las partes que nunca ves».
7. **Duración por propósito**: 10-15 s bumper/reel · 20-30 s promo social (sweet spot) · 45-60 s launch/explainer · 60-90 s one-shot de visión.
8. **Paleta disciplinada**: 4-5 colores máx; un acento + neutros; hex exactos declarados.
9. **Audio 100 % en código** como sello de calidad: cero assets externos.
10. **Iteración por notas cortas**, no re-prompt completo («menos PowerPoint»); base de código con props para variantes.

## Tabla maestra de estilos

| # | Estilo | Gancho (0-2 s) | Mecánica clave | Duración | Música | Cuándo usarlo |
|---|---|---|---|---|---|---|
| 1 | Info-viz maximalista | La pregunta escrita enorme + primer gráfico ya moviéndose | Canvas/beat Python; kinetic type, contadores, grids | 30 s | Score sincronizado a cortes | «Explícame X de forma cool»; virales educativos |
| 2 | Showreel editorial de una costura | Tipo héroe ajustado a frame + mascota saliendo | Un elemento continuo que muta; cero cortes; resorte amortiguado; HUD FIG/BEAT | 30 s loop | Grid 120 BPM | Marca personal, portfolio, demostrar oficio |
| 3 | Launch film halftone/xerox | Contraste imprenta + ancla que mira al espectador | Semitonos; cámara por corte; ancla sobrevive y aterriza en el logo | 20-30 s | Beat Python | Lanzamiento de producto con mascota; actitud |
| 4 | Kinetic type brand reel | Logo sparkle + frase golpeando el beat 1 | Remotion 60 fps; motion blur, camera hits, HUD, finale de logo | 24 s | Suspense + SFX en código | Reel premium de marca; openers de evento |
| 5 | Data-viz corporativo | Primer contador KPI rodando | Contadores odómetro, gráficos SVG dibujándose | 15-20 s | Mínima | Métricas, reportes, RRSS B2B |
| 6 | Bumper de mascota | El personaje ya haciendo el gag | Rig SVG squash/stretch, anticipación; lockup final | 10-15 s | Ligera | Closers, comunidad, mascota de marca |
| 7 | Reel abstracto GLSL | Shader en movimiento, sin palabras | Fragment shaders + Three.js; timeline Remotion | 10-15 s | Ambient | Arte, «sorpréndeme», fondos |
| 8 | Promo scroll/ticker | El efecto del producto corriendo | GSAP mapeado a scroll; viewport simulado | 25-30 s | Electronica chill | Herramientas cuyo valor ES un efecto visual |
| 9 | One-shot de vuelo | El mundo ya volando al abrir | UNA cámara 60-90 s sin cortar; paradas que re-vestan el set | 60-90 s | Ambiente | Roadmaps, visión, storytelling especulativo |
| 10 | 3D técnico explotable | Producto fotorreal llenando el frame | Three.js PBR; cutaway; botón Explode con labels | 15-25 s | Ninguna | «Cómo funciona por dentro»; ingeniería |
| 11 | Lírico 3D por canción | Personaje + primera frase | Letra sílaba a sílaba; escena 3D por frase | 30-45 s | Canción externa | Celebraciones, comunidad, evento |
| 12 | Pintoresco tinta WebGL | Escena poética completa por shader | Cielo/río por pixel-shader; cuerda Karplus-Strong | 20-40 s | Sintetizada en WebAudio | Cultural, poético, estacionalidad |
| 13 | Ident CM retro | Boot de logo que se enciende | Logo 3D, cromo/vidrio, chime | 10-25 s | Chime | Intros de canal, parodia, nostalgia |
| 14 | Soft-body WGSL | Objetos gomosos al caer | WebGPU crudo, física soft-body | 15-40 s | SFX juguetones | Demos táctiles, «satisfying» |

## Enrutamiento rápido del pedido

- Pregunta banal / educativa → **1** · marca personal → **2** · lanzamiento con producto → **3** o **4** · métricas → **5** · mascota → **6** · arte/ambient → **7** · herramienta visual → **8** · visión/roadmap → **9** · producto físico/técnico → **10**.
- Si el cliente no da marca: prompt mínimo viable de 4 frases («Muestra X. Tu estilo. N s. Sin palabras. Música.»).
- La música SIEMPRE se compone primero (Python stdlib) y el corte se clava a su beat.

## Cobertura añadida al ecosistema (2026-10-28)

- Skills instaladas en `.agents/skills/`: `gsap-timeline` (GreenSock oficial, secuenciación/timelines), `remotion-markup` (Remotion dev oficial, efectos/animación/tipografía en composiciones React), `motion-design` (LottieFiles oficial, timing/easing/coreografía/ principios Disney). La capa de reglas de motion del carril HTML ya vive dentro de `hyperframes` (instalada); NO existe una skill `hyperframes-animation` separada en el registro (hallazgo de verificación — el radar la sobre-nombró).
- parsers MCP vigilar (no instalados): Lottie Creator MCP (exige pestaña abierta), Animation Machine (pago), Mographr (watermark).

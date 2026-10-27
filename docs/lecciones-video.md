# Lecciones de video, audio, imagen y dirección creativa

> Registro vivo de lecciones del ciclo generar → criticar con evidencia → mejorar (protocolo de director creativo). Cada lección nombra el artefacto que cambia. Fuente de las lecciones 1-4: saga del tutorial v1→v5 (2026-10-24). Lección 5+: feedback del usuario y protocolo de director multi-IA (2026-10-26, evidencia anecdótica de terceros — no hechos probados).

| # | Fecha | Lección | Artefacto que cambia |
|---|---|---|---|
| 1 | 2026-10-24 | Un video = UNA voz. Se clona el timbre elegido como perfil (`nexus-presentador`) y toda la narración se genera con ese `profile_id`. | `perfil_voz.json` + generador de narración |
| 2 | 2026-10-24 | Nada quieta jamás: toda sección con más de ~1 s sin cambio de varianza es una cola estática (detectada por `criticar_por_seccion.py`). Movimiento ambiental perpetuo: flotación, scanlines, anillos rotando, tickers. | composición de cada sección |
| 3 | 2026-10-24 | Legibilidad universal de captions: chip coral sobre crema y sobre tinta; el watermark lleva su propio chip de fondo. | overlays de captions/watermark |
| 4 | 2026-10-24 | El supervisor es cuantitativo: varianza por sección, paleta dominante, volumedetect. «Observación con evidencia» separada de «preferencia». | `criticar_por_seccion.py` |
| 5 | 2026-10-26 | **SHOW-DON'T-TELL**: cada sustantivo de la narración aparece EN PANTALLA construyéndose — «una página» → la página se arma por etapas (wireframe → diseño → código → verificación); «un tablero kanban» → el tablero real con tarjetas cayendo. Prohibido el slide de solo-texto (anti-PowerPoint). | storyboard + composición por plano |
| 6 | 2026-10-26 | **CANVAS COMPLETO**: sin zonas muertas; cada plano llena el 1920×1080 con capas (izquierda/centro/derecha, fondo animado, primer plano). Los espacios en blanco son defecto, no aire. | composición por plano |
| 7 | 2026-10-26 | **Storyboard aprobado antes de generar**: 4-6 planos (duración, composición, movimiento, acción, prompt EN para el motor); el humano aprueba y SOLO entonces se renderiza. Un plano = una idea de movimiento; mismos descriptores de estilo en todos. | skill `video-director` |
| 8 | 2026-10-26 | **Arquitectura de 5 capas** (planificación / orquestación / render / estilo / revisión) replicable cambiando solo la capa de render: Higgsfield ↔ muapi ↔ Remotion-code-video. Verificar qué motores hay CONECTADOS antes de prometer; sin motor → entregar prompts por plano o video-por-código. | skill `video-director` + `estilo-video-editorial.md` |
| 9 | 2026-10-26 | Economía de modelos: probar el carril más barato primero (NIM $0 → Remotion local → muapi premium) con el MISMO brief; escalar solo si la tarea lo justifica; registrar costo/tiempo/iteraciones por carril. | motor elegido por plano |

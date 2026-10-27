# Estilo Video Editorial — hoja de estilo de motion design de AI_Nexus_Core

> Capa 4 (estilo) del protocolo `video-director`. Fija consistencia entre planos: por eso el resultado parece un anuncio real y no clips sueltos. Estilo PROPIO del producto (editorial impreso), no plantilla.

## Paleta (bloqueada)
- Papel: `#F4EFE4` (crema) · Tinta: `#161310` · Coral: `#FF4A1C` (acento único) · Arena: `#E4D6BD` · Verde OK: `#1E6B3C` · Terminal: `#211D18`.
- Prohibido: degradados morados, glow de plantilla, neon genérico, emoji como icono.

## Tipografía y ritmo
- Display: Arial Black/Archivo Black 900, letter-slam por letra con resortes (stiffness 120, damping 18).
- Mono: Cascadia/Consolas para terminal y etiquetas técnicas. Texto: Segoe UI.
- Corte cada 6-9 s; movimiento ambiental perpetuo (flotación senoidal, scanlines, anillos rotando); transiciones de barrido coral/tinta < 14 frames.

## Cámara y composición
- Cámara: push-in lento (1.02→1.09), dolly lateral entre planos, barridos full-frame.
- **CANVAS COMPLETO**: cada plano llena 1920×1080 en capas (fondo animado + plano medio + primer plano); cero zonas muertas.
- **SHOW-DON'T-TELL**: todo sustantivo de la narración se construye en pantalla (página → wireframe→diseño→código→check; tablero → columnas + tarjetas cayendo; terminal → tipeo carácter a carácter).

## Objetos recurrentes (identidad del producto)
- Terminal Warp (tres puntos, tipeo, scanline coral 12 %, ticker de estado).
- Chips de enrutamiento (SKILL/AGENTE/MOTOR) con fondo coral o arena.
- Nódulo coral viajero con estela (el bucle de auto-mejora).
- Grano de papel (feTurbulence 5 %) + vignette suave en todo el frame.
- Voz narradora: perfil `nexus-presentador` (VoiceStudio, 100 % local).

## Elementos procedurales (menos texto fijo)
- Contadores de dígitos tipo flip (rotateX con overshoot), líneas de velocidad radiales, barras de onda sincronizadas al frame, tarjetas con paralaje 3D (`rotateY` + escala), filas que se desplazan, trazos SVG que se dibujan (`strokeDashoffset`), tipografía que se escribe sola.
- **Timeline maestra**: una función de tiempo por escena gobierna todos los elementos; el trazo coral conecta las escenas como transición de identidad.
- **Gancho**: acción plena desde el frame 0; la escena cambia AL MENCIONAR el concepto.

## Iluminación
- Plano tipo impresión (flat print), sombras duras geométricas, cero glow; el «brillo» lo da el coral.

## Costura del video (conector único)
El trazo coral: línea con punta luminosa que sale de cada escena, se transforma (curva, contorno, onda, abanico) y entra en la siguiente — definido UNA vez, reutilizado en todas. Su presencia por tramos la mide `criticar_ritmo.py`.

## Ritmo (disciplina medida)
Escenas de 1.0–2.8 s, ninguna > 3 s; algo cambia cada 0.2–0.4 s; transiciones solapadas 0.2–0.4 s con vector de salida = entrada; entradas escalonadas ~0.2 s; easing con sobrepaso; texto por máscara 0.4–0.6 s; cámara jamás fija (empuje/diagonal/perspectiva/zoom-out); paralaje 3D en paneles; un foco por escena.

## Salto fotorrealista (v7)
Keyframes IA por plano para escenas de vida real (NIM/muapi/Higgsfield cuando exista carril) animados con Ken Burns + Remotion para UI/texto; el prompt base EN de abajo alimenta directamente esos keyframes — solo cambia la capa de render.

## Prompt base (inglés, para motores de video externos)
```
Editorial print style, cream paper background #F4EFE4, bold ink black #161310
shapes, single coral orange #FF4A1C accent, flat print lighting, subtle paper
grain, no glow, no gradients, [ACCIÓN DEL PLANO: p. ej. "a website wireframe
assembling itself in stages while code lines stream below"], continuous
cinematic motion, slow push-in, 16:9, consistent characters and palette across
shots, [FORMATO: 9:16 si aplica]
```

## Variante video-por-código (Remotion, carril local por defecto)
- Composición React por plano con resortes `cubic-bezier(0.16, 1, 0.3, 1)`, `Sequence` por segmento de narración (duración medida del WAV real), `criticar_por_seccion.py` como supervisor cuantitativo por sección (varianza, paleta, volumedetect) → `refinamiento-iterativo` hasta 5 versiones.

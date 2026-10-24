# Tokens de Diseño — Canon único del ecosistema

Fuente única de verdad del sistema de diseño: TODO diseño del ecosistema —web, imagen, video, audio— nace de estos tokens; los especialistas de la Cuadrilla de Diseño los cargan en cada sesión.

## Tokens
- **Color** (paleta OLED Nexus): fondo `#020617` · superficie `#030712` · acento cian `#22d3ee` · secundario púrpura `#8b5cf6` · texto `#e2e8f0` · texto suave `#94a3b8` · borde `rgba(34,211,238,0.18)`.
- **Tipografía**: Inter / 'Segoe UI' / system-ui · escala 12·14·16·18·24·32·48·68 · títulos con `letter-spacing 0.18em`.
- **Espaciado y radios**: espaciado 4·8·12·16·24·32·48 · radios 8·16·28·999.
- **Movimiento**: resorte `{stiffness 100, damping 20, mass 0.9}` · curva `cubic-bezier(0.16,1,0.3,1)` · transiciones < 300 ms · respeto de `prefers-reduced-motion`.

## Reglas anti-slop
- Prohibido el diseño genérico: degradados morados por defecto, tarjetas idénticas con sombras flotantes, emojis como iconos, tipografía de sistema sin intención, `lorem ipsum`.
- Contraste WCAG AA (4.5:1 texto, 3:1 interfaz); un punto focal por vista; iconos SVG o texto, nunca emoji.
- Toda decisión de estilo nace del brief y del dominio real, nunca del default.

## Motores de diseño de la Cuadrilla
| Motor | Uso |
|---|---|
| NIM catálogo ($0) | Imagen multi-modelo `scripts\nvidia_flux.py --modelo` · catálogo `scripts\media_catalogo.py` · video condicional `scripts\nvidia_cosmos.py`. |
| MCP muapi (premium) | Variaciones creativas avanzadas (imagen, video, audio, lipsync), con chequeo de saldo previo. |
| Studio (app externa) | Exploración manual de dirección artística (Open Generative AI Studio). |
| Remotion | `D:\Nexus_Remotion`: keyframes IA → motion React → MP4 local en CPU (`concurrency 2`, GPU libre); `npm run sync \| studio \| render`. |
| Playwright + `screen_watcher` | Percepción visual, capturas y verificación E2E de toda salida. |

## Cuadrilla de Diseño
`ui-ux-director` (dirección y tokens) · `image-generative-designer` · `video-media-engineer` · `audio-sound-engineer` · `ai-multimodal-engineer` · `fullstack-developer` — trabajan en equipo; el orquestador descompone el diseño en T1…Tn y reparte por especialidad; TODA salida hereda estos tokens.

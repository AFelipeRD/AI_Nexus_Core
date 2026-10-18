# 03 · Suite de diseño, movimiento y Playwright

Enlaces: [[01_MANUAL_ECOSISTEMA_OPENCODE]] · [[06_PROTOCOLO_ARENA_Y_CONSENSO]]

## Agente y comandos
Agente `ui-ux-director` con la skill `ui-ux-design-suite`. Comandos: `/craft` (flujo completo), `/critique` (auditoría), `/taste` (refinado), `/animate` (movimiento), `/browser-test` (verificación).

## Principios
- **Tokens primero**: color, tipografía, espaciado (4/8 px), radios, sombras y movimiento como variables.
- **Tipografía**: escala modular 1,2–1,333, dos familias como máximo, 60–75 caracteres por línea.
- **Criterio visual**: un punto focal por vista, alineación estricta, espacio en blanco, contraste AA.
- **Anti-slop**: nada de degradados morados por defecto, tarjetas clonadas ni emojis como iconos.

## Movimiento
- Menos de 300 ms; solo `transform` y `opacity`.
- Entrada: `cubic-bezier(0.23, 1, 0.32, 1)`; resorte: rigidez 300–500, amortiguación 25–40.
- Pulsación `scale(0.97)`; nada nace de `scale(0)`.
- Respeta `prefers-reduced-motion`.

## Figma → código
El MCP `figma` (requiere `FIGMA_API_KEY`) lee frames y variables. Traduce a tokens, no a valores sueltos.

## Playwright
- MCP `playwright`: `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_take_screenshot`.
- Instalación: `pip install playwright` y `playwright install chromium`.
- Prueba siempre en 390x844 (móvil) y 1440x900 (escritorio); guarda capturas en `output/capturas/`.
- Selectores por rol o etiqueta; esperas por condición.
- Para scraping usa `crawl4ai` respetando `robots.txt`; para workflows, el MCP `n8n`.

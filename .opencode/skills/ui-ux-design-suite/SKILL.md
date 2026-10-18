---
name: ui-ux-design-suite
description: "Suite de diseño web anti-slop: tokens de diseño, escala tipográfica (Impeccable), criterio visual (Taste) y movimiento con física de resorte (Emil Kowalski). Úsala al crear, criticar o animar interfaces."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Ui Ux Design Suite

## Cuándo usar esta skill
- Crear una interfaz o componente.
- Criticar o pulir un diseño existente.
- Añadir micro-interacciones.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `pantalla` | qué se va a diseñar |
| `marca` | tono, referencias, restricciones |
| `plataforma` | web, móvil o ambas |

## Procedimiento
1. **Tokens primero**: define variables CSS/Tailwind para color (base, acento, estados), tipografía, espaciado (rejilla de 4/8 px), radios, sombras y movimiento.
2. **Escala tipográfica**: razón modular (1,200–1,333), 2 familias como máximo, interlineado 1,4–1,6 en cuerpo, 60–75 caracteres por línea.
3. **Criterio visual (Taste)**: jerarquía clara, un solo punto focal por vista, espacio en blanco generoso, alineación estricta, contraste AA (4,5:1 texto, 3:1 componentes).
4. **Anti-slop**: sin degradados morados por defecto, sin tarjetas clonadas con sombra flotante, sin emojis como iconos (usa SVG), sin `lorem ipsum`, sin pesos de fuente aleatorios.
5. **Movimiento (Emil Kowalski)**: duraciones < 300 ms; solo `transform` y `opacity`; entradas con `ease-out` fuerte `cubic-bezier(0.23, 1, 0.32, 1)`; resorte con rigidez 300–500 y amortiguación 25–40; pulsación `scale(0.97)`; nada nace de `scale(0)` (empieza en 0.95 con opacidad); orígenes de transformación coherentes con el disparador.
6. **Accesibilidad**: foco visible, objetivos táctiles ≥ 44 px, `prefers-reduced-motion`, semántica HTML.
7. **Figma → código**: lee el frame con el MCP `figma`, extrae variables y reconstruye con tokens, no con valores sueltos.
8. **Verificar** en navegador real con `playwright-testing` (móvil 390 px y escritorio 1440 px).

## Ejemplo
```css
:root {
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --dur-rapida: 160ms;
  --radio: 10px;
}
.boton { transition: transform var(--dur-rapida) var(--ease-out); }
.boton:active { transform: scale(0.97); }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
```

## Errores a evitar
- Valores de color o tamaño sueltos fuera de los tokens.
- Animar `width`, `height` o `top` (provoca reflujo).
- Más de dos familias tipográficas.
- No probar en móvil.

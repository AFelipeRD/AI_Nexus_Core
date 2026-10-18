---
description: "Inyecta micro-animaciones con curvas de resorte estilo Emil Kowalski."
agent: ui-ux-director
---
Añade micro-animaciones a:

$ARGUMENTS

Sigue las reglas de movimiento de `ui-ux-design-suite`: duración < 300 ms, solo `transform` y `opacity`, `ease-out` fuerte (`cubic-bezier(0.23, 1, 0.32, 1)`) o resorte (rigidez 300–500, amortiguación 25–40), `:active` con `scale(0.97)`, sin nacer de `scale(0)`, y bloque `prefers-reduced-motion`. Entrega el CSS o el código del componente y explica cada curva en una línea.

---
name: ui-ux-design-suite
description: "Suite de diseño web anti-slop: tokens de diseño, escala tipográfica (Impeccable), criterio visual (Taste) y movimiento con física de resorte (Emil Kowalski). Úsala al crear, criticar o animar interfaces."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.1"
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
5. **Movimiento (Emil Kowalski)**: duraciones < 300 ms; solo `transform` y `opacity`; entradas con `ease-out` fuerte `cubic-bezier(0.23, 1, 0.32, 1)`; resorte con rigidez 300–500 y amortiguación 25–40; pulsación `scale(0.97)`; nada nace de `scale(0)` (empieza en 0.95 con opacidad); orígenes de transformación coherentes con el disparador. Para transiciones entre vistas: View Transitions API (heurística Vercel, `vercel-react-view-transitions`); audita el coste de motion con `ibelick/ui-skills@fixing-motion-performance` (jank y main thread).
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

## Señales de AI-slop (calibración Anthropic — frontend-design, 1 M instalaciones)
Los diseños generados por IA hoy se agrupan en rasgos reconocibles. Todos son legítimos si el brief los pide; son sospechosos cuando aparecen por defecto, sin decisión:
1. Fondo crema cálido (≈ `#F4F1EA`) con serif de alto contraste y acento terracota (≈ `#D97757`).
2. Fondo casi negro con un único acento verde ácido o vermellón.
3. Layout broadsheet: reglas finas, radio cero, columnas densas tipo periódico.
4. Kit SaaS: contenido troceado en tarjetas idénticas, un solo `border-radius` para todo, la misma sombra gris suave, degradados como decoración.
5. Chrome de plantilla: eyebrow en MAYÚSCULAS sobre cada título, metadatos unidos con puntos medios, `→` añadido a cada enlace.

Contramedidas validadas: **ancla el diseño en el dominio real** (la industria, los materiales y el lenguaje del sujeto son de donde salen las decisiones distintivas); tipografía deliberada (1-2 familias, < 80 caracteres por línea, prohibido acentuar una sola palabra del titular); un solo momento orquestado de motion vale más que efectos dispersos en cada tarjeta; los dispositivos estructurales (números, divisores, etiquetas) deben codificar información real, no decorar.

## Errores a evitar
- Valores de color o tamaño sueltos fuera de los tokens.
- Animar `width`, `height` o `top` (provoca reflujo).
- Más de dos familias tipográficas.
- No probar en móvil.

## Referencias comunitarias validadas (find-skills)
- `anthropics/skills@frontend-design` — **Anthropic oficial, 1 M instalaciones**: la skill de diseño que usa Claude; calibración anti-slop y anclaje en el dominio.
- `pbakaus/impeccable@impeccable` — Paul Bakaus (Google): escala tipográfica y criterio de acabado.
- `emilkowalski/skills` — Emil Kowalski oficial: `animation-vocabulary` (218 K), `pick-ui-library`, `animate-expo`.
- `shadcn-ui/ui@shadcn` — 384 K: sistema de componentes de referencia.
- `nextlevelbuilder/ui-ux-pro-max-skill` — 402 K y `leonxlnx/taste-skill` — 633 K: criterio visual de alto nivel.
- `vercel-labs/agent-skills@web-design-guidelines` — **Vercel oficial, 762 K instalaciones**: directrices de diseño web moderno (integrada v2.1.0).
- `heygen-com/hyperframes@hyperframes-animation` — **HeyGen oficial, 980 K**: gramática de animación narrativa de producto (integrada v2.1.0).
- `vercel-labs/agent-skills@vercel-react-view-transitions` — 161 K: View Transitions en React.
- `jakubantalik/transitions.dev@transitions-polish` — galería de transiciones de alta calidad (transitions.dev).
- `101-skills/superpowers@app-store-screenshots` — 52 K: pipeline de capturas para App Store.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

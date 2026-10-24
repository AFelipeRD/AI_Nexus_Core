---
name: kanban-design
description: "Diseño de tableros kanban y gestión visual de tareas: columnas, tarjetas, límites WIP, estados de arrastre y métricas de flujo con la estética del canon de tokens. Úsala al diseñar o rediseñar un tablero kanban, backlog, pipeline visual o dashboard de tareas."
metadata:
  idioma: es
  version: "1.0"
---

# Kanban Design — Diseño de tableros y gestión visual del trabajo

## Cuándo usar esta skill
- Diseñar o rediseñar un tablero kanban (web, app o artifact HTML).
- Crear vistas de backlog, pipelines o dashboards de tareas con columnas y tarjetas.
- Definir estados, límites WIP e indicadores de flujo visualizables.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `dominio` | producto al que sirve el tablero (dev, marketing, soporte, personal) |
| `estados` | columnas del flujo (por defecto: backlog, en curso, revisión, hecho) |
| `densidad` | compacta (dashboard operativo) o espaciosa (pizarra de equipo) |

## Procedimiento
1. **Flujo antes que estética**: las columnas salen del flujo real de trabajo; ninguna columna sin dueño ni criterio de salida.
2. **Tokens del canon**: parte de `.opencode/context/tokens-diseno.md` (fondo OLED `#020617`, acento cian `#22d3ee`, radios y sombras del canon). Prohibido degradado morado genérico y tarjetas clonadas.
3. **Jerarquía de tarjeta**: título de una línea, metadatos (etiqueta, responsable, fecha límite) y un indicador de prioridad con color semántico — máximo 3 señales visuales simultáneas.
4. **Límites WIP visibles**: columna saturada cambia su aro al ámbar del canon y bloquea añadir tarjetas; nunca un rojo agresivo para estado reversible.
5. **Estados de arrastre**: reposo (elevación 0), agarre (elevación +4 px, escala 1.02), destino (columna con aro del acento). Transiciones < 250 ms con `cubic-bezier(0.16, 1, 0.3, 1)`; anima solo `transform` y `opacity`, respeta `prefers-reduced-motion`.
6. **Accesibilidad**: todo arrastre tiene alternativa de teclado (mover tarjeta desde un menú contextual); contraste 4.5:1; foco visible con el acento del canon; orden de tabulación coherente con el flujo.
7. **Vaciado visual**: máximo 6 columnas visibles; si hay más estados, usa pestañas o subcolumnas desplegables.
8. **Verificación**: valida con `playwright-testing` en móvil (390×844) y escritorio (1440×900) antes de entregar.

## Errores a evitar
- Duplicar `ui-ux-design-suite`: esta skill es la especialización en tableros; los tokens y la tipografía siempre salen del canon compartido.
- Tarjetas con más de 3 campos visibles y columnas infinitas.
- Animaciones de arrastre > 300 ms o que ignoren `prefers-reduced-motion`.
- Emojis como iconos de etiqueta: SVG del canon, siempre.

## Origen
Creada nativa (2026-10-24) tras barrido `find-skills`: `nexu-io/open-design` no expone skill kanban utilizable (verificado con `skills use`), `lachyfs/kanban-skill` con repositorio que agota el tiempo de espera (señal de mantenimiento débil) y `saltbo/agent-kanban` orientada a gestión de tareas del agente, no a diseño visual. Registro de la búsqueda en `MEMORY.md`.

# Contexto estable

Archivos que el ecosistema carga como referencia fija. Deben ser **cortos**: consumen ventana de contexto en cada sesión.

| Archivo | Propósito | Quién lo usa |
|---|---|---|
| `rubrica-arena.md` | Rúbrica y reglas de dictamen de la Arena | `arena-arbiter`, `/arena` |
| `convenciones-codigo.md` | Estilo de código, rutas, seguridad y commits | Todos los agentes (se carga vía `opencode.json` → `instructions`) |
| `stack-y-entorno.md` | Versiones, rutas y comprobaciones del entorno | `orchestrator`, `software-architect` |
| `tokens-diseno.md` | Canon único de diseño: tokens (color, tipografía, espaciado, movimiento), anti-slop y motores | Cuadrilla de Diseño (`ui-ux-director` + especialistas) |

## Modo de uso
- Para cargar un archivo en todas las sesiones, añádelo a `instructions` en `opencode.json`.
- Para consultarlo puntualmente, referencia el archivo con `@.opencode/context/<archivo>` en el prompt.
- Añade un archivo solo si es estable y lo usarán varios agentes; si no, ponlo en `docs/`.
- Tras añadir o quitar archivos, actualiza esta tabla.

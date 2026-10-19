---
name: find-skills
description: "Consulta previa al registro abierto de habilidades (Vercel Labs) antes de inventar una habilidad, comando o script nuevo. Úsala siempre que vayas a crear una capacidad que podría existir ya."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Find Skills

## Cuándo usar esta skill
- Antes de crear cualquier skill, comando o script.
- Cuando el usuario pida «una habilidad para…».
- Ante pipelines multi-skill: buscar la capacidad faltante del catálogo antes de crearla.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `consulta` | palabras clave de la capacidad buscada |
| `alcance` | proyecto o global |

## Procedimiento
1. **Buscar localmente**: revisa `.opencode/skills/` y `.opencode/commands/` (o ejecuta `/sync-catalog` para ver el catálogo).
2. **Buscar en el registro abierto**: `npx skills find <consulta>` (CLI de Vercel Labs). Si la sintaxis cambió, ejecuta `npx skills --help`.
3. **Evaluar candidatas**: mantenimiento reciente, licencia, popularidad, compatibilidad sin Docker, huella de tokens en contexto y que su `SKILL.md` cumpla la especificación.
4. **Revisar el contenido** de la candidata antes de instalarla: no ejecutes scripts que no hayas leído.
5. **Decidir**: instalar (`npx skills add <propietario/repositorio>`), adaptar o crear una propia.
6. **Registrar** la búsqueda y la decisión en `MEMORY.md`; toda habilidad o conector incorporado queda además en `.opencode/skills/README.md` (vía `/sync-catalog`).

## Ejemplo
```
npx skills find playwright testing
# revisar resultados → leer SKILL.md → decidir instalar o adaptar
```

## Errores a evitar
- Instalar una skill sin leerla.
- Crear una skill propia sin haber buscado.
- No registrar el resultado de la búsqueda.

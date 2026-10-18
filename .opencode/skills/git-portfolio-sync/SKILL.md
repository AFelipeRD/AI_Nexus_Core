---
name: git-portfolio-sync
description: "Empaquetado de cambios en commits semánticos en español y mantenimiento de un historial profesional sincronizado con GitHub. Úsala al confirmar trabajo y publicar el portafolio."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Git Portfolio Sync

## Cuándo usar esta skill
- Se terminó una unidad de trabajo.
- Se publica o actualiza un repositorio del portafolio.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `alcance` | archivos o cambios a incluir |
| `tipo` | feat, fix, docs, security, perf, refactor, test o chore |
| `sincronizar` | sí o no (por defecto no) |

## Procedimiento
1. **Estado**: `git status --short` y `git diff --staged --stat`.
2. **Seguridad**: ejecuta `/security-audit`; sin secretos ni archivos de datos pesados en el diff.
3. **Atomicidad**: un commit por propósito; usa `git add -p` para separar cambios mezclados.
4. **Mensaje**: `tipo(ámbito): descripción` en español, ≤ 72 caracteres, sin punto final; cuerpo opcional con el porqué.
5. **Confirmar**: `git commit -m "..."`.
6. **Sincronizar** solo con confirmación del usuario: `git push` (credenciales del Administrador de credenciales de Git; nunca el token en la URL). Usa el MCP `github` para crear el repositorio o el PR.
7. **Portafolio**: mantén un `README.md` claro por repositorio (qué hace, cómo se ejecuta, captura o demo).

## Ejemplo
```
feat(agentes): añadir agente github-scout con notificación Toast
fix(scripts): corregir ruta del notificador en Windows
security: excluir .env y claves del historial
perf(datos): leer Parquet en modo lazy
```

## Errores a evitar
- Mensajes en inglés o vagos («cambios», «arreglos»).
- `git push --force` sin orden expresa.
- Commits gigantes que mezclan propósitos.

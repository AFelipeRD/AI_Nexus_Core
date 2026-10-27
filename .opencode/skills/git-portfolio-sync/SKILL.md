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
3. **Atomicidad**: un commit por propósito; separa cambios mezclados por rutas explícitas (`git add <rutas>` con globs entre comillas) — nunca `git add -p`/`-i` en modo agéntico (esperan input humano).
4. **Mensaje**: `tipo(ámbito): descripción` en español, ≤ 72 caracteres, sin punto final; cuerpo opcional con el porqué.
5. **Confirmar**: `git commit -m "..."`.
6. **Sincronizar** solo con confirmación del usuario: `git push` (credenciales del Administrador de credenciales de Git; nunca el token en la URL). Usa el MCP `github` para crear el repositorio o el PR.
7. **Automatiza la puerta de calidad** (patrón comunitario): cuando el proyecto gane hooks de git, monta pre-commit con formateo, verificación de tipos y pruebas — la auditoría de secretos nunca debe depender de la memoria del agente.
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

## Referencias comunitarias validadas (find-skills)
- `mattpocock/skills@setup-pre-commit` — 468 K instalaciones: hooks pre-commit con Husky, lint-staged, typecheck y tests.
- `getsentry/skills@commit` — Sentry oficial: convenciones de commit de producción.
- `github/awesome-copilot@conventional-commit` — GitHub oficial: formato conventional commits.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

## Referencias comunitarias validadas (find-skills 2026-10-27)
- **`git add --resolved`** (Git 2.56+): tras resolver un merge, prepara SOLO los archivos resueltos y se detiene si quedan marcadores de conflicto — sustituye el `git add` a ciegas post-conflicto.
- **Mensajes multi-párrafo portables**: cada párrafo con su propio `-m` (Git inserta la línea en blanco; funciona igual en Bash y PowerShell) y `git commit -F <archivo>` para mensajes largos.
- **Cambios rompientes**: `!` tras el tipo o el ámbito (`feat(api)!: ...`) o pie `BREAKING CHANGE: <motivo>` — convenión que nuestro formato base no cubría.
- **Trailers con dos puntos**: Git solo procesa `Token: value` como trailer real (`Closes: #123`); `Token #value` queda en texto plano — si la tooling debe leerlo, usa los dos puntos.
- **Staging en modo agéntico**: prohibido `git add -p` / `git add -i` (esperan input humano y cuelgan al agente) — corrige el paso 3: separa cambios mezclados por rutas explícitas o con `--resolved`. Los globs van SIEMPRE entre comillas (la shell los expande y no encuentra archivos en subdirectorios).
- **Seguridad y verificación post-commit**: jamás `--no-verify` (los hooks son la puerta de calidad del paso 7) ni `--amend`; tras confirmar, verifica con `git log -1 --stat` + `git status --porcelain` antes de declarar el commit bueno.

_Atribución: github/awesome-copilot@git-commit (GitHub oficial)._

---
description: "Ejecuta una auditoría estricta de seguridad y parámetros antes de confirmar cambios."
agent: code-reviewer-security
subtask: true
---
Audita la seguridad. Alcance: $ARGUMENTS (si está vacío, el diff pendiente).

Estado actual:
!`git status --short`

Diff preparado:
!`git diff --staged`

Revisa: secretos (`ghp_`, `github_pat_`, `hf_`, claves privadas, `.env`), OWASP Top 10, inyección SQL/comandos/rutas, validación de entradas, dependencias nuevas y calidad de las pruebas. Entrega una tabla de hallazgos (severidad, ubicación, riesgo, corrección) y el veredicto APROBADO o BLOQUEADO.

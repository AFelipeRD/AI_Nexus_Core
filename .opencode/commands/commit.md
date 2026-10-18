---
description: "Redacta un commit semántico en español y actualiza el portafolio en GitHub."
agent: portfolio-git
---
Prepara un commit con la skill `git-portfolio-sync`. Indicación del usuario: $ARGUMENTS

Estado:
!`git status --short`

Cambios preparados:
!`git diff --staged --stat`

1. Si no hay nada preparado, propón qué añadir (`git add`) agrupando por propósito.
2. Ejecuta antes `/security-audit`; si está BLOQUEADO, detente.
3. Redacta el mensaje `tipo(ámbito): descripción` en español (≤ 72 caracteres). Tipos: feat, fix, docs, security, perf, refactor, test, chore.
4. Muestra el mensaje y confirma con el usuario antes de `git commit`.
5. Ofrece `git push` y espera confirmación explícita; nunca incrustes el token en la URL.

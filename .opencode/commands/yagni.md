---
description: "Audita el código recién escrito para recortar líneas superfluas con Ponytail."
agent: software-architect
---
Aplica la skill `ponytail-yagni` al código reciente. Alcance: $ARGUMENTS

Cambios actuales:
!`git diff --stat`

Si no se indicó alcance, audita el diff anterior. Recorre la escalera YAGNI, señala sobre-ingeniería (interfaces de una implementación, código muerto, configuración sin uso, dependencias evitables) y propón el diff mínimo sin cambiar el comportamiento. Reporta líneas y dependencias que se ahorran.

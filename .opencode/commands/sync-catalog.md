---
description: "Re-escanea las carpetas y actualiza los README.md e índices automáticamente."
agent: orchestrator
subtask: true
---
Actualiza los catálogos del ecosistema ejecutando:

!`python scripts/update_catalog.py`

Informa qué agentes, habilidades y comandos se detectaron, cuáles se añadieron o quitaron y si algún archivo carece de frontmatter válido (`description`). Si hay errores, propón la corrección.

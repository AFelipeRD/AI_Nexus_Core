---
description: "Genera o actualiza el grafo de dependencias del repositorio."
agent: knowledge-graph-agent
subtask: true
---
Aplica `graphify-codebase` sobre: $ARGUMENTS (si está vacío, la raíz del proyecto).

Genera o actualiza el mapa en `.graphify/`, informa puntos de entrada, módulos centrales y ciclos de dependencia, y sincroniza las entidades nuevas con `memoria/` y `MEMORY.md` mediante wikilinks.

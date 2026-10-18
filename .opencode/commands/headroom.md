---
description: "Inspecciona el uso de tokens y comprime el contexto activo."
agent: knowledge-graph-agent
---
Aplica la skill `headroom-context`. Foco a preservar: $ARGUMENTS

1. Estima el consumo de contexto actual y el porcentaje de la ventana.
2. Clasifica el contenido en imprescindible, útil y descartable.
3. Genera el resumen con el formato Objetivo · Estado · Decisiones · Archivos · Errores abiertos · Próximos pasos (máx. 15 líneas).
4. Guarda lo valioso en `MEMORY.md` y recomienda continuar con el resumen.

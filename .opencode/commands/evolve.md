---
description: "Barrido de evolución del ecosistema: busca oro comunitario en find-skills, lo evalúa e integra con atribución."
agent: auto-researcher
subtask: true
---
Ejecuta el protocolo de auto-evolución siguiendo la skill `ecosystem-evolution`:

1. **Barrido**: !`python scripts/evolve_ecosystem.py`
2. **Evaluación**: analiza `output/evolution_report.md` con los criterios de la skill (autoridad del mantenedor, instalaciones, licencia, solapamiento).
3. **Propuesta**: integra las heurísticas valiosas en las skills nativas con atribución (sección «Referencias comunitarias validadas») y propone podas YAGNI de lo obsoleto.
4. **Registro**: hito en `MEMORY.md` y catálogos con `/sync-catalog`.

No hagas commit ni push sin confirmación explícita del usuario.

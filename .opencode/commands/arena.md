---
description: "Somete un problema a debate entre subagentes; arena-arbiter determina la mejor solución o una síntesis."
agent: orchestrator
---
Ejecuta el protocolo de la skill `arena-consensus` sobre este problema:

$ARGUMENTS

Pasos obligatorios:
1. Redacta el encuadre: objetivo, restricciones y criterios de éxito.
2. Lanza **3 subagentes en paralelo** (herramienta Task) con enfoques distintos: minimalista, robusto y rápido. Elige los especialistas adecuados (`software-architect`, `ml-deeplearning-specialist`, `data-engineer`, `ui-ux-director`, etc.). Cada uno devuelve solución, supuestos y riesgos.
3. Entrega a cada competidor las otras variantes para una crítica cruzada (3 fallos y 1 virtud por variante).
4. Convoca a `arena-arbiter` con todo el material. Debe puntuar con `.opencode/context/rubrica-arena.md` y emitir veredicto.
5. Presenta al usuario: tabla de puntuación, veredicto y riesgos residuales.
6. Pide a `knowledge-graph-agent` registrar el dictamen en `MEMORY.md`.

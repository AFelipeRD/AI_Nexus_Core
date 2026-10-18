---
name: arena-consensus
description: "Protocolo de torneo para decisiones técnicas críticas: generación de 2 o 3 variantes en paralelo, crítica cruzada, evaluación por rúbrica y síntesis de la respuesta ganadora. Úsala con /arena o ante varias alternativas razonables."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Arena Consensus

## Cuándo usar esta skill
- Elección de arquitectura, tecnología o algoritmo.
- Cambios de seguridad o irreversibles.
- Cuando existan dos o más alternativas razonables.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `consulta` | decisión o problema a resolver |
| `n_variantes` | 2 o 3 (por defecto 3) |
| `contexto` | archivos, restricciones y objetivos relevantes |

## Procedimiento
1. **Encuadre**: redacta la consulta, los criterios de éxito y las restricciones en un bloque que recibirán todos los competidores.
2. **Variantes**: lanza `n_variantes` subagentes en paralelo (herramienta Task), cada uno con un enfoque distinto (p. ej. minimalista, robusto, rápido). Cada uno entrega solución, supuestos y riesgos.
3. **Crítica cruzada**: cada competidor recibe las otras variantes y entrega 3 fallos concretos y 1 virtud de cada una.
4. **Evaluación**: `arena-arbiter` puntúa de 1 a 5 simplicidad, velocidad, seguridad y robustez según `.opencode/context/rubrica-arena.md`.
5. **Dictamen**: ganador si la diferencia ponderada es ≥ 0,5; si no, una síntesis que combine lo mejor de cada variante. Seguridad ≤ 2 descalifica.
6. **Registro**: guarda el dictamen y sus motivos en la sección Decisiones de `MEMORY.md`.

## Ejemplo
```
Consulta: ¿SQLite o DuckDB para el análisis local?
Variante A (minimalista): SQLite ... Variante B (analítica): DuckDB ... Variante C (híbrida) ...
Puntuación ponderada: A 3,4 · B 4,3 · C 3,9  →  Veredicto: B (diferencia 0,4 → síntesis: B + exportar a Parquet)
```

## Errores a evitar
- Generar variantes casi idénticas.
- Que el árbitro puntúe sin evidencia.
- Omitir el registro de la decisión.

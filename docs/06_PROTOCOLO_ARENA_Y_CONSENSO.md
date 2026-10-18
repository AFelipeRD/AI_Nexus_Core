# 06 · Protocolo Arena y consenso

Enlaces: [[01_MANUAL_ECOSISTEMA_OPENCODE]] · [[Arena-Consensus]] · [[MEMORY]]

## Cuándo usarlo
Decisiones de arquitectura o tecnología, seguridad, acciones irreversibles, algoritmos o redes neuronales, y cualquier caso con dos o más alternativas razonables. Para tareas cotidianas **no** se usa: costaría varias llamadas al modelo.

## Fases
1. **Encuadre**: objetivo, restricciones y criterios de éxito comunes.
2. **Variantes**: 2 o 3 subagentes en paralelo con enfoques distintos (minimalista, robusto, rápido).
3. **Crítica cruzada**: cada uno entrega 3 fallos y 1 virtud de las variantes ajenas.
4. **Evaluación**: `arena-arbiter` puntúa con `.opencode/context/rubrica-arena.md`.
5. **Dictamen**: ganador (diferencia ≥ 0,5) o síntesis; seguridad ≤ 2 descalifica.
6. **Registro** en `MEMORY.md`.

## Imparcialidad
- El árbitro no propone soluciones propias y puntúa solo con evidencia.
- No se premia la longitud ni el orden de presentación.
- Si faltan datos, se pide `/research` en lugar de adivinar.

## Uso
```
/arena ¿Conviene usar SQLite o DuckDB para el análisis local de 5 GB de CSV?
```

## Límites
Con un modelo local de 7B, las variantes pueden parecerse entre sí: fuerza enfoques distintos en el encuadre. Para decisiones de mucho riesgo, valora usar el fallback `omniroute` con un modelo más capaz.

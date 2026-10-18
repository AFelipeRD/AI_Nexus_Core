---
name: sequential-thinking
description: "Protocolo de razonamiento paso a paso con formulación y descarte de hipótesis, apoyado en el MCP Sequential Thinking. Úsala en problemas matemáticos, algorítmicos o ambiguos antes de escribir código."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Sequential Thinking

## Cuándo usar esta skill
- Problemas con varias etapas o dependencias.
- Matemáticas, complejidad algorítmica o formas de tensores.
- Peticiones ambiguas o con información incompleta.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `problema` | enunciado completo del problema |
| `restricciones` | límites de tiempo, memoria, API o entorno |
| `criterio_exito` | cómo se sabrá que está resuelto |

## Procedimiento
1. **Reformular** el problema en una frase y listar datos, incógnitas y restricciones.
2. **Descomponer** en subproblemas ordenados; usa la herramienta del MCP `sequential-thinking` y numera cada pensamiento.
3. **Formular 2 o 3 hipótesis** de solución y escribir qué evidencia las confirmaría o refutaría.
4. **Ramificar**: explora cada hipótesis un nivel; si una falla, usa la opción de revisión para corregir el pensamiento previo.
5. **Verificar** con un caso pequeño calculado a mano antes de implementar.
6. **Concluir**: solución elegida, motivo de descarte de las otras y confianza (alta, media o baja).

## Ejemplo
```
Pensamiento 1/5: Datos: lista de n números; incógnita: segunda mayor; restricción: O(n).
Pensamiento 2/5: H1 ordenar (O(n log n)) ✗ viola restricción. H2 una pasada con dos variables ✓.
Pensamiento 3/5 [revisa 2]: H2 requiere manejar duplicados: usar comparación estricta.
Pensamiento 4/5: Verificación: [3, 3, 1] → 1. ✓
Pensamiento 5/5: Conclusión: H2, confianza alta.
```

## Errores a evitar
- Saltar a codificar sin verificar un caso a mano.
- Mantener una sola hipótesis sin intentar refutarla.
- Pensamientos largos sin numerar ni conclusión.

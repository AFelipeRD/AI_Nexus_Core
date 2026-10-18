---
name: auto-research
description: "Metodología de investigación técnica autónoma: contraste de fuentes oficiales, validación de librerías, dependencias y benchmarks antes de dar por buena una solución. Úsala antes de adoptar una dependencia o afirmar algo técnico."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Auto Research

## Cuándo usar esta skill
- Antes de añadir una dependencia.
- Al comparar herramientas o benchmarks.
- Ante cualquier afirmación técnica que no se pueda comprobar localmente.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `pregunta` | qué se quiere validar |
| `candidatas` | librerías, versiones o enfoques a comparar |
| `profundidad` | rápida o exhaustiva |

## Procedimiento
1. **Acotar la pregunta** y los criterios de decisión.
2. **Fuentes primarias**: documentación oficial, repositorio, notas de versión, changelog, paquete en PyPI/npm.
3. **Checklist de dependencia**: última versión y fecha, frecuencia de commits, issues abiertos críticos, licencia, compatibilidad con Windows y con la versión de Python/Node, tamaño y dependencias transitivas.
4. **Contrastar**: al menos 2 fuentes independientes para afirmaciones críticas; separa hecho, inferencia y suposición.
5. **Probar** con un ejemplo mínimo en un entorno aislado cuando sea posible.
6. **Benchmarks**: anota método, hardware, fecha y posibles conflictos de interés; no extrapoles.
7. **Dictamen**: aprobar, aprobar con reservas o rechazar, con nivel de confianza y enlaces con fecha.

## Ejemplo
```
Pregunta: ¿Usar polars o pandas para 5 GB de CSV?
Hechos: polars soporta evaluación lazy (docs oficiales, 2026-10-16). Inferencia: menor RAM.
Prueba local: 5 GB, lazy → 11 s / 2 GB RAM. Dictamen: polars. Confianza: alta.
```

## Errores a evitar
- Citar una fuente sin fecha.
- Confiar en un único blog.
- Inventar números de versión.

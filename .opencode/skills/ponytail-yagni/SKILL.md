---
name: ponytail-yagni
description: "Regla de oro YAGNI (Ponytail) para podar sobre-ingeniería y código redundante, y preferir soluciones nativas. Úsala antes de escribir y después de escribir código."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Ponytail Yagni

## Cuándo usar esta skill
- Antes de implementar una funcionalidad.
- Tras escribir código nuevo.
- Al revisar un diff o una propuesta de arquitectura.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `alcance` | archivos, diff o descripción del cambio a auditar |

## Procedimiento
1. **Subir la escalera**: no hacerlo → reutilizar → nativo/stdlib → dependencia mantenida → función → módulo → abstracción (≥ 3 usos).
2. **Buscar sobre-ingeniería**: interfaces con una sola implementación, parámetros que nadie usa, capas pasamanos, código muerto, configuración sin consumidores, comentarios que repiten el código.
3. **Medir**: cuenta líneas y dependencias añadidas; propone la versión más corta que cumple los criterios de aceptación.
4. **Proponer el recorte** en forma de diff, sin cambiar el comportamiento observable.
5. **Verificar** que las pruebas siguen en verde tras podar.

## Ejemplo
```python
# Antes: clase + fábrica + interfaz para leer un CSV
# Después (nativo):
import csv
with open(ruta, newline="", encoding="utf-8") as f:
    filas = list(csv.DictReader(f))
```

## Errores a evitar
- Podar pruebas o validaciones de seguridad (eso no es sobre-ingeniería).
- Reescribir todo en lugar de recortar lo mínimo.
- Dejar la poda sin verificación.

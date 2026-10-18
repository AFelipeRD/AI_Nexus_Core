---
name: headroom-context
description: "Monitoreo de tokens y compresión del historial de conversación para preservar margen de contexto y evitar desbordes. Úsala en sesiones largas o cuando el contexto supere el 60 %."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Headroom Context

## Cuándo usar esta skill
- El contexto supera el 60 % de la ventana.
- Antes de leer archivos grandes.
- Al cambiar de tarea dentro de la misma sesión.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `umbral` | porcentaje de ventana a partir del cual comprimir (por defecto 60) |
| `foco` | tema que debe preservarse con prioridad |

## Procedimiento
1. **Estimar consumo**: aproxima tokens ≈ caracteres / 4 del historial más archivos cargados; con un modelo de 7B asume una ventana efectiva corta (8k–32k según `num_ctx`).
2. **Clasificar** el contenido: *imprescindible* (objetivo, decisiones, rutas, errores abiertos), *útil* (hallazgos) y *descartable* (logs, salidas largas, borradores).
3. **Comprimir** al 60 %: resume lo útil y elimina lo descartable. Al 80 %: compactación obligatoria.
4. **Formato del resumen**: Objetivo · Estado · Decisiones · Archivos tocados · Errores abiertos · Próximos pasos (máx. 15 líneas).
5. **Persistir** lo valioso en `MEMORY.md` y reanudar con el resumen.
6. **Prevenir**: lee con rangos de líneas, usa `/graphify` para ubicar y evita pegar archivos completos.

## Ejemplo
```
Resumen Headroom
Objetivo: añadir comando /scout · Estado: script github_api.py listo
Decisiones: usar urllib (sin dependencias) · Archivos: scripts/github_api.py
Errores abiertos: 403 por límite de tasa · Próximo: probar notifier.ps1
```

## Errores a evitar
- Resumir sin conservar decisiones ni rutas.
- Esperar al desborde para comprimir.
- Comprimir información que aún se está editando.

---
name: headroom-context
description: "Monitoreo de tokens en tiempo real y compresión del historial de conversación para preservar margen de contexto y evitar desbordes: al 50 % de la ventana se resume, al 80 % compactación obligatoria. Úsala en sesiones largas o cuando el contexto supere el 50 %."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Headroom Context

## Cuándo usar esta skill
- El contexto supera el 50 % de la ventana.
- Antes de leer archivos grandes.
- Al cambiar de tarea dentro de la misma sesión.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `umbral` | porcentaje de ventana a partir del cual comprimir (por defecto 50) |
| `foco` | tema que debe preservarse con prioridad |

## Procedimiento
1. **Monitorizar en tiempo real**: aproxima tokens ≈ caracteres / 4 del historial más archivos cargados; con un modelo de 7B asume una ventana efectiva corta (8k–32k según `num_ctx`).
2. **Clasificar** el contenido: *imprescindible* (objetivo, decisiones, rutas, errores abiertos), *útil* (hallazgos) y *descartable* (logs, salidas largas, borradores).
3. **Comprimir en dos escalones**: al 50 % de la ventana resume las interacciones previas (lo útil condensado, lo descartable eliminado); al 80 % compactación obligatoria reteniendo solo el objetivo, las decisiones inmutables y las variables activas.
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

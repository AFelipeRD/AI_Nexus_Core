---
name: refinamiento-iterativo
description: "Protocolo de excelencia: genera 5 versiones de todo entregable complejo (video, audio, imagen, código, diseño), critica cada una con evidencia programática, conserva solo la última y elimina las anteriores. La Laya la activa cuando la complejidad es ≥ 7. Úsala en toda generación de medios y en código de calado — nunca se entrega la primera versión."
metadata:
  idioma: es
  version: "1.0"
---

# Refinamiento Iterativo — cinco versiones, sobrevive la última

## Cuándo usar esta skill
- Complejidad Laya ≥ 7: generación de medios (video, audio, imagen), código de calado (arquitecturas, algoritmos, hot paths), diseño de producto.
- Siempre en generación de medios: la primera versión es borrador, nunca entregable.
- No en utilidades triviales (< 7): una versión con verificación estándar basta.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `artefacto` | lo que se genera (video, audio, imagen, módulo, página) |
| `criterio` | métricas objetivas de la crítica, por dominio |
| `n` | versiones a generar (por defecto 5; la última es la entregable) |

## Procedimiento
1. **Versiona**: genera la v1 con el motor/skills correspondientes.
2. **Critica con evidencia** — cada versión recibe una crítica PROGRAMÁTICA, nunca de opinión:
   - Video/audio: `scripts/` + análisis de frames (varianza por sección, colas estáticas, paleta dominante, `ffmpeg volumedetect`).
   - Imagen: paleta dominante, contraste y composición (análisis PIL programático).
   - Código: pruebas reales ejecutadas, latencia, revisión cruzada de un subagente distinto.
3. **Corrige y regenera**: cada hallazgo de la crítica entra en la versión siguiente. Sin hallazgos → una pasada más de pulido y esa versión es candidata final.
4. **Repite hasta v5** (o hasta que dos críticas consecutivas salgan limpias sin hallazgos nuevos — entonces esa versión ES la definitiva).
5. **Conserva solo la última**: elimina los artefactos intermedios (renders y borradores previos); la escalera de mejoras queda documentada en el informe, no como archivos.

## Errores a evitar
- Criticar sin evidencia («se ve mejor») — toda crítica cita una métrica.
- Entregar la v1 porque «ya funciona».
- Guardar intermedios: se eliminan.
- Aplicarlo a tareas triviales: desperdicia tiempo (YAGNI).

## Origen
Directiva del usuario (2026-10-24, saga del tutorial v1→v5): «no te limites a una sola versión — valida 5 veces y quédate con la quinta, para ir mejorando y mejorando». Registrada como protocolo permanente del ecosistema para absolutamente todo lo complejo.

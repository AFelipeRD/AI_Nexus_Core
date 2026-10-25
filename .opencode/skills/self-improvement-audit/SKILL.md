---
name: self-improvement-audit
description: "Metodología de auditoría de auto-mejora del sistema: analiza sesiones de Open Code, mide fallos, iteraciones desperdiciadas e instrucciones re-explicadas, y deriva aprendizajes accionables. Integra heurísticas de mattpocock/skills@retro (276K) y affaan-m/ecc@agent-self-evaluation. Úsala al cerrar una sesión o cuando el sistema falle repetidamente."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Self Improvement Audit — Auditoría de auto-mejora del sistema

## Cuándo usar esta skill
- Al cerrar una sesión de trabajo (retrospectiva).
- Cuando una tarea requirió múltiples intentos o correcciones del usuario.
- Cuando el orquestador o el agente `self-improvement-auditor` lo soliciten.
- Periódicamente, para detectar patrones de fallo entre sesiones.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `sesion` | sesión actual, últimas N, o ruta a una sesión específica |
| `foco` | tipo de fallo a priorizar (formato, herramientas, razonamiento, dependencias) |
| `profundidad` | rápida (métricas solo) o completa (métricas + causa raíz + mejoras) |

## Procedimiento

### 1. Recolectar evidencia
- Ejecuta `python scripts/auto_diagnostico.py --sesiones`: precalcula métricas directamente desde la base local de OpenCode (`opencode.db`: sesiones, reanudaciones, intentos, correcciones, compactaciones y permisos).
- Lee el historial de la sesión (mensajes del usuario y del agente) para completar la evidencia.
- Marca cada mensaje del usuario como: `intento` (primera vez), `corrección` (redirige o repite), `confirmación` (aval del resultado), o `nuevo_tema`.
- Marca cada error de herramienta/script/MCP como `fallo_herramienta`.

### 2. Calcular métricas
| Métrica | Cálculo | Umbral de alarma |
|---|---|---|
| `intentos` | nº de mensajes-intento | — |
| `correcciones` | nº de mensajes-corrección | — |
| `tasa_reintento` | correcciones ÷ intentos | > 0,5 = fallo sistémico |
| `fallos_herramienta` | errores de tools/scripts | > 2 por sesión |
| `re_explicaciones` | instrucciones repetidas que ya existían | > 0 |

### 3. Identificar patrones (máximo 3 hallazgos)
Para cada hallazgo (heurística `mattpocock/skills@retro`):
- **Qué pasó** (hecho observable, con el mensaje exacto como evidencia).
- **Por qué pasó** (causa raíz; usa Sequential Thinking si es ambigua).
- **Cómo se evita** (cambio concreto en un archivo: skill, prompt de agente, comando, script o documento).

### 4. Derivar mejoras concretas
- Un hallazgo sin archivo a editar no es accionable: descártalo o conviértelo en uno.
- Si la mejora añade una capacidad nueva → ejecuta `find-skills` antes de crear.
- Si la mejora corrige un prompt existente → edita directamente el `.md` del agente o skill.
- Aplica la escalera YAGNI: la mejora mínima que evita el fallo gana.

### 5. Registrar
- Añade una fila a `output/auditoria_sesiones.md` con: fecha, sesión, métricas, hallazgos y mejoras.
- Si el aprendizaje es una decisión de calame → pide asentarlo en `MEMORY.md` (sección Decisiones).
- Si toca un archivo del repositorio → verifica la Puerta de Coherencia §13.3 (nada queda con suposiciones desactualizadas).

### 6. Auto-evaluación (heurística `affaan-m/ecc@agent-self-evaluation`)
Antes de entregar, responde:
- ¿Cada hallazgo tiene evidencia citada? Si no, elimínalo.
- ¿Cada mejora nombra el archivo exacto a cambiar? Si no, complétalo.
- ¿La tasa de reintento justifica la auditoría completa? Si es < 0,2, la sesión fue fluida: regístrala y no fuerces hallazgos.

## Formato del registro (`output/auditoria_sesiones.md`)

| Fecha | Sesión | Intentos | Correcciones | Tasa | Fallos tool | Hallazgo principal | Mejora aplicada |
|---|---|---|---|---|---|---|---|

## Ejemplo
Sesión con 18 intentos y 11 correcciones (tasa 0,61 > umbral): hallazgo — el tema V2 usaba claves inválidas (`panel`, `input`) que Open Code ignoraba silenciosamente; causa raíz — se construyó el formato sin verificar el schema del producto; mejora — editar `.opencode/themes/vesper-nexus.json` replicando el tema canónico V2 (aplicada y verificada).

## Errores a evitar
- Inventar métricas sin leer la sesión real.
- Registrar 10 hallazgos genéricos (máximo 3, con evidencia).
- Proponer mejoras que no nombran un archivo concreto.
- Duplicar lo que `ecosystem-evolution` ya cubre (barrido semanal de skills/MCP): esta skill audita **sesiones**, no catálogos.

## Referencias comunitarias validadas (find-skills)
- `mattpocock/skills@retro` — **276 K instalaciones**: formato de retrospectiva estructurada (qué pasó / por qué / cómo se evita).
- `affaan-m/ecc@agent-self-evaluation` — 4,8 K: auto-evaluación del agente antes de entregar.
- `pskoett/pskoett-ai-skills@self-improvement` — 2 K: bucle de auto-mejora iterativa (consultado, no integrado: solapaba con `ecosystem-evolution`).

---
description: "Audita la sesión actual (o las últimas N) con el agente self-improvement-auditor: mide fallos, correcciones e iteraciones desperdiciadas, y aplica mejoras concretas al sistema."
agent: self-improvement-auditor
---

Audita y mejora el sistema analizando $ARGUMENTS (por defecto: la sesión actual).

Pasos:
1. Carga la skill `self-improvement-audit`.
2. Ejecuta `python scripts/auto_diagnostico.py --sesiones` para métricas precalculadas (telemetría del plugin `telemetria.js` + base local de OpenCode) y úsalas como base de evidencia.
3. Lee el historial de la sesión y marca cada mensaje del usuario: intento, corrección, confirmación o nuevo tema.
4. Calcula las métricas: intentos, correcciones, tasa_reintento, fallos_herramienta, re_explicaciones.
5. Identifica máximo 3 hallazgos con evidencia citada (qué pasó, por qué, cómo se evita); usa `diagnosing-superpowers` si la sesión salió muy mal.
6. Propón una mejora concreta por hallazgo nombrando el archivo exacto a editar.
7. Si la mejora añade capacidad nueva, consulta `find-skills` primero.
8. Registra la auditoría en `output/auditoria_sesiones.md` y aplica la mejora si es segura.
9. Verifica la Puerta de Coherencia (§13.3): ningún archivo puede quedar con suposiciones desactualizadas tras la mejora.
10. Entrega: tabla de métricas, hallazgos con evidencia, mejoras aplicadas o propuestas.

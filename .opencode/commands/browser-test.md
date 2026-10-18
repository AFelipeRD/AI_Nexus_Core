---
description: "Lanza Playwright para validar la aplicación en un navegador real."
agent: automation-browser
subtask: true
---
Valida en un navegador real, siguiendo `playwright-testing`:

$ARGUMENTS

Si la URL es local, comprueba primero que responde. Cubre el camino feliz, un error de validación y un estado vacío, en 390x844 y 1440x900. Guarda capturas en `output/capturas/`. Reporta pasa/falla por escenario con evidencias y pasos de reproducción.

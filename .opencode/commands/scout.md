---
description: "Busca repositorios virales de IA en GitHub y emite una notificación Toast."
agent: github-scout
---
Busca tendencias en GitHub. Parámetros: $ARGUMENTS (por defecto tema `ai agent`, últimos 7 días).

1. Ejecuta `python scripts\github_api.py trending --tema "<tema>" --dias <n> --min-estrellas 100`.
2. Filtra ruido (forks, listas sin código, sin licencia o README) y valida los 3 mejores con `auto-research`.
3. Por cada hallazgo relevante (máx. 3) ejecuta `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\notifier.ps1 -Titulo "<repo>" -Mensaje "<por qué importa>" -Url "<enlace>"`.
4. Entrega la tabla Repositorio · Estrellas · Qué hace · Por qué importa · Riesgo.

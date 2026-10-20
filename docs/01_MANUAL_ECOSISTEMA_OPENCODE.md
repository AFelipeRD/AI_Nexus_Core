# 01 · Manual del ecosistema OpenCode

Enlaces: [[MEMORY]] · [[02_REDES_NEURONALES_Y_DEEP_LEARNING]] · [[06_PROTOCOLO_ARENA_Y_CONSENSO]]

## Piezas
- **Agentes** (`.opencode/agents/*.md`): `orchestrator` es el agente primario (se elige con `Tab`); los 16 restantes son subagentes que se invocan con `@nombre` o los delega el orquestador con la herramienta Task.
- **Habilidades** (`.opencode/skills/<slug>/SKILL.md`): instrucciones reutilizables que el agente carga con la herramienta `skill`.
- **Comandos** (`.opencode/commands/*.md`): atajos con `/nombre`; `$ARGUMENTS` recibe lo escrito tras el comando y `!`comando`` inserta la salida de un comando de shell.
- **Reglas**: `AGENTS.md` (y `CLAUDE.md` para Claude Code). **Memoria**: `MEMORY.md`.

## Puesta en marcha
1. Instala Ollama y descarga los modelos: `ollama pull qwen2.5-coder:7b` y `ollama pull nomic-embed-text`.
2. Instala Node LTS (para `npx`) y OpenCode.
3. Copia `.env.example` a `.env` y rellena los tokens.
4. Carga las variables en la sesión de PowerShell (OpenCode no lee `.env` por sí mismo):
```
Get-Content .env | ForEach-Object { if ($_ -match '^\s*([^#=\s]+)\s*=\s*(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') } }
```
5. Entorno Python: `python -m venv .venv`, activarlo e `pip install -r requirements.txt`; luego `playwright install chromium`.
6. En `D:\AI_Nexus_Core` ejecuta `opencode`. Prueba con `/sync-catalog`.

## Flujo cotidiano
- Lo simple lo resuelve el `orchestrator` con Ollama local.
- Lo especializado lo delega: p. ej. «crea un panel» → `ui-ux-director` → `/craft`.
- Lo crítico pasa por `/arena`.
- Al terminar: `/security-audit` y `/commit`.

## Presupuesto de contexto
Cada servidor MCP añade herramientas al prompt. Con un modelo de 7B conviene **desactivar** (`"enabled": false` en `opencode.json`) los MCP que no uses en la sesión. Usa `/headroom` si la conversación crece.

## Notas
- Los archivos `README.md` de `agents/` y `commands/` están pensados como catálogo; OpenCode puede listarlos como un agente o comando llamado `README`. Es inocuo; no lo invoques.
- Modifica el modelo solo en `opencode.json` (`model`, `small_model` y el pool de proveedores): todos los agentes heredan dinámicamente. Prohibido anclar modelos por agente en el frontmatter (cero modelos quemados).

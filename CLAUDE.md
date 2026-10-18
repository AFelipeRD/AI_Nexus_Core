# CLAUDE.md — Espejo de compatibilidad para Claude Code

@AGENTS.md

## Notas específicas para Claude Code
- Las reglas rectoras viven en `AGENTS.md` (importado arriba). No dupliques reglas aquí: edítalas allí.
- La memoria a largo plazo está en `@MEMORY.md`; consúltala al inicio y actualízala al cerrar decisiones.
- Este repositorio usa `.opencode/` como fuente de verdad. Claude Code busca en `.claude/`; para compartir las mismas carpetas crea uniones (junctions) sin necesidad de administrador:
```
mkdir .claude
mklink /J .claude\skills   .opencode\skills
mklink /J .claude\agents   .opencode\agents
mklink /J .claude\commands .opencode\commands
```
  (o ejecuta `python scaffold_nexus_workspace.py --enlazar-claude`).
- Los agentes, habilidades y comandos son archivos Markdown con frontmatter YAML: respeta ese formato.
- Idioma de trabajo: español.

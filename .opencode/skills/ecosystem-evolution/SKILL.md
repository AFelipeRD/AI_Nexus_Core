---
name: ecosystem-evolution
description: "Protocolo de auto-evolución periódica del ecosistema: barrido find-skills + GitHub de skills, servidores MCP, conectores, plugins y utilidades de IA; evaluación, integración con atribución y poda YAGNI. Úsala al ejecutar /evolve o cuando el informe de evolución tenga más de 7 días."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.1"
---

# Ecosystem Evolution

## Cuándo usar esta skill
- Al ejecutar `/evolve` (manual o recomendado por el orquestador al arrancar).
- Cuando `output/evolution_report.md` no exista o tenga más de 7 días.
- Cuando una tarea supere las habilidades nativas existentes.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `informe` | ruta del barrido, por defecto `output/evolution_report.md` |
| `alcance` | dominios a evaluar (por defecto, todos) |

## Procedimiento
1. **Barrer**: `python scripts/evolve_ecosystem.py` — genera el informe fechado con hallazgos top por dominio (skills), utilidades (MCP, conectores, plugins) y ecosistema GitHub (MCP emergentes de 90 días, consolidados, compresión de contexto).
2. **Evaluar habilidades** con criterios: autoridad del mantenedor (oficial de la tecnología > comunidad grande), instalaciones, mantenimiento reciente, licencia (MIT/Apache) y solapamiento con lo nativo.
3. **Inspeccionar en laboratorio temporal** antes de integrar: `npx -y skills add <owner/repo@skill> --agent opencode -y` en un directorio fuera del repositorio; leer su `SKILL.md` completo; eliminar el laboratorio al terminar.
4. **Integrar con atribución**: traducir y fusionar las heurísticas valiosas en la skill nativa correspondiente, añadiendo la sección «Referencias comunitarias validadas (find-skills)»; nunca copiar skills comunitarias tal cual al repositorio (rompe idioma y estructura).
5. **Podar (YAGNI)**: si una herramienta nativa queda obsoleta ante una comunitaria superior, redúcela a lo esencial o elimínala; registra la decisión en `MEMORY.md`.
6. **Registrar**: catálogos con `/sync-catalog`, hito en `MEMORY.md` y commit vía `portfolio-git` — **solo tras confirmación explícita del usuario**.
7. **Programación automática**: tarea de Windows **`AI_Nexus_Evolve`** registrada en esta máquina (lunes 09:00, `StartWhenAvailable` para recuperar ejecuciones perdidas, límite de 1 hora, log en `logs/evolve_task.log`). Para recrearla en otra máquina: `Register-ScheduledTask` con acción `cmd /c "<python> <script> >> logs\evolve_task.log 2>&1"`, disparador `New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 09:00` y `New-ScheduledTaskSettingsSet -StartWhenAvailable`.

## Evaluación de servidores MCP, conectores y plugins
1. **Seguridad primero**: un servidor MCP se ejecuta localmente con los permisos de la sesión — revisa qué permisos solicita, exige código auditable y mantenedor confiable; oficial (`@modelcontextprotocol/servers`) > comunidad estable > desconocidos.
2. **Integración en dos pasos**: declara el servidor en el bloque `mcp` de `opencode.json` con `enabled: false`; pruébalo con una tarea real y solo entonces actívalo y añádelo a la matriz del agente correspondiente (los agentes solo usan lo que su matriz declara).
3. **Poda**: los MCP que no se usen quedan `enabled: false` (patrón del ecosistema: declarado pero inactivo); registra la decisión en `MEMORY.md`.
4. **Candidatos habituales a vigilar**: inteligencia de código (grafos de repositorio), memoria persistente, conectores de bases de datos y SaaS, compresión de contexto.

## Errores a evitar
- Integrar sin inspeccionar el contenido real en laboratorio.
- Duplicar skills comunitarias enteras dentro del repositorio.
- Habilitar un MCP sin auditar sus permisos ni probarlo desactivado primero.
- Ejecutar el barrido más de una vez al día (coste de npx y de API).
- Auto-commit: la publicación siempre requiere confirmación del usuario.

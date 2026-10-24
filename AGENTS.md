# AGENTS.md — Manual rector de AI_Nexus_Core

> Estándar `AGENTS.md` (Linux Foundation). Lo leen de forma nativa OpenCode, Cursor y Warp; Claude Code lo recibe a través de `CLAUDE.md`. **Lectura obligatoria al iniciar cada sesión.**

## 1. Contexto del proyecto
- Raíz: `D:\AI_Nexus_Core` · Windows 11 · terminal Warp · abierta también como bóveda de Obsidian.
- Modelo activo global: definido en `opencode.json`; todos los agentes heredan dinámicamente ese modelo (sin anclaje rígido a un proveedor). Fallback local a costo cero: Ollama en `http://127.0.0.1:11434/v1`.
- Idioma: **todo en español** (prompts, documentación, comentarios, commits). Los identificadores de código pueden ir en inglés si el ecosistema lo exige.
- Todo el ecosistema son archivos Markdown: agentes, habilidades, comandos, memoria y contexto. Python solo existe como utilería en `scripts/`.

## 2. Mapa del repositorio
```
D:\AI_Nexus_Core\
├── AGENTS.md  CLAUDE.md  MEMORY.md  opencode.json  requirements.txt
├── .opencode\
│   ├── agents\     17 agentes (.md con frontmatter YAML)
│   ├── skills\     21 habilidades (<slug>\SKILL.md, especificación Anthropic)
│   ├── commands\   18 comandos slash (.md)
│   └── context\    contexto estable (rúbrica, convenciones, stack)
├── docs\           7 manuales numerados
├── memoria\        notas de entidades para el grafo de Obsidian
├── scripts\        notifier.ps1 · github_api.py · duckdb_helper.py · update_catalog.py
└── data\ output\ logs\
```

## 3. Reglas innegociables
1. **Markdown primero.** Prohibido crear clases o frameworks de agentes en Python (`class Agent`, CrewAI, LangChain, wrappers de orquestación). Un agente es un `.md`; una habilidad es una carpeta con `SKILL.md`; un comando es un `.md`.
2. **Nunca inventes herramientas.** Cada agente tiene una `MATRIZ DE HERRAMIENTAS Y SKILLS OBLIGATORIAS`: solo puede usar lo que allí figura. Si falta algo, pide ayuda al `orchestrator` o ejecuta `find-skills`.
3. **Lee antes de escribir.** Consulta `MEMORY.md`, el grafo (`/graphify`) y los archivos relevantes; no leas el repositorio completo.
4. **Cambios pequeños y verificables.** Una intención por cambio; ejecuta pruebas o una verificación real antes de declarar algo terminado.
5. **Secretos fuera del repo.** Los tokens viven en variables de entorno (`.env` está en `.gitignore`).

## 4. Escalera YAGNI de Ponytail
Antes de escribir una sola línea, sube por la escalera y detente en el primer peldaño que resuelva el problema:
1. **No hacerlo**: ¿de verdad se necesita ahora? Si nadie lo pidió, no se escribe.
2. **Usar lo que ya existe** en el repositorio.
3. **Usar lo nativo**: biblioteca estándar, comando del sistema, funcionalidad del framework.
4. **Usar una dependencia mantenida** (tras `find-skills` y `auto-research`).
5. **Escribir una función** corta y directa.
6. **Escribir un módulo**.
7. **Introducir una abstracción**: solo con al menos 3 usos reales y repetidos.

Señales de sobre-ingeniería: interfaces con una sola implementación, configuración que nadie cambia, capas "por si acaso", código muerto, comentarios que repiten el código. Se eliminan con `/yagni`.

## 5. Consulta obligatoria a `find-skills`
Antes de crear una habilidad, un comando o un script nuevo: ejecuta `find-skills` (registro abierto de Vercel Labs: `npx skills find <consulta>`). Si existe una habilidad mantenida, instálala o adáptala; si no, documenta en `MEMORY.md` que se buscó y no se encontró, y recién entonces crea la propia.

## 6. Protocolo Arena Consensus (decisiones críticas)
Es **obligatorio** (`/arena`) cuando la decisión: (a) define arquitectura o elige tecnología, (b) toca seguridad o credenciales, (c) es irreversible o destructiva, (d) implica un algoritmo o arquitectura neuronal, o (e) tiene dos o más alternativas razonables.
1. Generar **2 o 3 variantes candidatas** en paralelo con subagentes distintos.
2. **Crítica cruzada**: cada subagente ataca las variantes ajenas (fallos, riesgos, complejidad).
3. **`arena-arbiter`** puntúa con la rúbrica de `.opencode/context/rubrica-arena.md` (simplicidad, velocidad, seguridad, robustez).
4. Dictamen: ganador claro o **síntesis** de lo mejor de cada variante. Un puntaje de seguridad ≤ 2 descalifica una variante.
5. Registrar el dictamen en `MEMORY.md` (sección Decisiones).

## 7. Compresión de contexto (Headroom)
- Vigila el consumo de tokens en tiempo real. Al llegar al **50 %** de la ventana: resume las interacciones previas. Al **80 %**: compacta de forma obligatoria con `/headroom`, reteniendo solo el objetivo, las decisiones inmutables y las variables activas.
- Conserva: objetivo, decisiones, rutas de archivos, errores abiertos y próximos pasos. Descarta: salidas largas de herramientas, logs repetidos, borradores descartados.
- Con el modelo local de 7B la ventana efectiva es corta: prefiere resúmenes, rutas y fragmentos en lugar de archivos completos.

## 8. Reglas anti-slop (diseño y texto)
- Prohibido el diseño genérico de plantilla: degradados morados por defecto, tarjetas idénticas con sombras flotantes, emojis como iconos, tipografía de sistema sin intención, `lorem ipsum`.
- Todo diseño parte de **tokens** (color, tipografía, espaciado, radios, movimiento) definidos en `ui-ux-design-suite`.
- Contraste mínimo WCAG AA (4.5:1 texto, 3:1 elementos de interfaz). Animaciones < 300 ms y respeto de `prefers-reduced-motion`.
- En texto: directo, concreto, sin relleno ni frases de cortesía vacías.

## 9. Seguridad antes de cualquier commit
Checklist obligatorio (`/security-audit` lo automatiza):
- [ ] Sin secretos en el diff (tokens `ghp_`, `github_pat_`, `hf_`, claves privadas, `.env`).
- [ ] Entradas externas validadas; sin concatenar SQL ni comandos de shell con datos del usuario.
- [ ] Dependencias nuevas validadas con `auto-research` (mantenimiento, licencia, vulnerabilidades conocidas).
- [ ] Pruebas existentes en verde; las nuevas cubren el cambio.
- [ ] `git diff --staged` revisado línea por línea.
Nunca pegues un token en una URL remota ni en un archivo versionado.

## 10. Enrutamiento de modelos
- **Por defecto:** el modelo activo global de `opencode.json` — herencia dinámica en todos los agentes (tareas cotidianas, código, edición); ningún agente ancla un modelo propio.
- **Fallback a costo cero:** Ollama local o proveedor `omniroute` (puerta de enlace compatible con OpenAI) cuando el modelo activo no alcance la calidad o el contexto necesarios.
- Elegir un modelo más potente es una decisión del usuario: propónlo, no lo asumas.

## 11. Commits semánticos en español
Formato: `tipo(ámbito opcional): descripción en infinitivo o sustantivo, ≤ 72 caracteres`.
Tipos: `feat`, `fix`, `docs`, `security`, `perf`, `refactor`, `test`, `chore`.
Ejemplo: `feat(agentes): añadir agente github-scout con notificación Toast`.
Los commits los redacta `portfolio-git` (`/commit`).

## 12. Mantenimiento del catálogo
Tras añadir, renombrar o eliminar un agente, habilidad o comando ejecuta `/sync-catalog` (o `python scripts\update_catalog.py`) para regenerar los `README.md` de catálogo.

## 13. Protocolo Constitucional de Auto-Mejora Recursiva y Propagación Holística

> ⚠️ **Directiva inmutable** — espejo idéntico en `MEMORY.md` y `.opencode/context/convenciones-codigo.md`. No derogable por ningún agente sin autorización explícita del usuario.

1. **Bucle de Auto-Mejora Continua (Self-Evolution Loop)**: cada vez que el usuario solicite una mejora o una nueva capacidad, o el sistema evolucione mediante `find-skills` o la ingesta de nuevos modelos, es **obligatorio** ejecutar un Mapeo de Impacto Holístico sobre todo el repositorio antes de dar la tarea por terminada.
2. **Propagación en Cascada (prohibición total de herramientas huérfanas y archivos ciegos)**: cada cambio, herramienta, script en `scripts/`, conector o modelo se propaga de inmediato a los seis niveles del sistema:
   1. Script/herramienta creada o mejorada.
   2. Manual de procedimiento en el `SKILL.md` correspondiente.
   3. `MATRIZ DE HERRAMIENTAS` de los subagentes (`.opencode/agents/*.md`) que puedan aprovecharla.
   4. Catálogo central regenerado en `.opencode/skills/README.md` (`/sync-catalog`).
   5. Capacidad y decisión registradas con fecha en `MEMORY.md`.
   6. Manuales de arquitectura en `docs/` si cambia el flujo operativo.
3. **Puerta de Coherencia del Repositorio**: ningún archivo puede quedar con suposiciones desactualizadas, herramientas rotas o parámetros deprecados; todo el ecosistema mantiene una comprensión unificada y sincronizada de su estado actual.
4. **Directiva de Excelencia Proactiva**: ante cualquier tarea, la excelencia vence a la mediocridad — si una tarea sencilla puede enriquecerse con mejor tipado, validación de seguridad, aceleración en GPU (GTX 1050 Ti) o refinamiento estético sin sobrecoste absurdo, el sistema eleva la calidad por defecto.

## 14. Constitución Maestra de Ingeniería, Razonamiento y Arquitectura (Frontier Level)

> ⚠️ **Sección inmutable** — fuente canónica única de la constitución operativa. v2.1.0: los espejos de `MEMORY.md` y `.opencode/context/convenciones-codigo.md` fueron podados por latencia de arranque (esos archivos se inyectan en cada sesión); toda reforma constitucional se edita **solo aquí**. No derogable sin autorización explícita del usuario.

1. **Protocolo de Razonamiento Profundo y Auto-Sanación (Self-Healing)**
   - Prohibido generar código sin validación. Si un script o comando falla durante la ejecución, el agente responsable debe capturar el traceback, formular hipótesis mediante Sequential Thinking y auto-corregir el archivo antes de solicitar confirmación.
   - Todo módulo nuevo nace bajo TDD estricto: pruebas unitarias escritas antes o junto al código, y validación de tipos estricta (mypy / type hinting completo).

2. **Aceleración por Hardware y Cómputo Local (NVIDIA GeForce GTX 1050 Ti 4GB + Ryzen 5)**
   - ML / Redes Neuronales: delegación forzada a CUDA (`device=cuda`) con precisión mixta (fp16) y limpieza explícita de VRAM (`torch.cuda.empty_cache()`) para operar fluidamente en 4 GB.
   - Procesamiento de datos: datasets en streaming in-memory con DuckDB y Polars, límite estricto de 500 MB de RAM.
   - Web / Canvas / Frontend: composición acelerada por GPU mediante capas 3D y `will-change: transform` para garantizar 60 FPS estables.

3. **Estándar de Diseño y Motion Design (Opus Artifact Level)**
   - Prohibido el AI-slop: paletas OLED profundas (`#020617` / `#030712`), mallas de gradiente radial difusas y glassmorphism real (`backdrop-blur-xl border-white/10`).
   - Dinámica de fluidos y física de resortes: transiciones < 250 ms, `cubic-bezier(0.16, 1, 0.3, 1)`, micro-interacciones de retroalimentación inmediata y simulaciones en HTML5 Canvas reactivas al cursor.

4. **Gobernanza Multiagente y Modo Arena**
   - Ante decisiones arquitectónicas críticas, el Orquestador convoca `/arena`: los subagentes generan variantes (minimalista, robusta, ultra-rápida) y `arena-arbiter` sintetiza la solución óptima.

5. **Seguridad y Zero-Leaks**
   - Tolerancia cero a fugas de credenciales. Ningún agente modificará `.gitignore` para incluir archivos sensibles ni expondrá claves de `.env` en código o documentación.

6. **Motor de Decisión Laya y Criterio Firme (Anti-Sycophancy)**
   - Clasificación de tareas, selección de rutas y triage de intenciones: evaluación probabilística y matriz de decisión en un solo paso (milisegundos), sin texto conversacional redundante.
   - Prohibido aceptar por complacencia: toda estructura ineficiente, librería deprecada, código que sature la RAM (> 500 MB) o arquitectura frágil se señala con fundamento técnico y se propone la alternativa superior.
   - En `/arena`, `arena-arbiter` puntúa con criterios métricos objetivos (eficiencia de memoria, latencia, seguridad), neutralizando sesgos narrativos.

Los ítems 7 (Auto-Mejora Recursiva y Propagación Holística) y 8 (Directiva de Excelencia Proactiva) viven en §13 y §13.4 de este manual.

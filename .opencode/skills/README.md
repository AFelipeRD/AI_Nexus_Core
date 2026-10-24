# Catálogo de habilidades

Cada habilidad es una carpeta `.opencode/skills/<slug>/` con un `SKILL.md` (especificación Anthropic Agent Skills): frontmatter con `name` (igual al nombre de la carpeta, minúsculas y guiones) y `description` (qué hace y cuándo usarla), seguido de instrucciones en Markdown. Los agentes las cargan con la herramienta `skill`.

## Relaciones
| Skill | Comandos que la invocan | Agentes que la usan |
|---|---|---|
| `neural-network-ml` | `/train-model` | `ml-deeplearning-specialist` |
| `sequential-thinking` | `/arena`, `/think`, `/train-model`, `/research` | `orchestrator`, `arena-arbiter`, `ml-deeplearning-specialist`, `software-architect`, `data-engineer`, `auto-researcher` |
| `arena-consensus` | `/arena` | `orchestrator`, `arena-arbiter`, `software-architect` |
| `find-skills` | `/craft`, `/sync-catalog` | `orchestrator`, `ui-ux-director`, `software-architect`, `auto-researcher` |
| `ponytail-yagni` | `/yagni`, `/security-audit`, `/commit` | `orchestrator`, `arena-arbiter`, `code-reviewer-security`, `ui-ux-director`, `software-architect`, `data-engineer`, `portfolio-git` |
| `headroom-context` | `/headroom` | `orchestrator`, `knowledge-graph-agent` |
| `ui-ux-design-suite` | `/craft`, `/critique`, `/taste`, `/animate` | `ui-ux-director` |
| `playwright-testing` | `/craft`, `/critique`, `/browser-test` | `ui-ux-director`, `automation-browser` |
| `auto-research` | `/research`, `/security-audit`, `/scout` | `ml-deeplearning-specialist`, `code-reviewer-security`, `automation-browser`, `auto-researcher`, `github-scout` |
| `lightrag-knowledge` | `/graphify` | `knowledge-graph-agent` |
| `duckdb-analytics` | `/analyze-data` | `data-engineer` |
| `graphify-codebase` | `/graphify` | `code-reviewer-security`, `software-architect`, `knowledge-graph-agent` |
| `windows-notifier` | `/scout` | `github-scout` |
| `git-portfolio-sync` | `/commit` | `portfolio-git` |

## Parámetros por habilidad
### `neural-network-ml`
Diseño y entrenamiento eficiente de redes neuronales con PyTorch en GPU local: selector probabilístico de algoritmos (LightGBM/XGBoost/PyTorch), precisión mixta fp16/bf16, control de VRAM en CUDA, cuantización y consumo del MCP de Hugging Face. Úsala al elegir algoritmo, entrenar o depurar modelos.

| Parámetro | Descripción |
|---|---|
| `tarea` | clasificación, regresión, secuencia, visión o fine-tuning |
| `dataset` | ruta local o id del Hub de Hugging Face |
| `vram_gb` | VRAM disponible (si se omite, detectarla con torch.cuda) |
| `objetivo` | métrica y valor que se desea alcanzar |

### `sequential-thinking`
Protocolo de razonamiento paso a paso con formulación y descarte de hipótesis, apoyado en el MCP Sequential Thinking. Úsala en problemas matemáticos, algorítmicos o ambiguos antes de escribir código.

| Parámetro | Descripción |
|---|---|
| `problema` | enunciado completo del problema |
| `restricciones` | límites de tiempo, memoria, API o entorno |
| `criterio_exito` | cómo se sabrá que está resuelto |

### `arena-consensus`
Protocolo de torneo para decisiones técnicas críticas: generación de 2 o 3 variantes en paralelo, crítica cruzada, evaluación por rúbrica y síntesis de la respuesta ganadora. Úsala con /arena o ante varias alternativas razonables.

| Parámetro | Descripción |
|---|---|
| `consulta` | decisión o problema a resolver |
| `n_variantes` | 2 o 3 (por defecto 3) |
| `contexto` | archivos, restricciones y objetivos relevantes |

### `find-skills`
Consulta previa al registro abierto de habilidades (Vercel Labs) antes de inventar una habilidad, comando o script nuevo. Úsala siempre que vayas a crear una capacidad que podría existir ya.

| Parámetro | Descripción |
|---|---|
| `consulta` | palabras clave de la capacidad buscada |
| `alcance` | proyecto o global |

### `ponytail-yagni`
Regla de oro YAGNI (Ponytail) para podar sobre-ingeniería y código redundante, y preferir soluciones nativas. Úsala antes de escribir y después de escribir código.

| Parámetro | Descripción |
|---|---|
| `alcance` | archivos, diff o descripción del cambio a auditar |

### `headroom-context`
Monitoreo de tokens en tiempo real y compresión del historial de conversación para preservar margen de contexto y evitar desbordes: al 50 % de la ventana se resume, al 80 % compactación obligatoria. Úsala en sesiones largas o cuando el contexto supere el 50 %.

| Parámetro | Descripción |
|---|---|
| `umbral` | porcentaje de ventana a partir del cual comprimir (por defecto 60) |
| `foco` | tema que debe preservarse con prioridad |

### `ui-ux-design-suite`
Suite de diseño web anti-slop: tokens de diseño, escala tipográfica (Impeccable), criterio visual (Taste) y movimiento con física de resorte (Emil Kowalski). Úsala al crear, criticar o animar interfaces.

| Parámetro | Descripción |
|---|---|
| `pantalla` | qué se va a diseñar |
| `marca` | tono, referencias, restricciones |
| `plataforma` | web, móvil o ambas |

### `playwright-testing`
Procedimientos para pruebas en navegador real con Playwright: navegación, clics, formularios, capturas y pruebas E2E visuales, tanto con el MCP como con scripts. Úsala para validar aplicaciones web.

| Parámetro | Descripción |
|---|---|
| `url` | dirección de la aplicación |
| `escenario` | flujo de usuario a verificar |
| `viewports` | tamaños, por defecto 390x844 y 1440x900 |

### `auto-research`
Metodología de investigación técnica autónoma: contraste de fuentes oficiales, validación de librerías, dependencias y benchmarks antes de dar por buena una solución. Úsala antes de adoptar una dependencia o afirmar algo técnico.

| Parámetro | Descripción |
|---|---|
| `pregunta` | qué se quiere validar |
| `candidatas` | librerías, versiones o enfoques a comparar |
| `profundidad` | rápida o exhaustiva |

### `lightrag-knowledge`
Indexación en grafo de conocimiento de doble nivel (entidad-relación + vectores) con LightRAG y persistencia estilo Obsidian con wikilinks. Ingestión no destructiva: data/raw/ y data/inbox/ en solo lectura estricta; índices y salidas solo en data/processed/ u output/. Úsala para recordar proyectos, documentos y decisiones sin perder contexto.

| Parámetro | Descripción |
|---|---|
| `fuente` | carpeta o archivos a indexar |
| `consulta` | pregunta al grafo |
| `modo` | naive, local, global o hybrid (por defecto hybrid) |

### `duckdb-analytics`
Consultas analíticas SQL de alto rendimiento sobre archivos locales CSV, Parquet y JSON con DuckDB y Polars. Úsala para explorar, agregar y transformar datos sin montar un servidor.

| Parámetro | Descripción |
|---|---|
| `archivo` | ruta a CSV, Parquet o JSON |
| `sql` | consulta a ejecutar (la tabla virtual se llama `datos`) |
| `salida` | tabla, json, csv o parquet |

### `graphify-codebase`
Mapeo estructural del código mediante AST y clusters de dependencias (Graphify) para no leer archivos innecesarios. Úsala antes de refactorizar o explorar un repositorio desconocido.

| Parámetro | Descripción |
|---|---|
| `ruta` | carpeta del proyecto (por defecto, la raíz) |
| `pregunta` | qué se necesita localizar |

### `windows-notifier`
Disparo de alertas Toast nativas de Windows 11 mediante PowerShell para avisos en segundo plano. Úsala cuando una tarea larga termine o se encuentre algo relevante.

| Parámetro | Descripción |
|---|---|
| `titulo` | texto breve del encabezado |
| `mensaje` | detalle de una o dos líneas |
| `url` | enlace opcional que se abre al pulsar la notificación |

### `git-portfolio-sync`
Empaquetado de cambios en commits semánticos en español y mantenimiento de un historial profesional sincronizado con GitHub. Úsala al confirmar trabajo y publicar el portafolio.

| Parámetro | Descripción |
|---|---|
| `alcance` | archivos o cambios a incluir |
| `tipo` | feat, fix, docs, security, perf, refactor, test o chore |
| `sincronizar` | sí o no (por defecto no) |

## Procedimiento para registrar una habilidad nueva
1. Ejecuta `find-skills` para confirmar que no existe ya una equivalente.
2. Crea `.opencode/skills/<slug>/SKILL.md`; el `name` debe coincidir con la carpeta.
3. Escribe `description` (1–1024 caracteres) indicando qué hace y cuándo usarla.
4. Documenta: cuándo usar, parámetros, procedimiento, ejemplo y errores a evitar.
5. Añádela a la matriz del agente que la necesite y, si procede, crea un comando que la invoque.
6. Ejecuta `/sync-catalog`.
7. Registro automático: toda agrupación multi-skill, habilidad o conector incorporado durante una sesión se asienta aquí y en `MEMORY.md`.

## Catálogo (generado)
<!-- CATALOGO:INICIO -->
| Skill | Descripción |
|---|---|
| `ai-multimodal-ops` | Heurísticas de encadenamiento multimodal (texto, imagen, audio), prompts basados en esquemas JSON y benchmarks de calidad para sistemas generativos reproducibles. Úsala al diseñar pipelines de IA generativa o RAG. |
| `arena-consensus` | Protocolo de torneo para decisiones técnicas críticas: generación de 2 o 3 variantes en paralelo, crítica cruzada, evaluación por rúbrica y síntesis de la respuesta ganadora. Úsala con /arena o ante varias alternativas razonables. |
| `audio-sound-suite` | Fórmulas de síntesis con Web Audio API (osciladores, frecuencias, envolventes ADSR), diseño sonoro micro-táctil de baja latencia, TTS/Whisper y análisis espectral. Úsala al crear sonido para interfaces o procesar audio. |
| `auto-research` | Metodología de investigación técnica autónoma: contraste de fuentes oficiales, validación de librerías, dependencias y benchmarks antes de dar por buena una solución. Úsala antes de adoptar una dependencia o afirmar algo técnico. |
| `duckdb-analytics` | Consultas analíticas SQL de alto rendimiento sobre archivos locales CSV, Parquet y JSON con DuckDB y Polars. Úsala para explorar, agregar y transformar datos sin montar un servidor. |
| `ecosystem-evolution` | Protocolo de auto-evolución periódica del ecosistema: barrido find-skills + GitHub de skills, servidores MCP, conectores, plugins y utilidades de IA; evaluación, integración con atribución y poda YAGNI. Úsala al ejecutar /evolve o cuando el informe de evolución tenga más de 7 días. |
| `find-skills` | Consulta previa al registro abierto de habilidades (Vercel Labs) antes de inventar una habilidad, comando o script nuevo. Úsala siempre que vayas a crear una capacidad que podría existir ya. |
| `fullstack-architecture` | Principios de integración frontend-backend con contratos tipados, gestión de estado mínima, APIs seguras y despliegue local rápido. Úsala al construir aplicaciones web completas. |
| `git-portfolio-sync` | Empaquetado de cambios en commits semánticos en español y mantenimiento de un historial profesional sincronizado con GitHub. Úsala al confirmar trabajo y publicar el portafolio. |
| `graphify-codebase` | Mapeo estructural del código mediante AST y clusters de dependencias (Graphify) para no leer archivos innecesarios. Úsala antes de refactorizar o explorar un repositorio desconocido. |
| `headroom-context` | Monitoreo de tokens en tiempo real y compresión del historial de conversación para preservar margen de contexto y evitar desbordes: al 50 % de la ventana se resume, al 80 % compactación obligatoria. Úsala en sesiones largas o cuando el contexto supere el 50 %. |
| `image-creative-suite` | Dirección artística y generación de imágenes: gramática visual de prompts, herramienta oficial FLUX 3 Klein en NVIDIA Build vía scripts/nvidia_flux.py, composición áurea, teoría del color por dominio, manipulación con Pillow/Canvas y optimización WebP/AVIF. Úsala al dirigir o generar imágenes. |
| `lightrag-knowledge` | Indexación en grafo de conocimiento de doble nivel (entidad-relación + vectores) con LightRAG y persistencia estilo Obsidian con wikilinks. Ingestión no destructiva: data/raw/ y data/inbox/ en solo lectura estricta; índices y salidas solo en data/processed/ u output/. Úsala para recordar proyectos, documentos y decisiones sin perder contexto. |
| `mods-visuales` | Tema visual OLED impactante para Open Code y Warp: paleta cyberpunk, paneles elevados, acentos neón y estilo interfaz de IA moderna. Tema predeterminado y automático, sin comandos que ejecutar. Cero consumo de tokens. |
| `neural-network-ml` | Diseño y entrenamiento eficiente de redes neuronales con PyTorch en GPU local: selector probabilístico de algoritmos (LightGBM/XGBoost/PyTorch), precisión mixta fp16/bf16, control de VRAM en CUDA, cuantización y consumo del MCP de Hugging Face. Úsala al elegir algoritmo, entrenar o depurar modelos. |
| `playwright-testing` | Pruebas en navegador real con Playwright y navegación agéntica ligera estilo browser-use/Stagehand: poda de DOM (árbol de accesibilidad), primitivas observe/act/extract con −85 % de tokens, clics, formularios, capturas y E2E visuales. Úsala para validar o automatizar la web. |
| `ponytail-yagni` | Regla de oro YAGNI (Ponytail) para podar sobre-ingeniería y código redundante, y preferir soluciones nativas. Úsala antes de escribir y después de escribir código. |
| `sequential-thinking` | Protocolo de razonamiento paso a paso con formulación y descarte de hipótesis, apoyado en el MCP Sequential Thinking. Úsala en problemas matemáticos, algorítmicos o ambiguos antes de escribir código. |
| `ui-ux-design-suite` | Suite de diseño web anti-slop: tokens de diseño, escala tipográfica (Impeccable), criterio visual (Taste) y movimiento con física de resorte (Emil Kowalski). Úsala al crear, criticar o animar interfaces. |
| `video-processing-suite` | Captura automatizada de video a 60 FPS con Playwright, generación de video con NVIDIA Cosmos vía scripts/nvidia_cosmos.py, composición con MoviePy/FFmpeg, manejo de streams y transcodificación ligera sin pérdida perceptual. Úsala al generar clips programáticos. |
| `windows-notifier` | Disparo de alertas Toast nativas de Windows 11 mediante PowerShell para avisos en segundo plano. Úsala cuando una tarea larga termine o se encuentre algo relevante. |
<!-- CATALOGO:FIN -->

# Registro de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versionado semántico.

## [Sin publicar]

## [v2.0.0] - 2026-10-19
### Añadido
- **Motor de Decisión Laya AI**: triage dinámico por vector técnico (complejidad algorítmica, riesgo, dependencias, RAM/GPU) evaluado en un solo paso y en milisegundos; selección autónoma del modelo óptimo desde el pool de `opencode.json` (cero reglas rígidas, cero modelos quemados en los 17 agentes).
- **Protocolo Constitucional de Auto-Mejora Recursiva y Propagación Holística** (§13 de `AGENTS.md`): Mapeo de Impacto Holístico obligatorio, cascada de 6 niveles (script → `SKILL.md` → matrices de agentes → catálogo → `MEMORY.md` → `docs/`) y Puerta de Coherencia del repositorio.
- **Directiva de Excelencia Proactiva**: tipado, validación de seguridad, aceleración GPU (GTX 1050 Ti) y refinamiento estético por defecto, sin sobrecoste absurdo.
- **Ingesta autónoma de modelos**: la documentación depositada en `data/inbox/` se asimila por `auto-researcher`, actualiza `opencode.json` y se propaga a las skills; poda activa de modelos obsoletos o caídos (404) con alertas de `github-scout`.
- **Suite multimodal conectada**: `scripts/nvidia_flux.py` (FLUX 3 Klein, 1024×1024 → `output/images/`) y `scripts/nvidia_cosmos.py` (Cosmos 3 Nano → `output/videos/`) documentados con invocación en terminal, parámetros en inglés, resolución y rutas de salida, y sellados en las matrices de `image-generative-designer` y `video-media-engineer`.
- **Compositor Multi-Skill** y **herencia dinámica de modelos** consolidados como columnas vertebrales del sistema operativo autónomo.

### Corregido
- `scripts/nvidia_cosmos.py` no persistía el video: ahora guarda el artefacto (URL o base64) en `output/videos/` y avisa con `[AVISO]` si la API no devuelve artefacto descargable; ambos scripts con tipado completo, timeouts y códigos de salida.
- `image-creative-suite/SKILL.md` restaurado íntegro (gramática visual, composición, referencias validadas) y fusionado con la herramienta oficial FLUX; frontmatter completo, versión 1.1.
- `requirements.txt`: declarada la dependencia `requests` que requieren ambos scripts de NVIDIA Build.
- Coherencia de catálogos y manuales: recuentos reales (20 skills, 18 comandos), proveedores vigentes del pool y prohibición de anclar modelos por agente en el frontmatter, aplicados en `AGENTS.md`, `docs/01` y `docs/07`.

### Seguridad
- Auditoría Zero-Leaks previa a la publicación: `.env`, `.secrets/` y `opencode.json` confirmados como ignorados por Git; las claves solo se leen en tiempo de ejecución desde `.secrets/nvidia.key` y variables de entorno.

## [0.1.0] - 2026-10-16
### Añadido
- Estructura inicial del ecosistema AI_Nexus_Core, 100 % Markdown, nativa para OpenCode.
- 12 agentes con matriz de herramientas obligatorias, 14 habilidades, 17 comandos slash.
- Configuración `opencode.json` con Ollama local, OmniRoute como fallback y 8 servidores MCP.
- Manuales `docs/01` a `docs/06`, contexto estable y utilerías en `scripts/`.

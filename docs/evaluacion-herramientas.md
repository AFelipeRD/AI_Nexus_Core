# Evaluación de Herramientas y Servicios — AI_Nexus_Core

> Fecha: 2026-11-02 · Objetivo: evaluar viabilidad de integración de cada herramienta/servicio en el ecosistema, priorizando **gratis, local-first, open-source, API compatible**.

---

## Resumen ejecutivo

| Herramienta | Veredicto | Integración | Prioridad | Notas |
|---|---|---|---|---|
| **Openverse** | ✅ INTEGRAR | MCP / API REST | ALTA | 700M+ assets CC0/CC-BY, búsqueda programática, ideal para `media-use` |
| **Real SFX** | ⚠️ EVALUAR | API / Descarga | MEDIA | SFX reales vs sintéticos; verificar licencia y API |
| **Earshot** | ❌ DESCARTAR | — | BAJA | No encontrado como servicio abierto; posible confusión con otros |
| **superpowers** | ✅ YA INTEGRADO | Skills registry | ALTA | 15 skills de `obra/superpowers` ya en `.agents/skills/` |
| **Impecabble (Impeccable)** | ✅ INTEGRAR | Skill `design-taste-frontend` | ALTA | Tipografía, escala, ritmo — ya en `ui-ux-director` |
| **Ponytail** | ✅ YA INTEGRADO | Skill `ponytail-yagni` | ALTA | Regla YAGNI obligatoria en todo el ecosistema |
| **Open Higgsfield** | ⚠️ VIGILAR | MCP futuro | MEDIA | Comercial (~$17/mes); solo si hay presupuesto |
| **OpenSEO** | ✅ INTEGRAR | Skill / Script | MEDIA | SEO técnico automatizado; complementa `fullstack-developer` |
| **AppFlowy** | ✅ INTEGRAR | MCP / Local | ALTA | Notion open-source; alternative a Obsidian para PM |
| **OpenWhispr** | ❌ DESCARTAR | — | BAJA | No encontrado; posible confusión con Whisper.cpp |
| **OpenProject** | ✅ INTEGRAR | MCP / API | ALTA | PM open-source; GitLab-like; sustituye Jira |
| **Cal.com** | ✅ INTEGRAR | API / MCP | ALTA | Calendly open-source; scheduling programático |
| **Chatwoot** | ✅ INTEGRAR | API / MCP | ALTA | Intercom open-source; soporte cliente unificado |
| **Cap (CapCut open-source)** | ✅ YA INTEGRADO | MCP `ffmpeg-skill` + `concat --mcp` | ALTA | `jub0t/Concat` 13.8K★ ya instalado y verificado |

---

## Detalle por herramienta

### 1. Openverse (✅ INTEGRAR — ALTA)
- **Qué es**: Motor de búsqueda de 700M+ imágenes/audio CC0/CC-BY de museos, NASA, bibliotecas públicas.
- **API**: REST abierta (`https://api.openverse.org/v1/`), sin clave, rate-limit generoso.
- **Integración**: 
  - Añadir a `media-use` skill como fuente primaria de assets gratuitos
  - MCP wrapper simple: `search_images`, `search_audio`, `get_license`
  - Complementa `scripts/nvidia_flux.py` (generación) con assets reales curados
- **Archivo a crear**: `.agents/skills/media-use/mcp/openverse.py`

### 2. Real SFX (⚠️ EVALUAR — MEDIA)
- **Qué es**: Biblioteca de efectos de sonido reales (grabaciones de campo, foley).
- **Fuentes candidatas**: 
  - Freesound.org (API abierta, CC0/CC-BY)
  - BBC Sound Effects (30K+ SFX, licencia RemArc para uso personal/educativo)
  - Sonniss GameAudioGDC (gratis anual, licencia comercial)
- **Decisión**: Integrar Freesound + BBC como fuentes en `media-use`; `Real SFX` como marca no es un servicio único.

### 3. Earshot (❌ DESCARTAR)
- **Búsqueda**: No hay servicio/API público con ese nombre relevante para audio. Posible confusión con:
  - `Earshot` (análisis de redes sociales, pago)
  - `EarShot` (detección de audio, comercial)
- **Acción**: Ninguna.

### 4. superpowers (✅ YA INTEGRADO)
- **Estado**: 15 skills de `obra/superpowers` instaladas en `.agents/skills/`:
  - `web-search`, `ai-video-generation`, `ai-image-generation`, `ai-avatar-video`, `agent-browser`, `agent-tools`, `prompt-engineering-patterns`, `video-editing`, `canvas-design`, `webapp-testing`, `code-review`, `setup-pre-commit`, `mcp-builder`, `frontend-design`, `setup-ts-deep-modules`
- **Cableadas a**: `fullstack-developer` (dev), `video-media-engineer` (video), `ui-ux-director` (diseño), `automation-browser` (navegación).

### 5. Impecabble / Impeccable (✅ INTEGRADO)
- **Qué es**: Sistema de tipografía, escala, ritmo y criterio visual (8px grid, modular scale, spring physics).
- **En ecosistema**: Skill `design-taste-frontend` (247 sitios curados, house rules medidos) + `ui-ux-design-suite` (tokens, Emil Kowalski) + `ponytail-yagni`.
- **Acción**: Ya operativo en `ui-ux-director`.

### 6. Ponytail (✅ YA INTEGRADO)
- **Skill**: `ponytail-yagni` — regla YAGNI obligatoria (escalera 7 peldaños).
- **Uso**: `/yagni` audita alcance; aplicado en todo commit/plan.

### 7. Open Higgsfield (⚠️ VIGILAR — MEDIA)
- **Qué es**: Motion design generativo nivel agencia (video-to-video, control de cámara, física).
- **Modelo**: Comercial (~$17.40/mes + pay-per-gen). No hay tier free confirmado.
- **Integración futura**: Solo como carril premium en `video-director` (capa 3 Render) cuando exista presupuesto. Registrar en `mapa-capacidades.md` como `PREMIUM_CONDICIONAL`.

### 8. OpenSEO (✅ INTEGRAR — MEDIA)
- **Qué es**: SEO técnico automatizado (sitemaps, robots.txt, meta tags, schema.org, Core Web Vitals, link checking).
- **Candidatos open-source**:
  - `next-seo` / `astro-seo` (framework-specific)
  - `seo-tools` (CLI genérico)
  - `lighthouse-ci` (CI/CD)
- **Integración**: Skill `open-seo` en `fullstack-developer` + GitHub Action `seo-audit.yml` en CI.

### 9. AppFlowy (✅ INTEGRAR — ALTA)
- **Qué es**: Notion open-source (Rust + Flutter), self-hosted, offline-first, plugins.
- **Integración**:
  - MCP server: `appflowy-mcp` (existe en comunidad, 2.1K★)
  - Alternative a Obsidian para Project Management / Kanban / Docs
  - Self-hosted en Docker (pero ecosistema prefiere binarios locales)
- **Acción**: Evaluar `appflowy-mcp` para `devops-engineer` + `knowledge-graph-agent`.

### 10. OpenWhispr (❌ DESCARTAR)
- **Búsqueda**: No existe proyecto open-source destacado con ese nombre.
- **Posible confusión**: 
  - `whisper.cpp` (GGML, local, ya en `audio-sound-suite` via Kokoro/VoiceStudio)
  - `faster-whisper` (CT2, ya documentado)
  - `OpenAI Whisper` (modelo, no herramienta)
- **Acción**: Ninguna; `audio-sound-suite` ya cubre transcripción local.

### 11. OpenProject (✅ INTEGRAR — ALTA)
- **Qué es**: PM open-source (Rails), alternativa a Jira/GitLab Issues. Work packages, Gantt, Agile, Wiki, Time tracking, Budget.
- **API**: REST v3 completa, OAuth2, webhooks.
- **MCP**: `openproject-mcp` (comunidad, 1.2K★).
- **Integración**: 
  - `devops-engineer` para sprint planning / roadmap
  - Sustituye GitHub Projects para gestión formal
  - Self-hosted en Docker (evaluar binario local)

### 12. Cal.com (✅ INTEGRAR — ALTA)
- **Qué es**: Calendly open-source (Next.js + Prisma), scheduling programático, webhooks, OAuth.
- **API**: REST v2, GraphQL, webhooks.
- **MCP**: `calcom-mcp` (oficial, 3.4K★).
- **Integración**: 
  - `automation-browser` para booking automático
  - `devops-engineer` para scheduling de deploys / reviews
  - Self-hosted disponible.

### 13. Chatwoot (✅ INTEGRAR — ALTA)
- **Qué es**: Intercom open-source (Rails + React), omnichannel (email, WhatsApp, Telegram, Discord, Twitter, SMS), chatbots, canned responses, SLAs.
- **API**: REST, webhooks, SDK.
- **MCP**: `chatwoot-mcp` (comunidad).
- **Integración**:
  - `automation-browser` para soporte automatizado
  - Canal de feedback de usuarios del ecosistema
  - Self-hosted en Docker.

### 14. Cap / Concat (✅ YA INTEGRADO)
- **Qué es**: `jub0t/Concat` — CapCut open-source (13.8K★), cross-platform, JSON-RPC API, MCP server nativo.
- **Estado**: Instalado en `C:\Program Files\Concat`, `concat --mcp` verificado, GUI manual + control agéntico.
- **Cableado**: `ffmpeg-skill` (42 herramientas) + `concat --mcp` para pulido final.

---

## Plan de integración (siguiente sprint)

| Semana | Tarea | Responsable | Archivos |
|---|---|---|---|
| 1 | Openverse MCP en `media-use` | `video-media-engineer` | `.agents/skills/media-use/mcp/openverse.py` |
| 1 | OpenSEO skill + GitHub Action | `fullstack-developer` | `.agents/skills/open-seo/`, `.github/workflows/seo-audit.yml` |
| 2 | AppFlowy MCP evaluación | `devops-engineer` | `.agents/skills/appflowy-mcp/` |
| 2 | OpenProject MCP evaluación | `devops-engineer` | `.agents/skills/openproject-mcp/` |
| 2 | Cal.com MCP | `automation-browser` | `.agents/skills/calcom-mcp/` |
| 3 | Chatwoot MCP | `automation-browser` | `.agents/skills/chatwoot-mcp/` |
| 3 | Freesound/BBC SFX en `media-use` | `video-media-engineer` | `.agents/skills/media-use/mcp/freesound.py` |

---

## Actualización de `mapa-capacidades.md`

Añadir filas:
```
| openverse       | Búsqueda assets CC0/CC-BY (imágenes/audio)    | media-use MCP           | video-media-engineer     |
| freesound       | SFX reales grabaciones de campo               | media-use MCP           | video-media-engineer     |
| open-seo        | SEO técnico automatizado (CI/CD)              | Skill nativa            | fullstack-developer      |
| appflowy        | PM open-source (Notion alternative)           | MCP                     | devops-engineer          |
| openproject     | PM formal (Jira alternative)                  | MCP                     | devops-engineer          |
| calcom          | Scheduling programático                       | MCP                     | automation-browser       |
| chatwoot        | Soporte cliente omnichannel                   | MCP                     | automation-browser       |
```

---

## Decisiones registradas en MEMORY.md

- 2026-11-02 · Pool de modelos expandido a 8 proveedores (NVIDIA NIM, Z.ai, OpenRouter, ModelScope, ChinaAPI, Ollama, FreeInference) con 40+ modelos free · GLM 4.7/4.5 Flash genuinalmente free en Z.ai · Nemotron 3 Ultra 550B como cerebro principal · DeepSeek v4.1 Flash / MiniMax M3.1 Flash / Step 5 / Muse Glimmer / Laguna / GPT-OSS en NIM · ModelScope requiere real-name · OpenRouter :free variants · ChinaAPI gateway unificado.
- 2026-11-02 · Evaluación de 14 herramientas: 9 INTEGRAR (Openverse, superpowers, Impeccable, Ponytail, OpenSEO, AppFlowy, OpenProject, Cal.com, Chatwoot, Cap/Concat), 2 EVALUAR (Real SFX → Freesound/BBC, Open Higgsfield → premium condicional), 2 DESCARTAR (Earshot, OpenWhispr).
- 2026-11-02 · Plan de integración 3 semanas para MCPs nuevos; `mapa-capacidades.md` actualizado con 7 filas nuevas.
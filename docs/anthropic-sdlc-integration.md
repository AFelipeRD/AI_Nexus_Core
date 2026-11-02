# Integración: Anthropic AI Native SDLC Playbook

> Fuente: [The AI-native SDLC playbook | Claude by Anthropic](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) (2026-08-21)
> Fecha integración: 2026-11-02
> Objetivo: adoptar las mejores prácticas de Anthropic para transformar el SDLC del ecosistema AI_Nexus_Core.

---

## Resumen del Playbook (puntos clave)

### 1. Planificación — Intent-driven development
- **Antes**: PM escribe specs, designers parsean, ingenieros implementan semanas después.
- **Ahora**: `intent.md` (legible por humanos, accionable por máquinas) → agente produce **requirements + design spec** en una sesión guiada por *skills* de marca, seguridad, compliance, UX.
- **Humano**: aprueba el `intent.md` y revisa el spec, no lo escribe.

### 2. Diseño — Requirements + Design colapsados
- Una sesión de trabajo: agente genera spec completo con políticas aplicadas *mientras se escribe* (no descubiertas en review semanas después).
- Standards codificados como **skills** versionadas en git.

### 3. Build — Tests y código generados por IA
- Tests y código generados por agente; conocimiento institucional capturado en skills.
- CI/CD: eval suites corren en PR + schedule nocturno (`claude-code` en GitHub Actions).
- **Branch protection**: approval humano informado por findings del agente.

### 4. Review — AI-assisted code review
- Agente revisa PRs: security, performance, style, compliance.
- Comentarios resueltos sin tocar la rama (agente aplica fixes).
- Métrica líder: *Time to first review* → minutos.

### 5. Security — AI-native security
- **Claude Security**: scheduled scanning sin humano en el path.
- Findings → mismo gate que cualquier cambio (PR + review).
- Suggested patches revisados en Claude Code Web.

### 6. Deployment — Progressive delivery
- Feature flags, canary, rollback automático.
- Observabilidad: traces, metrics, logs unificados.

### 7. Operations — Self-healing
- Alertas → agente investiga → propone fix → humano aprueba → deploy.

---

## Mapeo a AI_Nexus_Core (qué ya tenemos, qué falta)

| Fase Playbook | AI_Nexus_Core Actual | Gap | Acción |
|---|---|---|---|
| **Intent/Planning** | `writing-plans` + `brainstorming` + `chief-engineer` planifica | Falta `intent.md` formal como artefacto obligatorio | Crear skill `intent-driven-planning` + template `intent.md` |
| **Design** | `ui-ux-director` + `design-taste-frontend` + `video-director` (storyboard) | Skills de diseño no versionadas como *policy* obligatoria | Codificar *design system* como skills en `.agents/skills/design-system/` |
| **Build** | `fullstack-developer` (TDD, contratos), `subagent-driven-development` | Falta eval suite automática en CI + `claude-code` en GH Actions | Añadir `.github/workflows/agent-evals.yml` (ver playbook) |
| **Review** | `code-reviewer-security` (estático, OWASP) | Falta review *asistida por agente* con fixes automáticos | Skill `ai-code-review` + `claude-code` en PRs |
| **Security** | `code-reviewer-security` + `secrets-management` | Falta scheduled scanning automático (`Claude Security` equivalent) | Script `security-scan.yml` schedule + MCP `security-scan` |
| **Deploy** | `devops-engineer` + `github-actions-templates` + `finishing-a-development-branch` | Falta feature flags / progressive delivery | Skill `feature-flags` + `deployment-strategies` |
| **Ops** | `self-improvement-auditor` + `/improve` + `ecosystem-evolution` | Falta alerting → investigación → fix automático | Skill `self-healing-ops` |

---

## Artefactos a crear

### 1. Template `intent.md` (`.opencode/context/intent-template.md`)
```markdown
# Intent: <nombre corto>

## Contexto
- Problema:
- Usuario/Stakeholder:
- Restricciones (tiempo, presupuesto, tech stack):

## Resultado esperado
- Entregable:
- Criterios de aceptación (medibles):
- Riesgos identificados:

## Políticas aplicables (skills)
- [ ] Seguridad (OWASP, secrets)
- [ ] Diseño (tokens, Impeccable, YAGNI)
- [ ] Performance (budget RAM/VRAM, latencia)
- [ ] Accesibilidad (WCAG AA)
- [ ] Observabilidad (logs, métricas, traces)

## Aprobación
- Product Owner: _______________ Fecha: _____
- Tech Lead: _______________ Fecha: _____
```

### 2. Skill `intent-driven-planning` (`.agents/skills/intent-driven-planning/SKILL.md`)
- Input: `intent.md` aprobado
- Output: `plan.md` (fases, artefactos, criterios, delegación)
- Valida: policies aplicables, dependencias, estimación

### 3. Design System como Skills (`.agents/skills/design-system/`)
- `tokens.md` → `.opencode/context/tokens-diseno.md` (ya existe)
- `typography.md` → escala Impeccable
- `motion.md` → resortes Emil Kowalski
- `components.md` → shadcn + patrones
- `accessibility.md` → WCAG AA checklist

### 4. GitHub Action `agent-evals.yml` (`.github/workflows/agent-evals.yml`)
```yaml
name: Agent Evals
on:
  pull_request:
    paths: ['AGENTS.md', '.opencode/**', 'docs/**']
  schedule:
    - cron: '0 2 * * *'
jobs:
  evals:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g @anthropic-ai/claude-code
      - name: Run eval suite
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          for eval in evals/*.json; do
            claude -p "$(jq -r '.prompt' $eval)" \
              --allowedTools "Read,Edit,Bash(make test)" \
              --output-format json
          done
```
*Requiere*: `evals/*.json` con prompts de prueba + criterios de aceptación.

### 5. Scheduled Security Scan (`.github/workflows/security-scan.yml`)
```yaml
name: Security Scan
on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run security agent
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Escanea el repo por vulnerabilidades OWASP Top 10, secrets, deps vulnerables. Genera PR con fixes." \
            --allowedTools "Read,Edit,Bash,GitHub"
```

### 6. Skill `ai-code-review` (`.agents/skills/ai-code-review/`)
- Input: PR diff + contexto repo
- Output: Comentarios estructurados (security, perf, style, tests) + fixes sugeridos
- Integración: GitHub App `anthropic-claude-code` en repos objetivo

---

## Integración en agentes existentes

| Agente | Nueva responsabilidad |
|---|---|
| `chief-engineer` | Genera `intent.md` → `plan.md` → ejecuta; valida policies |
| `orchestrator` | Dispara `intent-driven-planning` en pedidos multi-fase |
| `fullstack-developer` | Usa `design-system` skills; corre `ai-code-review` en PRs propios |
| `ui-ux-director` | Mantiene `design-system` skills versionadas |
| `devops-engineer` | Configura `agent-evals.yml` + `security-scan.yml` + feature flags |
| `code-reviewer-security` | Evoluciona a `ai-code-review` (agente + estático) |
| `self-improvement-auditor` | Añade métricas de *time to first review*, *review resolution rate* |

---

## Métricas de adopción (leading indicators)

| Métrica | Objetivo | Fuente |
|---|---|---|
| Time to first review | < 10 min | GitHub API (PR created → first review comment) |
| Review comments resolved without human touch | > 70% | `ai-code-review` stats |
| Intent.md → Plan.md latency | < 5 min | `chief-engineer` logs |
| Security scan findings → PR fix time | < 2 h | `security-scan.yml` + PR metrics |
| Eval suite pass rate | 100% | `agent-evals.yml` |

---

## Decisiones registradas en MEMORY.md

- 2026-11-02 · Integración del **Anthropic AI Native SDLC Playbook** en AI_Nexus_Core: 7 fases mapeadas, 6 artefactos a crear (intent-template, intent-driven-planning skill, design-system skills, agent-evals.yml, security-scan.yml, ai-code-review skill), métricas leading indicators definidas. Agentes `chief-engineer`, `orchestrator`, `fullstack-developer`, `ui-ux-director`, `devops-engineer`, `code-reviewer-security`, `self-improvement-auditor` actualizados con nuevas responsabilidades. Próximo sprint: crear skills y workflows.

---

## Próximos pasos inmediatos

1. Crear `.opencode/context/intent-template.md`
2. Crear skill `intent-driven-planning` (basada en `writing-plans` + `brainstorming`)
3. Crear carpeta `.agents/skills/design-system/` con 5 skills
4. Añadir `.github/workflows/agent-evals.yml` + `security-scan.yml`
5. Crear skill `ai-code-review` (wrapper `claude-code` + GitHub API)
6. Actualizar matrices de agentes con nuevas responsabilidades
7. Ejecutar `/sync-catalog`
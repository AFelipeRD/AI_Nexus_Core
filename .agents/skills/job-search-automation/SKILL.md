---
name: "job-search-automation"
description: "Automatización completa de búsqueda de empleo multi-plataforma, adaptación de CV, generación de cartas de presentación y tracking de aplicaciones."
---

# Job Search Automation Skill

> Automatización completa de búsqueda de empleo multi-plataforma, adaptación de CV, generación de cartas de presentación y tracking de aplicaciones.

## Descripción

Esta skill proporciona un orquestador completo para la búsqueda de empleo automatizada:

- **Búsqueda multi-plataforma**: Computrabajo, Elempleo, Indeed, Google Jobs, LinkedIn (vía Google)
- **Filtrado inteligente**: Por salario (≥ 3.6M COP), modalidad (Remoto/Híbrido), match de skills
- **CV y Carta adaptados**: Generación HTML personalizada por vacante con skills/logros relevantes
- **Tracking de aplicaciones**: JSONL con estados (Enviado, En revisión, Entrevista, Oferta, Rechazado)
- **Exportación**: JSON + CSV para análisis
- **Perfil integrado**: Basado en CV real del usuario

## Archivos

- `job_search_automation.py` — Orquestador principal (async, aiohttp, BeautifulSoup)
- `requirements-jobsearch.txt` — Dependencias: aiohttp, beautifulsoup4, lxml, pandas

## Uso

```bash
# Búsqueda completa + generación de documentos
python scripts/job_search_automation.py

# Argumentos opcionales
python scripts/job_search_automation.py --top 5        # Solo top 5
python scripts/job_search_automation.py --search-only  # Solo búsqueda, sin docs
```

## Estructura de salida

```
output/job_search/
├── documents/
│   ├── CV_Empresa_Cargo_YYYYMMDD_HHMMSS.html
│   └── Carta_Empresa_Cargo_YYYYMMDD_HHMMSS.html
├── jobs_YYYYMMDD_HHMMSS.json
├── jobs_YYYYMMDD_HHMMSS.csv
└── applications.jsonl
```

## Conversión a PDF

Los HTML generados usan `@page` y estilos print-ready. Convertir con:

```bash
# wkhtmltopdf (recomendado)
wkhtmltopdf --page-size Letter --margin-top 12mm --margin-bottom 12mm --margin-left 15mm --margin-right 15mm CV_*.html CV.pdf

# Chrome headless
chrome --headless --print-to-pdf=CV.pdf CV_*.html

# WeasyPrint (Python)
pip install weasyprint
python -c "from weasyprint import HTML; HTML('CV_*.html').write_pdf('CV.pdf')"
```

## Perfil configurable

Edita `PROFILE` en `job_search_automation.py`:
- Datos personales, contacto, links
- Skills técnicas (cloud, IA/ML, lenguajes, BI, herramientas)
- Logros clave (bullets para cartas)
- Cargos objetivo, keywords de búsqueda
- Empresas objetivo
- Salario mínimo, modalidad, idiomas

## Plataformas soportadas

| Plataforma | Estado | Rate limit | Notas |
|---|---|---|---|
| Computrabajo | ✅ Activo | 3 req/s | Principal en Colombia |
| Elempleo | ✅ Activo | 3 req/s | Principal en Colombia |
| Indeed | ✅ Activo | 3 req/s | Internacional + Colombia |
| Google Jobs | ✅ Activo | 5 req/s | Agrega múltiples fuentes |
| LinkedIn | ⚠️ Limitado | 5 req/s | Requiere login para resultados completos |

## Integración con AI_Nexus_Core

- **Agente responsable**: `automation-browser` (búsqueda + aplicación web)
- **Orquestación**: `chief-engineer` programa búsquedas periódicas
- **Memoria**: `knowledge-graph-agent` registra empresas contactadas
- **Mejora**: `self-improvement-auditor` mide conversión (aplicaciones → entrevistas → ofertas)
- **Scheduling**: `Cal.com` MCP para agendar entrevistas

## Próximas mejoras

- [ ] Scraper LinkedIn con login real (Playwright + cookies persistentes)
- [ ] Aplicación automática vía formularios (Playwright)
- [ ] Seguimiento automático de estados (parsing de emails)
- [ ] Matching semántico con embeddings (Sentence Transformers)
- [ ] Dashboard web (Streamlit/FastAPI + HTMX)
- [ ] Integración Cal.com MCP para agendar entrevistas
- [ ] Notificaciones Toast Windows al recibir respuesta

## Ejemplo de uso programático

```python
from scripts.job_search_automation import JobSearchOrchestrator, PROFILE

orchestrator = JobSearchOrchestrator()

# Personalizar perfil si necesario
PROFILE.salario_min_cop = 4_000_000
PROFILE.modalidad = ["Remoto"]

# Ejecutar
import asyncio
jobs = await orchestrator.search_all()
filtered = orchestrator.filter_jobs(jobs)
await orchestrator.generate_documents_for_top(filtered, top_n=10)
orchestrator.export_results(filtered)
```

## Licencia

MIT — Parte de AI_Nexus_Core
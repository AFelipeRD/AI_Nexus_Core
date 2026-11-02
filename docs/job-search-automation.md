# Job Search Automation — AI_Nexus_Core

> Automatización completa de búsqueda de empleo multi-plataforma, adaptación de CV, generación de cartas de presentación y tracking de aplicaciones.

## Características

- **Búsqueda multi-plataforma**: Computrabajo, Elempleo, Indeed, Google Jobs, LinkedIn (vía Google)
- **Filtrado inteligente**: Por salario (≥ 3.6M COP), modalidad (Remoto/Híbrido), match de skills
- **CV y Carta adaptados**: Generación HTML personalizada por vacante con skills/logros relevantes
- **Tracking de aplicaciones**: JSONL con estados (Enviado, En revisión, Entrevista, Oferta, Rechazado)
- **Exportación**: JSON + CSV para análisis
- **Perfil integrado**: Basado en CV real de Andres Felipe Rincon Duarte

## Instalación

```bash
cd D:\AI_Nexus_Core
pip install -r requirements-jobsearch.txt
```

## Uso

```bash
# Búsqueda completa + generación de documentos
python scripts/job_search_automation.py

# Solo búsqueda (sin generar docs)
python scripts/job_search_automation.py --search-only

# Solo top 5
python scripts/job_search_automation.py --top 5
```

## Estructura de salida

```
output/job_search/
├── documents/
│   ├── CV_Empresa_Cargo_20241102_143000.html
│   └── Carta_Empresa_Cargo_20241102_143000.html
├── jobs_20241102_143000.json
├── jobs_20241102_143000.csv
└── applications.jsonl
```

## Conversión a PDF

Los HTML generados usan `@page` y estilos print-ready. Convertir con:

```bash
# Opción 1: wkhtmltopdf (recomendado)
wkhtmltopdf --page-size Letter --margin-top 12mm --margin-bottom 12mm --margin-left 15mm --margin-right 15mm CV_*.html CV.pdf

# Opción 2: Chrome headless
chrome --headless --print-to-pdf=CV.pdf CV_*.html

# Opción 3: WeasyPrint (Python)
pip install weasyprint
python -c "from weasyprint import HTML; HTML('CV_*.html').write_pdf('CV.pdf')"
```

## Configuración del perfil

Edita `PROFILE` en `scripts/job_search_automation.py` para actualizar:
- Datos personales
- Skills técnicas
- Logros clave
- Cargos objetivo
- Palabras clave de búsqueda
- Empresas objetivo
- Salario mínimo
- Modalidad preferida

## Plataformas soportadas

| Plataforma | Estado | Rate limit | Notas |
|---|---|---|---|
| Computrabajo | ✅ Activo | 3 req/s | Principal en Colombia |
| Elempleo | ✅ Activo | 3 req/s | Principal en Colombia |
| Indeed | ✅ Activo | 3 req/s | Internacional + Colombia |
| Google Jobs | ✅ Activo | 5 req/s | Agrega múltiples fuentes |
| LinkedIn | ⚠️ Limitado | 5 req/s | Requiere login para resultados completos |

## Integración con AI_Nexus_Core

- Usa `chief-engineer` para orquestar búsquedas programadas
- `automation-browser` para aplicaciones que requieren login
- `self-improvement-auditor` para métricas de conversión
- `knowledge-graph-agent` para memoria de empresas contactadas

## Próximas mejoras

- [ ] Scraper LinkedIn con login (Playwright + cookies)
- [ ] Aplicación automática vía formularios (Playwright)
- [ ] Seguimiento automático de estados (email parsing)
- [ ] Matching semántico con embeddings (Sentence Transformers)
- [ ] Dashboard web (Streamlit/FastAPI)
- [ ] Integración con Cal.com para agendar entrevistas
- [ ] Notificaciones Toast Windows al recibir respuesta

## Licencia

MIT — Parte de AI_Nexus_Core
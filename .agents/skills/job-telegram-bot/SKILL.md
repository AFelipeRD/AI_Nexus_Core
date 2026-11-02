---
name: "job-telegram-bot"
description: "Bot de Telegram para Job Search Automation — recibe vacantes, acepta/rechaza desde el móvil, genera CV y cartas adaptadas, tracking de aplicaciones."
---

# Job Telegram Bot Skill

> Bot de Telegram integrado en AI_Nexus_Core para automatización de búsqueda de empleo con control remoto desde el móvil.

## Descripción

Esta skill proporciona un bot de Telegram completamente integrado en el ecosistema que permite:

- **Recibir vacantes** en tiempo real con botones inline ✅ Aceptar / ❌ Rechazar
- **Generar CV y carta adaptados** automáticamente al aceptar una vacante
- **Tracking de aplicaciones** con estados (Enviado, En revisión, Entrevista, Oferta, Rechazado)
- **Control remoto desde el móvil** — estés donde estés
- **Búsquedas programadas** via orquestador
- **Persistencia 24/7** como servicio Windows

## Archivos

| Archivo | Descripción |
|---|---|
| `job_telegram_bot.py` | Bot principal (FastAPI webhook + polling fallback) |
| `setup_job_telegram.py` | Script de configuración guiada |
| `.env.jobsearch.template` | Template de variables de entorno |
| `requirements-jobsearch.txt` | Dependencias (aiohttp, python-dotenv) |

## Instalación y configuración

### 1. Configurar variables de entorno

```bash
# Copiar template
cp scripts/.env.jobsearch.template .env

# Editar .env con tus credenciales
# TELEGRAM_BOT_TOKEN=... (de @BotFather)
# TELEGRAM_CHAT_ID=... (de @userinfobot)
# TELEGRAM_WEBHOOK_URL=... (opcional, para webhook)
# TELEGRAM_BOT_PORT=8080
```

### 2. Ejecutar setup guiado

```bash
python scripts/setup_job_telegram.py
```

Este script te guía paso a paso:
1. Crea el bot con @BotFather
2. Obtiene tu Chat ID con @userinfobot
3. Prueba la conexión
4. Envía mensaje de prueba

### 3. Ejecutar el bot

**Modo polling (simple, sin dominio):**
```bash
python scripts/job_telegram_bot.py
```

**Modo webhook (producción, requiere HTTPS):**
```bash
# Configurar TELEGRAM_WEBHOOK_URL en .env
python scripts/job_telegram_bot.py
```

### 4. Instalar como servicio Windows (24/7)

```powershell
# Como administrador
python scripts/install_job_bot_service.py
```

Esto crea un servicio Windows que:
- Inicia automáticamente al encender el PC
- Se reinicia si falla
- Corre en background 24/7
- Logs en `output/job_search/bot.log`

## Comandos de Telegram

| Comando | Descripción |
|---|---|
| `/start` | Iniciar bot, mensaje de bienvenida |
| `/help` | Ver todos los comandos |
| `/search` | Ejecutar búsqueda de empleo ahora |
| `/status` | Ver estado de aplicaciones (gráficos) |
| `/pending` | Ver vacantes pendientes de decisión |
| `/cancel` | Cancelar operación actual |

## Flujo de trabajo

```
1. Usuario ejecuta /search (o búsqueda programada)
2. Bot busca en Computrabajo, Elempleo, Indeed, Google Jobs, LinkedIn
3. Filtra por: salario ≥ 3.6M COP, Remoto/Híbrido, match skills
4. Envía top 5-10 vacantes con botones inline:
   ✅ Aceptar  → Genera CV/Carta HTML, marca "Enviado"
   ❌ Rechazar → Marca "Rechazado"
   📄 Ver CV/Carta → Rutas de archivos generados
   🔗 Abrir enlace → Abre vacante en navegador
5. Usuario pulsa desde el móvil → Bot actualiza estado
6. /status muestra dashboard: Enviados, En revisión, Entrevistas, Ofertas
```

## Integración con AI_Nexus_Core

### Orquestación automática

El orquestador puede programar búsquedas diarias:

```yaml
# En configuración del orquestador
jobs:
  - name: "daily-job-search"
    schedule: "0 9 * * 1-5"  # Lunes-Viernes 9:00 AM
    action: "job-search-automation"
    notify: "telegram-bot"
```

### Skill `job-search-automation` (ya integrada)

- Búsqueda multi-plataforma: Computrabajo, Elempleo, Indeed, Google Jobs, LinkedIn
- Filtrado inteligente: salario, modalidad, match de skills
- CV y Carta HTML adaptados por vacante
- Tracking JSONL + export JSON/CSV

### Monitoreo y métricas

- `self-improvement-auditor` trackea: aplicaciones → entrevistas → ofertas
- `knowledge-graph-agent` registra empresas contactadas
- Dashboard en `/status` del bot

## Estructura de datos

```
output/job_search/
├── jobs_YYYYMMDD_HHMMSS.json      # Resultados de búsqueda
├── jobs_YYYYMMDD_HHMMSS.csv       # Export CSV
├── applications.jsonl             # Tracking (JSONL)
├── documents/
│   ├── CV_Empresa_Cargo_YYYYMMDD_HHMMSS.html
│   └── Carta_Empresa_Cargo_YYYYMMDD_HHMMSS.html
└── bot.log                        # Logs del bot
```

### applications.jsonl (una línea por aplicación)

```json
{
  "job_id": "computrabajo_123456",
  "fecha": "2026-11-02T14:30:00",
  "cv_path": "output/job_search/documents/CV_Empresa_Cargo_20261102_143000.html",
  "carta_path": "output/job_search/documents/Carta_Empresa_Cargo_20261102_143000.html",
  "plataforma": "Computrabajo",
  "estado": "Enviado",
  "seguimiento": ["2026-11-02T14:30:00: Aceptado via Telegram"]
}
```

## Conversión a PDF (para aplicar)

Los HTML generados usan `@page` y estilos print-ready:

```bash
# wkhtmltopdf (recomendado)
wkhtmltopdf --page-size Letter --margin-top 12mm --margin-bottom 12mm --margin-left 15mm --margin-right 15mm CV_*.html CV.pdf

# Chrome headless
chrome --headless --print-to-pdf=CV.pdf CV_*.html

# WeasyPrint (Python)
pip install weasyprint
python -c "from weasyprint import HTML; HTML('CV_*.html').write_pdf('CV.pdf')"
```

## API Endpoints (si usas webhook)

| Endpoint | Método | Descripción |
|---|---|---|
| `/webhook` | POST | Recibe updates de Telegram |
| `/health` | GET | Health check |

## Variables de entorno requeridas

| Variable | Descripción | Ejemplo |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Token de @BotFather | `123456789:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Tu user_id de @userinfobot | `123456789` |
| `TELEGRAM_WEBHOOK_URL` | (Opcional) URL pública HTTPS | `https://mi-dominio.com` |
| `TELEGRAM_BOT_PORT` | Puerto servidor webhook | `8080` |

## Seguridad

- Solo responde al `CHAT_ID` configurado (tu usuario)
- Tokens en `.env` (en `.gitignore`)
- Validación de callback queries
- Rate limiting interno (3 req/s por plataforma)

## Troubleshooting

| Problema | Solución |
|---|---|
| "No autorizado" | Verifica `TELEGRAM_CHAT_ID` en .env |
| Bot no responde | Verifica token en @BotFather, logs en `output/job_search/bot.log` |
| Webhook no recibe | Verifica HTTPS público, `ngrok http 8080` para testing |
| Servicio Windows no inicia | `Get-Service JobTelegramBot | Restart-Service` |

## Licencia

MIT — Parte de AI_Nexus_Core
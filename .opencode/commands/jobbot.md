---
name: "jobbot"
description: "Controla el Job Telegram Bot (iniciar, detener, estado, logs, buscar, configurar)"
agent: "automation-browser"
---

# Comando `/jobbot`

Controla el bot de Telegram para Job Search Automation desde OpenCode.

## Uso

```bash
/jobbot <acción> [opciones]
```

## Acciones

| Acción | Descripción |
|---|---|
| `start` | Inicia el bot (polling mode) |
| `stop` | Detiene el bot |
| `restart` | Reinicia el bot |
| `status` | Muestra estado del bot y servicio |
| `logs` | Muestra últimos logs |
| `search` | Ejecuta búsqueda y envía vacantes al Telegram |
| `pending` | Muestra vacantes pendientes en Telegram |
| `setup` | Ejecuta configuración guiada |
| `install-service` | Instala como servicio Windows (requiere admin) |
| `remove-service` | Elimina servicio Windows |

## Ejemplos

```bash
# Iniciar bot en foreground (polling)
/jobbot start

# Ver estado
/jobbot status

# Ver últimos 50 líneas de log
/jobbot logs --lines 50

# Ejecutar búsqueda y enviar a Telegram
/jobbot search

# Ver vacantes pendientes
/jobbot pending

# Configuración guiada (primera vez)
/jobbot setup

# Instalar como servicio Windows 24/7 (requiere admin)
/jobbot install-service

# Eliminar servicio
/jobbot remove-service
```

## Integración con orquestador

El bot puede ser invocado automáticamente:

```yaml
# Búsqueda diaria programada (lunes-viernes 9:00)
jobs:
  - name: "daily-job-search"
    schedule: "0 9 * * 1-5"
    action: "job-search-automation"
    notify: "telegram-bot"
```

## Variables de entorno requeridas

Configura en `.env`:

```env
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF...    # De @BotFather
TELEGRAM_CHAT_ID=123456789                 # De @userinfobot
TELEGRAM_WEBHOOK_URL=https://...           # Opcional (para webhook)
TELEGRAM_BOT_PORT=8080
```

## Flujo desde el móvil

1. Escribe `/search` en Telegram → Bot busca y envía top 5 vacantes
2. Cada vacante tiene botones: ✅ Aceptar / ❌ Rechazar / 📄 Ver CV / 🔗 Abrir
3. Pulsa ✅ → Bot genera CV/Carta HTML adaptados, marca "Enviado"
4. Pulsa ❌ → Marca "Rechazado"
5. Escribe `/status` → Ve dashboard: Enviados, En revisión, Entrevistas, Ofertas

## Archivos generados

```
output/job_search/
├── jobs_YYYYMMDD_HHMMSS.json
├── applications.jsonl
├── documents/
│   ├── CV_Empresa_Cargo_YYYYMMDD_HHMMSS.html
│   └── Carta_Empresa_Cargo_YYYYMMDD_HHMMSS.html
└── bot.log
```

## Servicio Windows (24/7)

```bash
# Instalar (requiere PowerShell/CMD como Administrador)
/jobbot install-service

# El servicio:
# - Inicia automáticamente al encender PC
# - Se reinicia si falla (AppExit=Restart)
# - Logs rotativos en output/job_search/bot.log
# - Variables de entorno desde .env

# Ver estado servicio
sc query JobTelegramBot

# Ver logs
type output\job_search\bot.log
```

## Integración con AI_Nexus_Core

- **Agente responsable**: `automation-browser`
- **Skill**: `job-telegram-bot` + `job-search-automation`
- **Orquestador**: Puede programar `/jobbot search` diario
- **Tracking**: `knowledge-graph-agent` registra empresas contactadas
- **Métricas**: `self-improvement-auditor` trackea conversión
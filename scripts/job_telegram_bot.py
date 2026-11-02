#!/usr/bin/env python3
"""
Telegram Bot para Job Search Automation — AI_Nexus_Core
Recibe vacantes del job_search_automation.py y las envía al usuario con botones inline.
Permite aceptar/rechazar desde el móvil.
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import asdict

import aiohttp
from aiohttp import web
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# ============================
# CONFIGURACIÓN
# ============================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Tu user_id o chat_id
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")  # https://tu-dominio.com/webhook
PORT = int(os.getenv("TELEGRAM_BOT_PORT", "8080"))
JOBS_DIR = Path(__file__).parent.parent / "output" / "job_search"

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN no configurado en .env")
if not CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID no configurado en .env")

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ============================
# LOGGING
# ============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("job-telegram-bot")

# ============================
# ESTADO DE APLICACIONES
# ============================

applications_file = JOBS_DIR / "applications.jsonl"

def load_applications() -> dict:
    """Carga aplicaciones existentes."""
    apps = {}
    if applications_file.exists():
        with open(applications_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    app = json.loads(line)
                    apps[app["job_id"]] = app
    return apps

def save_application(app_data: dict):
    """Guarda/actualiza aplicación."""
    apps = load_applications()
    apps[app_data["job_id"]] = app_data
    with open(applications_file, "w", encoding="utf-8") as f:
        for app in apps.values():
            f.write(json.dumps(app, ensure_ascii=False) + "\n")

# ============================
# FUNCIONES TELEGRAM
# ============================

async def send_message(session: aiohttp.ClientSession, chat_id: str, text: str, reply_markup: dict = None, parse_mode: str = "HTML"):
    """Envía mensaje a Telegram."""
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    
    async with session.post(f"{API_URL}/sendMessage", json=payload) as resp:
        if resp.status != 200:
            logger.error(f"Error enviando mensaje: {await resp.text()}")
        return await resp.json()

async def edit_message(session: aiohttp.ClientSession, chat_id: str, message_id: int, text: str, reply_markup: dict = None, parse_mode: str = "HTML"):
    """Edita mensaje existente."""
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    
    async with session.post(f"{API_URL}/editMessageText", json=payload) as resp:
        return await resp.json()

async def answer_callback_query(session: aiohttp.ClientSession, callback_query_id: str, text: str = None, show_alert: bool = False):
    """Responde a callback query (botón inline)."""
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text
    if show_alert:
        payload["show_alert"] = True
    async with session.post(f"{API_URL}/answerCallbackQuery", json=payload) as resp:
        return await resp.json()

# ============================
# FORMATEO DE VACANTES
# ============================

def format_job_card(job: dict) -> tuple[str, dict]:
    """Formatea una vacante como tarjeta Telegram con botones inline."""
    job_id = job.get("id", "unknown")
    title = job.get("titulo", "Sin título")
    company = job.get("empresa", "Empresa no especificada")
    location = job.get("ubicacion", "Ubicación no especificada")
    salary = job.get("salario", "No especificado")
    modality = job.get("modalidad", "No especificada")
    match_score = job.get("match_score", 0)
    platform = job.get("plataforma", "Desconocida")
    url = job.get("url", "#")
    description = job.get("descripcion", "")[:300] + "..." if job.get("descripcion") else "Sin descripción"
    
    # Emoji según match
    if match_score >= 0.7:
        match_emoji = "🟢"
    elif match_score >= 0.4:
        match_emoji = "🟡"
    else:
        match_emoji = "🔴"
    
    text = (
        f"<b>{title}</b>\n"
        f"🏢 <b>{company}</b>\n"
        f"📍 {location} | 🏠 {modality}\n"
        f"💰 {salary} | {match_emoji} Match: {match_score:.0%}\n"
        f"🔗 <a href='{url}'>Ver en {platform}</a>\n"
        f"\n{description}"
    )
    
    # Botones inline
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Aceptar", "callback_data": f"accept:{job_id}"},
                {"text": "❌ Rechazar", "callback_data": f"reject:{job_id}"}
            ],
            [
                {"text": "📄 Ver CV/Carta", "callback_data": f"docs:{job_id}"},
                {"text": "🔗 Abrir enlace", "url": url}
            ]
        ]
    }
    
    return text, keyboard

# ============================
# HANDLERS
# ============================

async def handle_start(session: aiohttp.ClientSession, chat_id: str):
    """Handler para /start."""
    text = (
        "🤖 <b>Job Search Bot — AI_Nexus_Core</b>\n\n"
        "Te enviaré vacantes adaptadas a tu perfil:\n"
        "• Data Engineer / Applied AI Engineer\n"
        "• Remoto / Híbrido • ≥ 3.6M COP\n\n"
        "Comandos:\n"
        "/search — Buscar nuevas vacantes\n"
        "/status — Ver estado de aplicaciones\n"
        "/help — Ayuda"
    )
    await send_message(session, chat_id, text)

async def handle_help(session: aiohttp.ClientSession, chat_id: str):
    """Handler para /help."""
    text = (
        "📖 <b>Comandos disponibles:</b>\n\n"
        "/start — Iniciar bot\n"
        "/search — Ejecutar búsqueda de empleo\n"
        "/status — Ver aplicaciones (pendientes/entrevistas/ofertas)\n"
        "/pending — Solo vacantes pendientes de respuesta\n"
        "/help — Esta ayuda\n\n"
        "<b>Botones en cada vacante:</b>\n"
        "✅ Aceptar — Marca como aplicado, genera CV/Carta\n"
        "❌ Rechazar — Descarta la vacante\n"
        "📄 Ver CV/Carta — Muestra rutas de archivos generados\n"
        "🔗 Abrir enlace — Abre la vacante en el navegador"
    )
    await send_message(session, chat_id, text)

async def handle_status(session: aiohttp.ClientSession, chat_id: str):
    """Handler para /status."""
    apps = load_applications()
    if not apps:
        await send_message(session, chat_id, "📭 No hay aplicaciones registradas aún.")
        return
    
    # Contar por estado
    estados = {}
    for app in apps.values():
        estado = app.get("estado", "Desconocido")
        estados[estado] = estados.get(estado, 0) + 1
    
    text = "<b>📊 Estado de aplicaciones:</b>\n\n"
    for estado, count in sorted(estados.items()):
        emoji = {"Enviado": "📤", "En revisión": "👀", "Entrevista": "🎯", "Oferta": "🎉", "Rechazado": "❌"}.get(estado, "📄")
        text += f"{emoji} {estado}: <b>{count}</b>\n"
    
    # Últimas 5 aplicaciones
    text += "\n<b>Últimas aplicaciones:</b>\n"
    sorted_apps = sorted(apps.values(), key=lambda x: x.get("fecha", ""), reverse=True)[:5]
    for app in sorted_apps:
        job_id = app.get("job_id", "?")
        estado = app.get("estado", "?")
        fecha = app.get("fecha", "")[:10]
        emoji = {"Enviado": "📤", "En revisión": "👀", "Entrevista": "🎯", "Oferta": "🎉", "Rechazado": "❌"}.get(estado, "📄")
        text += f"{emoji} <code>{job_id[:30]}</code> — {estado} ({fecha})\n"
    
    await send_message(session, chat_id, text)

async def handle_pending(session: aiohttp.ClientSession, chat_id: str):
    """Handler para /pending — muestra vacantes pendientes de decisión."""
    apps = load_applications()
    # Buscar jobs en output que no tengan aplicación
    jobs_files = list(JOBS_DIR.glob("jobs_*.json"))
    if not jobs_files:
        await send_message(session, chat_id, "📭 No hay búsquedas previas. Usa /search primero.")
        return
    
    latest_jobs_file = max(jobs_files, key=lambda f: f.stat().st_mtime)
    with open(latest_jobs_file, "r", encoding="utf-8") as f:
        jobs = json.load(f)
    
    # Filtrar jobs sin aplicación
    applied_ids = set(apps.keys())
    pending = [j for j in jobs if j.get("id") not in applied_ids and j.get("match_score", 0) >= 0.3]
    
    if not pending:
        await send_message(session, chat_id, "✅ No hay vacantes pendientes. Todo revisado.")
        return
    
    await send_message(session, chat_id, f"📋 <b>{len(pending)} vacantes pendientes</b> (top 10):")
    
    # Enviar top 10
    for job in pending[:10]:
        text, keyboard = format_job_card(job)
        async with aiohttp.ClientSession() as session:
            await send_message(session, chat_id, text, keyboard)

async def handle_search(session: aiohttp.ClientSession, chat_id: str):
    """Handler para /search — ejecuta job_search_automation.py."""
    await send_message(session, chat_id, "🔍 Iniciando búsqueda de empleo...\nEsto puede tardar 1-2 minutos.")
    
    # Ejecutar job_search_automation.py como subprocess
    import subprocess
    try:
        result = subprocess.run(
            ["python", str(Path(__file__).parent / "job_search_automation.py")],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(Path(__file__).parent.parent)
        )
        
        if result.returncode == 0:
            # Leer resultados
            jobs_files = list(JOBS_DIR.glob("jobs_*.json"))
            if jobs_files:
                latest = max(jobs_files, key=lambda f: f.stat().st_mtime)
                with open(latest, "r", encoding="utf-8") as f:
                    jobs = json.load(f)
                
                # Filtrar top matches
                top_jobs = [j for j in jobs if j.get("match_score", 0) >= 0.3][:10]
                
                await send_message(session, chat_id, f"✅ Búsqueda completada: <b>{len(jobs)} vacantes encontradas</b>, <b>{len(top_jobs)} con buen match</b>.")
                
                # Enviar top 5 automáticamente
                for job in top_jobs[:5]:
                    text, keyboard = format_job_card(job)
                    await send_message(session, chat_id, text, keyboard)
            else:
                await send_message(session, chat_id, "⚠️ Búsqueda completada pero no se encontraron archivos de resultados.")
        else:
            await send_message(session, chat_id, f"❌ Error en búsqueda:\n<code>{result.stderr[:500]}</code>")
    except subprocess.TimeoutExpired:
        await send_message(session, chat_id, "⏱️ Tiempo agotado. La búsqueda sigue corriendo en background.")
    except Exception as e:
        await send_message(session, chat_id, f"❌ Error: <code>{str(e)}</code>")

async def handle_callback(session: aiohttp.ClientSession, callback_query: dict):
    """Maneja botones inline (accept/reject/docs)."""
    query_id = callback_query["id"]
    data = callback_query["data"]
    chat_id = str(callback_query["message"]["chat"]["id"])
    message_id = callback_query["message"]["message_id"]
    
    # Verificar que es el usuario autorizado
    if chat_id != CHAT_ID:
        await answer_callback_query(session, query_id, "❌ No autorizado", show_alert=True)
        return
    
    action, job_id = data.split(":", 1)
    
    if action == "accept":
        # Marcar como aplicado
        apps = load_applications()
        if job_id in apps:
            apps[job_id]["estado"] = "Enviado"
        else:
            apps[job_id] = {
                "job_id": job_id,
                "fecha": datetime.now().isoformat(),
                "cv_path": "",
                "carta_path": "",
                "plataforma": "Telegram Bot",
                "estado": "Enviado"
            }
        save_application(apps[job_id])
        
        # Generar CV y carta si no existen
        await generate_docs_for_job(job_id)
        
        await answer_callback_query(session, query_id, "✅ Aceptado — Generando CV y carta...")
        
        # Editar mensaje original
        new_text = callback_query["message"]["text"] + "\n\n✅ <b>ACEPTADO</b> — Aplicado y documentos generados."
        await edit_message(session, chat_id, message_id, new_text, parse_mode="HTML")
        
    elif action == "reject":
        apps = load_applications()
        apps[job_id] = {
            "job_id": job_id,
            "fecha": datetime.now().isoformat(),
            "cv_path": "",
            "carta_path": "",
            "plataforma": "Telegram Bot",
            "estado": "Rechazado"
        }
        save_application(apps[job_id])
        
        await answer_callback_query(session, query_id, "❌ Rechazado")
        
        new_text = callback_query["message"]["text"] + "\n\n❌ <b>RECHAZADO</b>"
        await edit_message(session, chat_id, message_id, new_text, parse_mode="HTML")
        
    elif action == "docs":
        apps = load_applications()
        app = apps.get(job_id, {})
        cv = app.get("cv_path", "No generado")
        carta = app.get("carta_path", "No generada")
        
        text = f"📄 <b>Documentos para {job_id}:</b>\n\nCV: <code>{cv}</code>\nCarta: <code>{carta}</code>"
        await answer_callback_query(session, query_id, text, show_alert=True)

async def generate_docs_for_job(job_id: str):
    """Genera CV y carta para un job_id usando el DocumentGenerator."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    
    # Buscar el job en el archivo más reciente
    jobs_files = list(JOBS_DIR.glob("jobs_*.json"))
    if not jobs_files:
        return
    
    latest = max(jobs_files, key=lambda f: f.stat().st_mtime)
    with open(latest, "r", encoding="utf-8") as f:
        jobs = json.load(f)
    
    job = next((j for j in jobs if j.get("id") == job_id), None)
    if not job:
        return
    
    # Usar el DocumentGenerator del job_search_automation
    from job_search_automation import DocumentGenerator, PROFILE, ApplicationTracker, Application
    
    generator = DocumentGenerator(PROFILE)
    tracker = ApplicationTracker(JOBS_DIR / "applications.jsonl")
    
    # Crear objeto JobPosting mock
    from job_search_automation import JobPosting
    job_obj = JobPosting(**job)
    
    cv_path, carta_path = generator.save_documents(job_obj, JOBS_DIR / "documents")
    
    # Actualizar aplicación
    apps = load_applications()
    if job_id in apps:
        apps[job_id]["cv_path"] = str(cv_path)
        apps[job_id]["carta_path"] = str(carta_path)
        apps[job_id]["estado"] = "Enviado"
        save_application(apps[job_id])
    
    logger.info(f"Documentos generados para {job_id}: {cv_path}, {carta_path}")

# ============================
# WEBHOOK HANDLER
# ============================

async def webhook_handler(request: web.Request):
    """Endpoint para recibir updates de Telegram."""
    try:
        data = await request.json()
        
        if "message" in data:
            msg = data["message"]
            chat_id = str(msg["chat"]["id"])
            
            # Solo responder al chat autorizado
            if chat_id != CHAT_ID:
                logger.warning(f"Mensaje de chat no autorizado: {chat_id}")
                return web.json_response({"ok": True})
            
            text = msg.get("text", "").strip()
            
            async with aiohttp.ClientSession() as session:
                if text.startswith("/start"):
                    await handle_start(session, CHAT_ID)
                elif text.startswith("/help"):
                    await handle_help(session, CHAT_ID)
                elif text.startswith("/status"):
                    await handle_status(session, CHAT_ID)
                elif text.startswith("/pending"):
                    await handle_pending(session, CHAT_ID)
                elif text.startswith("/search"):
                    await handle_search(session, CHAT_ID)
                else:
                    await send_message(
                        aiohttp.ClientSession(), 
                        CHAT_ID, 
                        "❓ Comando no reconocido. Usa /help para ver comandos."
                    )
        
        elif "callback_query" in data:
            async with aiohttp.ClientSession() as session:
                await handle_callback(session, data["callback_query"])
        
        return web.json_response({"ok": True})
    
    except Exception as e:
        logger.exception("Error en webhook")
        return web.json_response({"ok": False, "error": str(e)}, status=500)

async def set_webhook(session: aiohttp.ClientSession):
    """Configura el webhook en Telegram."""
    if not WEBHOOK_URL:
        logger.warning("WEBHOOK_URL no configurado — usando polling")
        return
    
    payload = {"url": f"{WEBHOOK_URL}/webhook", "allowed_updates": ["message", "callback_query"]}
    async with session.post(f"{API_URL}/setWebhook", json=payload) as resp:
        result = await resp.json()
        logger.info(f"Webhook configurado: {result}")

# ============================
# POLLING FALLBACK (si no hay webhook)
# ============================

async def polling_loop():
    """Polling loop como fallback si no hay webhook."""
    offset = 0
    async with aiohttp.ClientSession() as session:
        # Configurar webhook si hay URL
        if WEBHOOK_URL:
            await set_webhook(session)
        
        logger.info("Bot iniciado — escuchando updates...")
        
        while True:
            try:
                if not WEBHOOK_URL:
                    # Polling mode
                    params = {"offset": offset + 1, "timeout": 30, "allowed_updates": ["message", "callback_query"]}
                    async with session.get(f"{API_URL}/getUpdates", params=params) as resp:
                        data = await resp.json()
                        if data.get("ok") and data.get("result"):
                            for update in data["result"]:
                                offset = update["update_id"]
                                
                                if "message" in update:
                                    msg = update["message"]
                                    chat_id = str(msg["chat"]["id"])
                                    if chat_id == CHAT_ID:
                                        text = msg.get("text", "").strip()
                                        if text.startswith("/start"):
                                            await handle_start(session, CHAT_ID)
                                        elif text.startswith("/help"):
                                            await handle_help(session, CHAT_ID)
                                        elif text.startswith("/status"):
                                            await handle_status(session, CHAT_ID)
                                        elif text.startswith("/pending"):
                                            await handle_pending(session, CHAT_ID)
                                        elif text.startswith("/search"):
                                            await handle_search(session, CHAT_ID)
                                
                                elif "callback_query" in update:
                                    await handle_callback(session, update["callback_query"])
                
                await asyncio.sleep(1)
            
            except Exception as e:
                logger.exception("Error en polling loop")
                await asyncio.sleep(5)

# ============================
# MAIN
# ============================

async def main():
    # Verificar directorios
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    (JOBS_DIR / "documents").mkdir(parents=True, exist_ok=True)
    
    logger.info("=" * 50)
    logger.info("JOB TELEGRAM BOT — AI_Nexus_Core")
    logger.info(f"Chat ID autorizado: {CHAT_ID}")
    logger.info(f"Webhook URL: {WEBHOOK_URL or 'Polling mode'}")
    logger.info("=" * 50)
    
    if WEBHOOK_URL:
        # Webhook mode — iniciar servidor aiohttp
        app = web.Application()
        app.router.add_post("/webhook", webhook_handler)
        app.router.add_get("/health", lambda r: web.json_response({"status": "ok"}))
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        logger.info(f"Servidor webhook iniciado en puerto {PORT}")
        
        # Mantener vivo
        try:
            while True:
                await asyncio.sleep(3600)
        except KeyboardInterrupt:
            await runner.cleanup()
    else:
        # Polling mode
        await polling_loop()

if __name__ == "__main__":
    asyncio.run(main())
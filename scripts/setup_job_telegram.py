#!/usr/bin/env python3
"""
Setup script para Job Search Telegram Bot
Guía paso a paso para configurar el bot.
"""

import os
import subprocess
import sys
from pathlib import Path

def print_step(num: int, title: str):
    print(f"\n{'='*60}")
    print(f"PASO {num}: {title}")
    print(f"{'='*60}")

def print_info(text: str):
    print(f"  ℹ️  {text}")

def print_success(text: str):
    print(f"  ✅ {text}")

def print_warning(text: str):
    print(f"  ⚠️  {text}")

def print_error(text: str):
    print(f"  ❌ {text}")

def run_cmd(cmd: list[str]) -> tuple[bool, str]:
    """Ejecuta comando y retorna (success, output)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def main():
    print("\n🤖 JOB SEARCH TELEGRAM BOT — SETUP")
    print("Este script te guía para configurar el bot de Telegram.")
    
    # Paso 1: Verificar Python y dependencias
    print_step(1, "Verificar entorno")
    
    success, output = run_cmd([sys.executable, "--version"])
    if success:
        print_success(f"Python: {output.strip()}")
    else:
        print_error("Python no encontrado")
        return
    
    # Verificar dependencias
    deps = ["aiohttp", "python-dotenv"]
    for dep in deps:
        success, _ = run_cmd([sys.executable, "-c", f"import {dep}"])
        if success:
            print_success(f"{dep} instalado")
        else:
            print_warning(f"{dep} NO instalado — instalando...")
            run_cmd([sys.executable, "-m", "pip", "install", dep])
    
    # Paso 2: Crear archivo .env
    print_step(2, "Configurar variables de entorno (.env)")
    
    env_path = Path(__file__).parent.parent / ".env"
    template_path = Path(__file__).parent / ".env.jobsearch.template"
    
    if env_path.exists():
        print_info(f".env ya existe en {env_path}")
        overwrite = input("  ¿Sobrescribir? (s/N): ").strip().lower()
        if overwrite != 's':
            print_info("Manteniendo .env actual")
        else:
            # Leer template y pedir valores
            pass
    else:
        print_info("Creando .env desde template...")
    
    # Pedir token
    print_info("\n📱 PASO CRÍTICO: Crear bot en Telegram")
    print_info("1. Abre Telegram y busca @BotFather")
    print_info("2. Envía /newbot")
    print_info("3. Pon nombre (ej: 'Mi Job Search Bot')")
    print_info("4. Pon username (ej: 'mi_job_search_bot')")
    print_info("5. Copia el TOKEN que te da (formato: 123456789:ABC-DEF...)")
    
    token = input("\n  Pega tu BOT TOKEN aquí: ").strip()
    if not token or ":" not in token:
        print_error("Token inválido")
        return
    
    # Pedir chat_id
    print_info("\n🆔 Ahora necesitamos tu CHAT_ID:")
    print_info("1. En Telegram, busca @userinfobot o @getmyid_bot")
    print_info("2. Envía /start")
    print_info("3. Copia el ID que te devuelve (número, ej: 123456789)")
    
    chat_id = input("\n  Pega tu CHAT_ID aquí: ").strip()
    if not chat_id.isdigit():
        print_error("Chat ID inválido (debe ser numérico)")
        return
    
    # Webhook opcional
    print_info("\n🌐 Webhook (opcional - para producción):")
    print_info("Si tienes un dominio con HTTPS, pon la URL base (ej: https://mi-dominio.com)")
    print_info("Si no, déjalo vacío para usar polling (consulta cada segundo)")
    webhook = input("\n  WEBHOOK_URL (vacío para polling): ").strip()
    
    port = input("  Puerto (default 8080): ").strip() or "8080"
    
    # Escribir .env
    env_content = f"""# Job Search Telegram Bot
TELEGRAM_BOT_TOKEN={token}
TELEGRAM_CHAT_ID={chat_id}
TELEGRAM_WEBHOOK_URL={webhook}
TELEGRAM_BOT_PORT={port}
"""
    
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print_success(f".env creado en {env_path}")
    
    # Paso 3: Probar bot
    print_step(3, "Probar conexión con Telegram")
    
    import asyncio
    import aiohttp
    
    async def test_bot():
        async with aiohttp.ClientSession() as session:
            # Test getMe
            url = f"https://api.telegram.org/bot{token}/getMe"
            async with session.get(url) as resp:
                data = await resp.json()
                if data.get("ok"):
                    bot_info = data["result"]
                    print_success(f"Bot conectado: @{bot_info['username']} ({bot_info['first_name']})")
                else:
                    print_error(f"Error: {data}")
                    return False
            
            # Test sendMessage
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": "✅ <b>Job Search Bot configurado correctamente!</b>\n\nUsa /help para ver comandos.", "parse_mode": "HTML"}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    data = await resp.json()
                    if data.get("ok"):
                        print_success("Mensaje de prueba enviado a tu Telegram")
                    else:
                        print_error(f"Error enviando mensaje: {data}")
                        return False
            
            return True
    
    try:
        result = asyncio.run(test_bot())
        if not result:
            print_error("Prueba falló")
            return
    except Exception as e:
        print_error(f"Error en prueba: {e}")
        return
    
    # Paso 4: Instrucciones finales
    print_step(4, "¡Listo! Cómo usar el bot")
    
    print_info("\n📱 En Telegram, escribe a tu bot:")
    print_info("  /start    — Iniciar")
    print_info("  /help     — Ver comandos")
    print_info("  /search   — Buscar vacantes ahora")
    print_info("  /status   — Ver estado de aplicaciones")
    print_info("  /pending  — Ver vacantes pendientes")
    print_info("")
    print_info("🎯 Cuando lleguen vacantes, verás botones:")
    print_info("  ✅ Aceptar  → Genera CV/Carta y marca como aplicado")
    print_info("  ❌ Rechazar → Descarta la vacante")
    print_info("  📄 Ver CV/Carta — Rutas de archivos generados")
    print_info("  🔗 Abrir enlace — Abre la vacante en navegador")
    
    print_info("\n🚀 Para EJECUTAR el bot:")
    if os.getenv("TELEGRAM_WEBHOOK_URL"):
        print_info("  python scripts/job_telegram_bot.py")
        print_info("  (Asegúrate de que el webhook URL sea accesible desde internet)")
    else:
        print_info("  python scripts/job_telegram_bot.py")
        print_info("  (Modo polling - consulta cada segundo)")
    
    print_info("\n🔄 Para ejecutar búsqueda AHORA:")
    print_info("  1. En Telegram: /search")
    print_info("  2. O desde terminal: python scripts/job_search_automation.py")
    
    print("\n" + "="*60)
    print_success("SETUP COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    main()
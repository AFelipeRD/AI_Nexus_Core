#!/usr/bin/env python3
"""
Job Telegram Bot - Servicio Windows usando sc.exe + subprocess monitor
Este enfoque SÍ funciona: el servicio es un monitor ligero que lanza el bot como subprocess.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Cargar .env
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value

SERVICE_NAME = "JobTelegramBot"
DISPLAY_NAME = "AI_Nexus_Core Job Telegram Bot"
DESCRIPTION = "Bot de Telegram para Job Search Automation - AI_Nexus_Core"

BAT_WRAPPER = PROJECT_ROOT / "scripts" / "job_telegram_bot_service.bat"
PYTHON_EXE = sys.executable
BOT_SCRIPT = PROJECT_ROOT / "scripts" / "job_telegram_bot.py"
LOG_DIR = PROJECT_ROOT / "output" / "job_search"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "bot.log"
SERVICE_LOG = LOG_DIR / "service.log"


def log(msg: str):
    """Log a archivo y consola."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        with open(SERVICE_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def create_bat_wrapper():
    """Crea el wrapper .bat que ejecuta el bot."""
    bat_content = f'''@echo off
REM Job Telegram Bot - Wrapper para servicio Windows
REM Generado automáticamente

cd /d "{PROJECT_ROOT}"
set PYTHONPATH={PROJECT_ROOT};{PROJECT_ROOT}\\.venv\\Lib\\site-packages
set PYTHONIOENCODING=utf-8

REM Cargar variables de entorno desde .env
if exist "{PROJECT_ROOT}\\.env" (
    for /f "usebackq tokens=1* delims==" %%a in ("{PROJECT_ROOT}\\.env") do (
        if not "%%a"=="" if not "%%a"=="#" set "%%a=%%b"
    )
)

REM Ejecutar bot
"{PYTHON_EXE}" "{BOT_SCRIPT}" >> "{LOG_FILE}" 2>&1

REM Si termina, esperar 5s antes de reiniciar
timeout /t 5 /nobreak >nul
'''
    BAT_WRAPPER.write_text(bat_content, encoding="utf-8")
    log(f"[OK] Wrapper creado: {BAT_WRAPPER}")


def run_cmd(cmd: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=30)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def service_exists() -> bool:
    success, _ = run_cmd(["sc", "query", SERVICE_NAME])
    return success


def install_service():
    """Instala el servicio usando sc.exe nativo."""
    log("Instalando servicio JobTelegramBot...")
    
    # Crear wrapper .bat
    create_bat_wrapper()
    
    # Ruta al wrapper .bat
    bin_path = f'cmd.exe /c "{BAT_WRAPPER}"'
    
    # Crear servicio
    success, output = run_cmd([
        "sc", "create", SERVICE_NAME,
        "binPath=", bin_path,
        "DisplayName=", DISPLAY_NAME,
        "start=", "auto",
        "obj=", "LocalSystem"
    ])
    
    if not success:
        log(f"[ERROR] Error creando servicio: {output}")
        return False
    
    log(f"[OK] Servicio creado")
    
    # Descripción
    run_cmd(["sc", "description", SERVICE_NAME, DESCRIPTION])
    
    # Recuperación ante fallos
    run_cmd([
        "sc", "failure", SERVICE_NAME,
        "actions=", "restart/5000/restart/10000/restart/30000",
        "reset=", "86400"
    ])
    
    # Variables de entorno del servicio
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        log("Configurando variables de entorno del servicio...")
        reg_path = f"HKLM\\SYSTEM\\CurrentControlSet\\Services\\{SERVICE_NAME}\\Environment"
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        subprocess.run([
                            "reg", "add", reg_path, "/v", key, "/t", "REG_SZ", 
                            "/d", value, "/f"
                        ], check=True, capture_output=True, timeout=10)
        except Exception as e:
            log(f"[WARN] Error configurando env vars: {e}")
    
    log("[OK] Servicio instalado y configurado")
    return True


def remove_service():
    """Elimina el servicio."""
    log("Eliminando servicio...")
    run_cmd(["sc", "stop", SERVICE_NAME])
    success, output = run_cmd(["sc", "delete", SERVICE_NAME])
    if success:
        log(f"[OK] Servicio eliminado")
        # Limpiar wrapper
        if BAT_WRAPPER.exists():
            BAT_WRAPPER.unlink()
            log(f"[OK] Wrapper eliminado")
    else:
        log(f"[ERROR] Error eliminando: {output}")
    return success


def start_service():
    """Inicia el servicio."""
    log("Iniciando servicio...")
    success, output = run_cmd(["sc", "start", SERVICE_NAME])
    if success:
        log("[OK] Servicio iniciado")
        # Verificar estado
        time.sleep(2)
        run_cmd(["sc", "query", SERVICE_NAME])
        return True
    else:
        log(f"[ERROR] Error iniciando: {output}")
        return False


def stop_service():
    """Detiene el servicio."""
    log("Deteniendo servicio...")
    success, output = run_cmd(["sc", "stop", SERVICE_NAME])
    if success:
        log("[OK] Servicio detenido")
    else:
        log(f"[ERROR] Error deteniendo: {output}")
    return success


def status_service():
    """Muestra estado."""
    success, output = run_cmd(["sc", "query", SERVICE_NAME])
    if success:
        print(output)
    else:
        print(f"[ERROR] Servicio no encontrado: {output}")


def logs_service(lines: int = 50):
    """Muestra logs."""
    log_file = LOG_DIR / "bot.log"
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            for line in lines[-lines:]:
                print(line.rstrip())
    else:
        print("[INFO] No hay logs aún")


def install_and_start():
    """Instala y arranca."""
    if install_service():
        time.sleep(2)
        start_service()


def main():
    import argparse
    
    os.chdir(PROJECT_ROOT)
    
    # Cargar .env
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
    
    parser = argparse.ArgumentParser(description="Job Telegram Bot - Servicio Windows nativo (sc.exe)")
    parser.add_argument("action", choices=[
        "install", "remove", "start", "stop", "restart", "status", "logs"
    ], help="Acción a realizar")
    args = parser.parse_args()
    
    # Cargar .env
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
    
    actions = {
        "install": install_service,
        "remove": remove_service,
        "start": start_service,
        "stop": lambda: (stop_service(), True),
        "restart": lambda: (stop_service(), time.sleep(2), start_service()),
        "status": status_service,
        "logs": lambda: (logs_service(), True),
    }
    
    action_func = actions.get(args.action)
    if action_func:
        action_func()
    else:
        print(f"Acción desconocida: {args.action}")

if __name__ == "__main__":
    main()
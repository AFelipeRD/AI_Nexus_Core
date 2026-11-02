#!/usr/bin/env python3
"""
Configurador de Tarea Programada Windows para Job Telegram Bot
Usa schtasks nativo - corre como SYSTEM al inicio, con env vars embebidas.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
os.chdir(PROJECT_ROOT)

TASK_NAME = "AI_Nexus_Core_JobTelegramBot"
BAT_WRAPPER = PROJECT_ROOT / "scripts" / "job_telegram_bot_task.bat"
PYTHON_EXE = sys.executable
BOT_SCRIPT = PROJECT_ROOT / "scripts" / "job_telegram_bot.py"
LOG_DIR = PROJECT_ROOT / "output" / "job_search"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def run_cmd(cmd: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=30)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def create_bat_wrapper():
    """Crea el wrapper .bat con auto-reinicio."""
    bat_content = f'''@echo off
REM Job Telegram Bot - Wrapper para Tarea Programada (SYSTEM)
REM Generado automáticamente

cd /d "{PROJECT_ROOT}"
set PYTHONPATH={PROJECT_ROOT};{PROJECT_ROOT}\\.venv\\Lib\\site-packages
set PYTHONIOENCODING=utf-8

REM Variables de entorno embebidas (desde .env)
if exist "{PROJECT_ROOT}\\.env" (
    for /f "usebackq tokens=1* delims==" %%a in ("{PROJECT_ROOT}\\.env") do (
        if not "%%a"=="" if not "%%a"=="#" set "%%a=%%b"
    )
)

:RESTART
"{PYTHON_EXE}" "{BOT_SCRIPT}" >> "{PROJECT_ROOT}\\output\\job_search\\bot.log" 2>&1
timeout /t 10 /nobreak >nul
goto RESTART
'''
    BAT_WRAPPER = PROJECT_ROOT / "scripts" / "job_telegram_bot_task.bat"
    BAT_WRAPPER.write_text(bat_content, encoding="utf-8")
    log(f"[OK] Wrapper creado: {BAT_WRAPPER}")
    return PROJECT_ROOT / "scripts" / "job_telegram_bot_task.bat"

def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def run_cmd(cmd: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=30)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def create_task():
    """Crea la tarea programada como SYSTEM (sin password)."""
    bat_path = create_bat_wrapper()
    
    log("Creando tarea programada (SYSTEM, al inicio)...")
    
    # Usar SYSTEM account - no necesita password, corre al inicio
    cmd = [
        "schtasks", "/create",
        "/tn", "AI_Nexus_Core_JobTelegramBot",
        "/tr", f'cmd.exe /c "{BAT_WRAPPER}"',
        "/sc", "onstart",
        "/ru", "SYSTEM",
        "/rl", "highest",
        "/f"
    ]
    
    log("Creando tarea programada (SYSTEM)...")
    success, output = run_cmd(cmd)
    if not success:
        log(f"[ERROR] Error creando tarea: {output}")
        return False
    
    log("[OK] Tarea programada creada (SYSTEM)")
    
    # Configurar reinicio ante fallo
    run_cmd([
        "schtasks", "/change", "/tn", "AI_Nexus_Core_JobTelegramBot",
        "/ri", "5", "/du", "9999:59"
    ])
    
    log("[OK] Tarea configurada: reinicio cada 5 min si falla")
    return True


def start_task():
    log("Iniciando tarea...")
    success, output = run_cmd(["schtasks", "/run", "/tn", "AI_Nexus_Core_JobTelegramBot"])
    if success:
        log("[OK] Tarea iniciada")
        time.sleep(3)
        query_task()
    else:
        log(f"[ERROR] Error: {output}")
    return success


def stop_task():
    log("Deteniendo tarea...")
    success, output = run_cmd(["schtasks", "/end", "/tn", "AI_Nexus_Core_JobTelegramBot", "/f"])
    log("[OK] Tarea detenida" if success else f"[ERROR] {output}")
    return success


def query_task():
    success, output = run_cmd(["schtasks", "/query", "/tn", "AI_Nexus_Core_JobTelegramBot", "/v", "/fo", "LIST"])
    if success:
        print(output)
    else:
        log(f"[ERROR] {output}")


def logs_task(lines: int = 50):
    log_file = PROJECT_ROOT / "output" / "job_search" / "bot.log"
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f.readlines()[-lines:]:
                print(line.rstrip())
    else:
        print("[INFO] No hay logs aún")


def remove_task():
    log("Eliminando tarea...")
    run_cmd(["schtasks", "/end", "/tn", "AI_Nexus_Core_JobTelegramBot", "/f"])
    success, output = run_cmd(["schtasks", "/delete", "/tn", "AI_Nexus_Core_JobTelegramBot", "/f"])
    if success:
        log("[OK] Tarea eliminada")
        bat_path = PROJECT_ROOT / "scripts" / "job_telegram_bot_task.bat"
        if bat_path.exists():
            bat_path.unlink()
            log("[OK] Wrapper eliminado")
    else:
        log(f"[ERROR] {output}")
    return success


def run_cmd(cmd: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=30)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def main():
    import argparse
    from pathlib import Path
    
    PROJECT_ROOT = Path(__file__).parent.parent
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
    
    parser = argparse.ArgumentParser(description="Job Telegram Bot - Tarea Programada Windows (schtasks)")
    parser.add_argument("action", choices=[
        "install", "remove", "start", "stop", "restart", "status", "logs"
    ], help="Acción a realizar")
    args = parser.parse_args()
    
    actions = {
        "install": create_task,
        "remove": lambda: (remove_task(), True),
        "start": start_task,
        "stop": lambda: (stop_task(), True),
        "restart": lambda: (stop_task(), time.sleep(2), start_task()),
        "status": query_task,
        "logs": lambda: (logs_task(), True),
    }
    
    action_func = actions.get(args.action)
    if action_func:
        action_func()
    else:
        print(f"Acción desconocida: {args.action}")

def remove_task():
    log("Eliminando tarea...")
    run_cmd(["schtasks", "/end", "/tn", "AI_Nexus_Core_JobTelegramBot", "/f"])
    success, output = run_cmd(["schtasks", "/delete", "/tn", "AI_Nexus_Core_JobTelegramBot", "/f"])
    if success:
        log("[OK] Tarea eliminada")
        bat_path = PROJECT_ROOT / "scripts" / "job_telegram_bot_task.bat"
        if bat_path.exists():
            bat_path.unlink()
            log("[OK] Wrapper eliminado")
    else:
        log(f"[ERROR] {output}")
    return success

if __name__ == "__main__":
    main()
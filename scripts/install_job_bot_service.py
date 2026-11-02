#!/usr/bin/env python3
"""
Instalador de servicio Windows para Job Telegram Bot
Crea un servicio Windows que corre 24/7 en background.
Requiere permisos de administrador.
"""

import os
import sys
import subprocess
import winreg
from pathlib import Path

def run_cmd(cmd: list[str], shell: bool = True) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=shell, timeout=30)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def is_admin() -> bool:
    """Verifica si se ejecuta como administrador."""
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def check_python_path() -> str:
    """Obtiene la ruta completa de python.exe."""
    return sys.executable

def create_service():
    """Crea el servicio Windows usando NSSM (Non-Sucking Service Manager)."""
    
    # Rutas
    project_root = Path(__file__).parent.parent
    python_exe = check_python_path()
    script_path = project_root / "scripts" / "job_telegram_bot.py"
    working_dir = project_root
    nssm_path = project_root / "tools" / "nssm.exe"
    
    service_name = "JobTelegramBot"
    display_name = "AI_Nexus_Core Job Telegram Bot"
    description = "Bot de Telegram para Job Search Automation - AI_Nexus_Core"
    
    print(f"🤖 Instalando servicio Windows: {service_name}")
    print(f"Python: {python_exe}")
    print(f"Script: {script_path}")
    print(f"Directorio: {working_dir}")
    
    # Verificar NSSM
    if not nssm_path.exists():
        print("⚠️ NSSM no encontrado. Descargando...")
        nssm_url = "https://nssm.cc/release/nssm-2.24.zip"
        tools_dir = project_root / "tools"
        tools_dir.mkdir(exist_ok=True)
        
        import urllib.request
        import zipfile
        import io
        
        print("Descargando NSSM...")
        response = urllib.request.urlopen(nssm_url)
        zip_data = io.BytesIO(response.read())
        with zipfile.ZipFile(zip_data) as z:
            z.extract("nssm-2.24/win64/nssm.exe", tools_dir)
            (tools_dir / "nssm-2.24" / "win64" / "nssm.exe").rename(nssm_path)
            # Limpiar
            import shutil
            shutil.rmtree(tools_dir / "nssm-2.24")
        print_success(f"NSSM instalado en {nssm_path}")
    
    # Verificar script
    if not script_path.exists():
        print_error(f"Script no encontrado: {script_path}")
        return False
    
    # Verificar .env
    env_file = working_dir / ".env"
    if not env_file.exists():
        print_warning(".env no encontrado. El bot necesitará TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID")
        print_info("Ejecuta: python scripts/setup_job_telegram.py")
    
    # Crear servicio con NSSM
    print_info(f"Creando servicio '{service_name}'...")
    
    # Install
    success, output = run_cmd([
        str(nssm_path), "install", service_name,
        python_exe, str(script_path)
    ])
    if not success:
        print_error(f"Error instalando servicio: {output}")
        return False
    
    # Configurar directorio de trabajo
    success, output = run_cmd([str(nssm_path), "set", service_name, "AppDirectory", str(working_dir)])
    if not success:
        print_error(f"Error configurando directorio: {output}")
        return False
    
    # Configurar descripción
    success, output = run_cmd([str(nssm_path), "set", service_name, "Description", "Bot de Telegram para Job Search Automation - AI_Nexus_Core"])
    if not success:
        print_warning(f"Error configurando descripción: {output}")
    
    # Configurar inicio automático
    success, output = run_cmd([str(nssm_path), "set", service_name, "Start", "SERVICE_AUTO_START"])
    if not success:
        print_error(f"Error configurando inicio auto: {output}")
        return False
    
    # Configurar reinicio en caso de fallo
    run_cmd([str(nssm_path), "set", service_name, "AppExit", "Default", "Restart"])
    run_cmd([str(nssm_path), "set", service_name, "AppThrottle", "1000"])
    run_cmd([str(nssm_path), "set", service_name, "AppRestartDelay", "5000"])
    
    # Configurar logging
    log_dir = Path(__file__).parent.parent / "output" / "job_search"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "bot.log"
    
    run_cmd([str(nssm_path), "set", service_name, "AppStdout", str(log_file)])
    run_cmd([str(nssm_path), "set", service_name, "AppStderr", str(log_file)])
    run_cmd([str(nssm_path), "set", service_name, "AppRotateFiles", "1"])
    run_cmd([str(nssm_path), "set", service_name, "AppRotateBytes", "10485760"])  # 10MB
    
    # Configurar variables de entorno del servicio
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    run_cmd([str(nssm_path), "set", service_name, "AppEnvironmentExtra", f"{key}={value}"])
    
    print_success(f"Servicio '{service_name}' creado y configurado")
    
    # Iniciar servicio
    print_info("Iniciando servicio...")
    success, output = run_cmd([str(nssm_path), "start", service_name])
    if success:
        print_success("Servicio iniciado correctamente")
    else:
        print_warning(f"Servicio creado pero no iniciado: {output}")
        print_info("Puedes iniciarlo manualmente: nssm start JobTelegramBot")
    
    return True

def remove_service():
    """Elimina el servicio Windows."""
    nssm_path = Path(__file__).parent.parent / "tools" / "nssm.exe"
    service_name = "JobTelegramBot"
    
    if not nssm_path.exists():
        print_error("NSSM no encontrado")
        return False
    
    # Detener y eliminar
    run_cmd([str(nssm_path), "stop", service_name])
    success, output = run_cmd([str(nssm_path), "remove", service_name, "confirm"])
    
    if success:
        print_success(f"Servicio '{service_name}' eliminado")
    else:
        print_error(f"Error eliminando servicio: {output}")
    return success

def print_success(msg): print(f"  ✅ {msg}")
def print_error(msg): print(f"  ❌ {msg}")
def print_warning(msg): print(f"  ⚠️ {msg}")
def print_info(msg): print(f"  ℹ️ {msg}")

def run_cmd(cmd: list[str], shell: bool = True) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=shell, timeout=30)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def print_success(msg): print(f"  ✅ {msg}")
def print_error(msg): print(f"  ❌ {msg}")
def print_warning(msg): print(f"  ⚠️ {msg}")
def print_info(msg): print(f"  ℹ️ {msg}")

def main():
    if not is_admin():
        print_error("ESTE SCRIPT REQUIERE PERMISOS DE ADMINISTRADOR")
        print_info("Ejecuta PowerShell o CMD como Administrador y luego:")
        print_info(f"  python {__file__}")
        return
    
    print("\n" + "="*60)
    print("🤖 INSTALADOR SERVICIO WINDOWS - JOB TELEGRAM BOT")
    print("="*60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        remove_service()
        return
    
    create_service()
    
    print("\n" + "="*60)
    print_success("INSTALACIÓN COMPLETADA")
    print("="*60)
    print_info("Comandos útiles:")
    print_info("  Iniciar:   nssm start JobTelegramBot")
    print_info("  Detener:   nssm stop JobTelegramBot")
    print_info("  Reiniciar: nssm restart JobTelegramBot")
    print_info("  Estado:    nssm status JobTelegramBot")
    print_info("  Logs:      type output\\job_search\\bot.log")
    print_info("  Eliminar:  python scripts\\install_job_bot_service.py remove")
    print("="*60)

def is_admin() -> bool:
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

if __name__ == "__main__":
    main()
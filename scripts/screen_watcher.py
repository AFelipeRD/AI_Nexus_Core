"""Percepción de pantalla ligera para modelos con visión (p. ej. Nemotron 3.5 Super VL).

Instantáneas locales y efímeras de la pantalla completa o de la ventana activa
para auditar interfaces en tiempo real.

Uso (terminal, desde la raíz del repositorio):
    python scripts/screen_watcher.py                        # pantalla completa
    python scripts/screen_watcher.py --ventana              # solo la ventana activa
    python scripts/screen_watcher.py --salida <ruta.png>    # destino alternativo

Privacidad (supervisión Laya AI, obligatoria):
- La captura vive solo en disco local y es EFÍMERA: elimínala tras el análisis.
- PROHIBIDO capturar pantallas con credenciales visibles o datos personales
  sin autorización explícita del usuario; prohibido commitear la instantánea
  (`.gitignore` bloquea `assets/temp_screen*.png`).
- Ninguna acción derivada de la captura puede ser destructiva.
"""
from __future__ import annotations

import argparse
import ctypes
import ctypes.wintypes
from pathlib import Path

from PIL import ImageGrab

BASE = Path(__file__).resolve().parent.parent
SALIDA_POR_DEFECTO = BASE / "assets" / "temp_screen.png"

user32 = ctypes.windll.user32


def _rect_ventana_activa() -> tuple[int, int, int, int] | None:
    """Devuelve (x1, y1, x2, y2) de la ventana en primer plano, o None."""
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return None
    rect = ctypes.wintypes.RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        return None
    if rect.right - rect.left <= 0 or rect.bottom - rect.top <= 0:
        return None
    return (rect.left, rect.top, rect.right, rect.bottom)


def capturar(salida: Path, solo_ventana: bool = False) -> Path:
    """Captura la pantalla (o ventana activa) y guarda un PNG optimizado."""
    bbox = _rect_ventana_activa() if solo_ventana else None
    img = ImageGrab.grab(bbox=bbox)
    salida.parent.mkdir(parents=True, exist_ok=True)
    img.save(salida, format="PNG", optimize=True)
    print(f"[OK] Captura {img.width}x{img.height} guardada en: {salida}")
    print("[AVISO] Instantanea efimera: eliminala tras el analisis; nunca la commitees.")
    return salida


def main() -> None:
    parser = argparse.ArgumentParser(description="Instantanea ligera de pantalla para modelos con vision.")
    parser.add_argument("--ventana", action="store_true", help="capturar solo la ventana activa")
    parser.add_argument("--salida", type=Path, default=SALIDA_POR_DEFECTO, help="ruta del PNG de salida")
    args = parser.parse_args()
    capturar(args.salida, args.ventana)


if __name__ == "__main__":
    main()

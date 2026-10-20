"""Generación de imágenes con FLUX 3 Image Klein (NVIDIA Build).

Uso (terminal, desde la raíz del repositorio):
    python scripts/nvidia_flux.py "<PROMPT_EN_INGLES>" "<NOMBRE_ARCHIVO.png>"

- Resolución fija: 1024x1024 px, steps=50, seed=0.
- La clave se lee en tiempo de ejecución de D:/AI_Nexus_Core/.secrets/nvidia.key.
- La imagen se guarda en output/images/<NOMBRE_ARCHIVO.png>.
"""
import base64
import os
import sys
from typing import Any

import requests

BASE_DIR = "D:/AI_Nexus_Core"
KEY_PATH = f"{BASE_DIR}/.secrets/nvidia.key"
OUTPUT_DIR = f"{BASE_DIR}/output/images"
INVOKE_URL = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux-3-image-klein"


def _leer_api_key() -> str | None:
    """Lee la clave de NVIDIA Build desde .secrets/ (nunca versionada)."""
    try:
        with open(KEY_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] No se encontro la clave en {KEY_PATH}")
        return None


def generar_imagen(prompt_texto: str, nombre_archivo: str = "robot_publicidad.png") -> None:
    api_key = _leer_api_key()
    if not api_key:
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    payload = {
        "prompt": prompt_texto,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "steps": 50,
    }

    print(f"[FLUX] Llamando a NVIDIA Build API con el prompt: '{prompt_texto[:60]}...'")
    try:
        res = requests.post(INVOKE_URL, headers=headers, json=payload, timeout=300)
    except requests.RequestException as exc:
        print(f"[ERROR] Fallo de red al llamar a NVIDIA Build: {exc}")
        sys.exit(1)

    if res.status_code != 200:
        print(f"[ERROR] NVIDIA respondio con codigo {res.status_code}: {res.text}")
        sys.exit(1)

    res_json: dict[str, Any] = res.json()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, nombre_archivo)

    # Extraer base64 de la primera estructura conocida de la respuesta.
    b64_str: str | None = None
    if res_json.get("artifacts"):
        b64_str = res_json["artifacts"][0].get("base64")
    b64_str = b64_str or res_json.get("image") or res_json.get("b64_json")

    if b64_str:
        with open(out_path, "wb") as f_img:
            f_img.write(base64.b64decode(b64_str))
        print(f"[EXITO] Imagen generada y guardada en: {out_path}")
    else:
        print("[AVISO] La respuesta no trajo imagen decodificable.")
        print("[INFO] Estructura recibida de NVIDIA:", list(res_json.keys()))
        sys.exit(2)


if __name__ == "__main__":
    prompt_in = sys.argv[1] if len(sys.argv) > 1 else "A cute delivery robot in 3D Pixar style holding a gift box, commercial lighting"
    nombre_in = sys.argv[2] if len(sys.argv) > 2 else "robot_publicidad.png"
    generar_imagen(prompt_in, nombre_in)

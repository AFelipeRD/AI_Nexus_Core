"""Generación de video / simulación física con NVIDIA Cosmos 3 Nano (NVIDIA Build).

Uso (terminal, desde la raíz del repositorio):
    python scripts/nvidia_cosmos.py "<PROMPT_EN_INGLES>" "<NOMBRE_ARCHIVO.mp4>"

- La clave se lee en tiempo de ejecución de D:/AI_Nexus_Core/.secrets/nvidia.key.
- Si la API devuelve un artefacto descargable (URL o base64), se guarda en
  output/videos/<NOMBRE_ARCHIVO.mp4>; si solo devuelve metadatos, avisa con [AVISO].
"""
import base64
import json
import os
import sys
from typing import Any

import requests

BASE_DIR = "D:/AI_Nexus_Core"
KEY_PATH = f"{BASE_DIR}/.secrets/nvidia.key"
OUTPUT_DIR = f"{BASE_DIR}/output/videos"
INVOKE_URL = "https://ai.api.nvidia.com/v1/cosmos/nvidia/cosmos3-nano"


def _leer_api_key() -> str | None:
    """Lee la clave de NVIDIA Build desde .secrets/ (nunca versionada)."""
    try:
        with open(KEY_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] No se encontro la clave en {KEY_PATH}")
        return None


def _extraer_artefacto(res_json: dict[str, Any]) -> tuple[str, str] | None:
    """Devuelve ('url'|'b64', dato) con el artefacto de video, o None si no existe."""
    for campo in ("video", "video_url", "url", "b64_json", "artifact_url"):
        valor = res_json.get(campo)
        if isinstance(valor, str) and valor:
            return ("b64" if "b64" in campo else "url"), valor
    for artefacto in res_json.get("artifacts", []):
        if isinstance(artefacto, dict):
            if artefacto.get("base64"):
                return "b64", artefacto["base64"]
            if artefacto.get("url"):
                return "url", artefacto["url"]
    return None


def generar_video_cosmos(prompt_texto: str, output_filename: str = "cosmos_sim.mp4") -> None:
    api_key = _leer_api_key()
    if not api_key:
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt_texto,
            }
        ]
    }

    print(f"[COSMOS] Enviando simulación física a NVIDIA: '{prompt_texto[:50]}...'")
    try:
        response = requests.post(INVOKE_URL, headers=headers, json=payload, timeout=300)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[ERROR] Fallo de red al llamar a NVIDIA Build: {exc}")
        sys.exit(1)

    res_data: dict[str, Any] = response.json()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, output_filename)

    artefacto = _extraer_artefacto(res_data)
    if artefacto is None:
        print("[AVISO] La respuesta no trajo un artefacto de video descargable.")
        print("[INFO] Estructura recibida de NVIDIA:", json.dumps(res_data, indent=2)[:2000])
        sys.exit(2)

    modo, dato = artefacto
    try:
        if modo == "b64":
            with open(out_path, "wb") as f_out:
                f_out.write(base64.b64decode(dato))
        else:
            descarga = requests.get(dato, timeout=300)
            descarga.raise_for_status()
            with open(out_path, "wb") as f_out:
                f_out.write(descarga.content)
    except (requests.RequestException, ValueError) as exc:
        print(f"[ERROR] No se pudo guardar el video en {out_path}: {exc}")
        sys.exit(1)

    print(f"[EXITO] Video generado y guardado en: {out_path}")


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Quantum particles colliding in space, physical simulation"
    out_name = sys.argv[2] if len(sys.argv) > 2 else "cosmos_sim.mp4"
    generar_video_cosmos(prompt, out_name)

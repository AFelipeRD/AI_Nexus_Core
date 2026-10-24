"""Catalogo vivo de funciones de medios de la cuenta NVIDIA NIM (NVCF).

Uso (terminal, desde la raiz del repositorio):
    python scripts/media_catalogo.py           # tabla legible (solo medios)
    python scripts/media_catalogo.py --todo    # incluye LLM/ciencia/otros
    python scripts/media_catalogo.py --json    # JSON para orquestadores

- Consulta GET https://api.nvcf.nvidia.com/v2/nvcf/functions con la clave de
  .secrets/nvidia.key y clasifica las funciones a las que ESTA cuenta esta
  entitled (el catalogo ES la fuente de verdad; NVIDIA rotar modelos sin aviso).
- Cero modelos quemados: la rotacion se hace por argumento (--modelo), no por
  codigo. Este script es el paso previo recomendado de nvidia_flux.py y
  nvidia_cosmos.py.
"""
import argparse
import json
import re
import sys
from typing import Any

import requests

BASE_DIR = "D:/AI_Nexus_Core"
KEY_PATH = f"{BASE_DIR}/.secrets/nvidia.key"
URL_FUNCIONES = "https://api.nvcf.nvidia.com/v2/nvcf/functions"

# (categoria, patron) — se evaluan en orden; la primera que matchea gana.
REGLAS: list[tuple[str, str]] = [
    ("imagen-edicion", r"flux.*kontext|kontext"),
    ("imagen", r"flux|sdxl|stable-diffusion|imagen|edify-image|qwen-image|relighting|eyecontact|changenet|graphic-elements"),
    ("video", r"cosmos-predict|cosmos3|\bcosmos-[0-9]|\bltx\b|\bwan-?2|\bhunyuan\b|stable-video|\bsvd\b|\bkling\b|\bveo\b|\bt2v\b|\bi2v\b|\bvideo[-_]?gen\b"),
    ("video-analisis", r"video-detector|cosmos-nemotron|cosmos-reason"),
    ("3d", r"trellis|usdsearch|a2x"),
    ("audio", r"tts|asr|voice|parakeet|whisper|chatterbox|magpie|riva|canary|conformer|studiovoice"),
]


def _leer_api_key() -> str | None:
    try:
        with open(KEY_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] No se encontro la clave en {KEY_PATH}")
        return None


def _clasificar(nombre: str) -> str:
    for categoria, patron in REGLAS:
        if re.search(patron, nombre, re.IGNORECASE):
            return categoria
    return "otros"


def obtener_catalogo(api_key: str) -> list[dict[str, str]]:
    """[(nombre_normalizado, function_id, categoria)] de funciones entitled."""
    res = requests.get(
        URL_FUNCIONES,
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
        timeout=60,
    )
    if res.status_code != 200:
        print(f"[ERROR] NVCF respondio {res.status_code}: {res.text[:200]}")
        sys.exit(1)
    datos: dict[str, Any] = res.json()
    funciones = datos.get("functions") or datos or []
    catalogo: list[dict[str, str]] = []
    vistos: set[str] = set()
    for fn in funciones:
        fid = fn.get("id", "")
        nombre = fn.get("name", "")
        clave = f"{nombre}"
        if not nombre or clave in vistos:
            continue
        vistos.add(clave)
        catalogo.append({
            "modelo": nombre.removeprefix("ai-"),
            "function_id": fid,
            "categoria": _clasificar(nombre),
        })
    return sorted(catalogo, key=lambda x: (x["categoria"], x["modelo"]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Catalogo vivo de funciones NIM/NVCF de la cuenta.")
    parser.add_argument("--json", action="store_true", help="Salida JSON (todas las categorias).")
    parser.add_argument("--todo", action="store_true", help="Incluir categorias no mediaticas en la tabla.")
    args = parser.parse_args()

    api_key = _leer_api_key()
    if not api_key:
        sys.exit(1)
    catalogo = obtener_catalogo(api_key)

    if args.json:
        print(json.dumps(catalogo, indent=2, ensure_ascii=False))
        return

    categorias_medios = {"imagen", "imagen-edicion", "video", "video-analisis", "3d", "audio"}
    filas = [c for c in catalogo if args.todo or c["categoria"] in categorias_medios]
    print(f"{'CATEGORIA':<16} {'MODELO':<38} FUNCTION_ID")
    print("-" * 92)
    for f in filas:
        print(f"{f['categoria']:<16} {f['modelo']:<38} {f['function_id']}")
    videos = [c for c in catalogo if c["categoria"] == "video"]
    if not videos:
        print()
        print("[INFO] Ninguna funcion de generacion de video entitled en esta cuenta hoy.")
        print("       Rotacion: cuando NVIDIA otorgue cosmos-predict/ltx/wan a la cuenta,")
        print("       apareceran aqui y nvidia_cosmos.py las usara automaticamente.")


if __name__ == "__main__":
    main()

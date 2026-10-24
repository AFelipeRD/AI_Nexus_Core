"""Generacion de imagenes con el motor NVIDIA NIM — catalogo vivo, modelo agnostico.

Uso (terminal, desde la raiz del repositorio):
    python scripts/nvidia_flux.py "<PROMPT_EN_INGLES>" "<ARCHIVO.png>"
    python scripts/nvidia_flux.py "<PROMPT>" "<ARCHIVO.png>" --modelo flux_1_schnell
    python scripts/nvidia_flux.py "<PROMPT>" "<ARCHIVO.png>" --modelo flux_2_klein_4b --ancho 1280 --alto 720

- --modelo acepta cualquier funcion de imagen del catalogo de la cuenta
  (ver: python scripts/media_catalogo.py). Por defecto: flux_3_image_klein.
- Mecanismo: NVCF pexec por function_id (catalogo consultado en vivo) con
  fallback al gateway ai.api.nvidia.com. Cero modelos quemados: la rotacion
  de modelos se hace por argumento, no por codigo.
- La clave se lee de D:/AI_Nexus_Core/.secrets/nvidia.key (la misma del
  proveedor LLM nvidia de opencode.json — creditos de desarrollador gratuitos).
- La imagen se guarda en output/images/<ARCHIVO.png>.
"""
import argparse
import base64
import os
import sys
import time
from typing import Any

import requests

BASE_DIR = "D:/AI_Nexus_Core"
KEY_PATH = f"{BASE_DIR}/.secrets/nvidia.key"
OUTPUT_DIR = f"{BASE_DIR}/output/images"

URL_FUNCIONES = "https://api.nvcf.nvidia.com/v2/nvcf/functions"
URL_PEXEC = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions"
URL_POLL = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status"
POLL_INTERVALO_S = 5
POLL_TOPE_S = 300

MODELO_DEFECTO = "flux_3_image_klein"
RE_IMAGEN = r"flux|sdxl|stable-diffusion|imagen|edify-image|qwen-image"


def _leer_api_key() -> str | None:
    try:
        with open(KEY_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] No se encontro la clave en {KEY_PATH}")
        return None


def _normalizar(nombre: str) -> str:
    return nombre.lower().replace("ai-", "", 1).strip()


def _catalogo(api_key: str) -> list[dict[str, str]]:
    res = requests.get(
        URL_FUNCIONES,
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
        timeout=60,
    )
    if res.status_code != 200:
        print(f"[ERROR] No se pudo leer el catalogo NVCF ({res.status_code}).")
        sys.exit(6)
    datos: dict[str, Any] = res.json()
    funciones = datos.get("functions") or datos or []
    vistos: set[str] = set()
    filas: list[dict[str, str]] = []
    for fn in funciones:
        nombre = fn.get("name", "")
        if not nombre or nombre in vistos:
            continue
        vistos.add(nombre)
        filas.append({"modelo": _normalizar(nombre), "function_id": fn.get("id", "")})
    return filas


def _resolver_function_id(api_key: str, modelo: str) -> tuple[str, str]:
    """Busca el modelo pedido en el catalogo vivo; devuelve (function_id, modelo_real)."""
    import re
    objetivo = modelo.lower().replace("-", "_").replace(".", "_")
    filas = _catalogo(api_key)
    candidatas = [f for f in filas if re.search(RE_IMAGEN, f["modelo"], re.IGNORECASE)]
    for f in candidatas:
        if f["modelo"].lower().replace("-", "_").replace(".", "_") == objetivo:
            return f["function_id"], f["modelo"]
    print(f"[ERROR] '{modelo}' no esta en el catalogo de imagen de esta cuenta.")
    print("[INFO] Modelos de imagen disponibles hoy:")
    for f in candidatas:
        print(f"       - {f['modelo']}")
    sys.exit(7)


def _cuerpos_candidatos(modelo: str, args: argparse.Namespace) -> list[dict[str, Any]]:
    """Perfiles de cuerpo por familia + fallbacks genericos (la forma varia por modelo)."""
    m = modelo.lower()
    base = {"prompt": args.prompt, "width": args.ancho, "height": args.alto, "seed": args.seed}
    if "klein-3" in m or "klein_3" in m:
        return [dict(base, steps=args.pasos), {"prompt": args.prompt, "seed": args.seed}]
    if "schnell" in m:
        return [
            {"prompt": args.prompt, "mode": "base", "aspect_ratio": "1:1", "seed": args.seed},
            dict(base, steps=4),
            {"prompt": args.prompt, "seed": args.seed},
        ]
    return [dict(base, steps=args.pasos), {"prompt": args.prompt, "seed": args.seed}]


def _extraer_imagen(res_json: dict[str, Any]) -> bytes | None:
    if res_json.get("artifacts"):
        b64 = res_json["artifacts"][0].get("base64")
        if b64:
            return base64.b64decode(b64)
    for clave in ("b64_image", "image", "b64_json"):
        valor = res_json.get(clave)
        if isinstance(valor, str) and len(valor) > 64:
            return base64.b64decode(valor)
    return None


def _poll(reqid: str, api_key: str) -> requests.Response | None:
    inicio = time.time()
    while time.time() - inicio < POLL_TOPE_S:
        res = requests.get(
            f"{URL_POLL}/{reqid}",
            headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
            timeout=120,
        )
        if res.status_code != 202:
            return res
        time.sleep(POLL_INTERVALO_S)
        print("[NIM] Generando en la nube... (poll)")
    return None


def generar_imagen(args: argparse.Namespace) -> None:
    api_key = _leer_api_key()
    if not api_key:
        sys.exit(1)

    function_id, modelo_real = _resolver_function_id(api_key, args.modelo)
    print(f"[NIM] Modelo: {modelo_real} (function_id={function_id[:8]}...)")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, args.archivo)
    cabeceras = {"Authorization": f"Bearer {api_key}", "Accept": "application/json",
                 "Content-Type": "application/json"}

    ultimo_error = ""
    for cuerpo in _cuerpos_candidatos(modelo_real, args):
        res = requests.post(f"{URL_PEXEC}/{function_id}", headers=cabeceras, json=cuerpo, timeout=120)
        if res.status_code == 202:
            reqid = res.headers.get("NVCF-REQID")
            if not reqid:
                print("[ERROR] 202 sin NVCF-REQID.")
                sys.exit(6)
            print("[NIM] Trabajo aceptado (async). Sondeando NVCF...")
            res = _poll(reqid, api_key) or res
        if res.status_code == 200:
            try:
                imagen = _extraer_imagen(res.json())
            except ValueError:
                imagen = None
            if imagen:
                with open(out_path, "wb") as f:
                    f.write(imagen)
                print(f"[EXITO] Imagen guardada en: {out_path}")
                print(f"[INFO] Modelo: {modelo_real} · {len(imagen) / 1_000_000:.2f} MB")
                return
            ultimo_error = "200 sin imagen decodificable"
            continue
        if res.status_code in (400, 422):
            ultimo_error = f"{res.status_code}: {res.text[:160]}"
            continue  # forma de cuerpo incorrecta -> probar el siguiente perfil
        print(f"[ERROR] NVCF respondio {res.status_code}: {res.text[:300]}")
        sys.exit(1)

    print(f"[ERROR] Ningun perfil de cuerpo funciono para {modelo_real}. Ultimo: {ultimo_error}")
    sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generacion de imagenes NIM (catalogo vivo).")
    parser.add_argument("prompt", help="Prompt en ingles")
    parser.add_argument("archivo", help="Nombre del archivo de salida en output/images/")
    parser.add_argument("--modelo", default=MODELO_DEFECTO, help="Modelo del catalogo (media_catalogo.py)")
    parser.add_argument("--ancho", type=int, default=1024)
    parser.add_argument("--alto", type=int, default=1024)
    parser.add_argument("--pasos", type=int, default=50)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    generar_imagen(args)


if __name__ == "__main__":
    main()

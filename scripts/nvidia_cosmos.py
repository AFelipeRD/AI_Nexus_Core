"""Motor de video NVIDIA NIM — catalogo vivo, modelo agnostico.

Uso (terminal, desde la raiz del repositorio):
    python scripts/nvidia_cosmos.py "<PROMPT_EN_INGLES>" "<ARCHIVO.mp4>"
    python scripts/nvidia_cosmos.py "<PROMPT>" "<ARCHIVO.mp4>" --modelo <nombre_del_catalogo>

- Consulta el catalogo NVCF de la cuenta (scripts/media_catalogo.py) y usa
  cualquier funcion de generacion de video entitled (cosmos-predict, ltx,
  wan, hunyuan, svd, kling, veo...). Cero modelos quemados: la rotacion de
  modelos se hace por argumento, no por codigo.
- Si hoy no hay ninguna funcion de video entitled, lo informa con las
  alternativas honestas (NVIDIA rota funciones sin aviso; el estado cambia
  solo, sin tocar codigo).
- Protocolo NVCF: submit (pexec por function_id) -> 202 + NVCF-REQID ->
  poll en api.nvcf.nvidia.com/v2/nvcf/pexec/status/{reqid} hasta 200 ->
  extraccion tolerante (KServe outputs, b64_video, artifacts, asset_url, mp4 crudo).
- La clave se lee de D:/AI_Nexus_Core/.secrets/nvidia.key (creditos NIM gratuitos).
- El video se guarda en output/videos/<ARCHIVO.mp4>.
"""
import argparse
import base64
import os
import re
import sys
import time
from typing import Any

import requests

BASE_DIR = "D:/AI_Nexus_Core"
KEY_PATH = f"{BASE_DIR}/.secrets/nvidia.key"
OUTPUT_DIR = f"{BASE_DIR}/output/videos"

URL_FUNCIONES = "https://api.nvcf.nvidia.com/v2/nvcf/functions"
URL_PEXEC = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions"
URL_POLL = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status"
POLL_INTERVALO_S = 5
POLL_TOPE_S = 600

RE_VIDEO = r"cosmos-predict|cosmos3|\bcosmos-[0-9]|\bltx\b|\bwan-?2|\bhunyuan\b|stable-video|\bsvd\b|\bkling\b|\bveo\b|\bt2v\b|\bi2v\b|\bvideo[-_]?gen\b"
RE_EXCLUIR = r"detector|nemotron|reason"

SUFJO_ESTILO = ", cinematic lighting, volumetric atmosphere, vivid color, photoreal"
PALABRAS_ESTILO = ("cinematic", "lighting", "sunset", "sunrise", "neon",
                   "golden hour", "vivid", "photoreal", "volumetric", "dramatic")
PROMPT_MAX = 300


def _leer_api_key() -> str | None:
    try:
        with open(KEY_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] No se encontro la clave en {KEY_PATH}")
        return None


def _prompt_estilizado(prompt: str) -> str:
    texto = " ".join(str(prompt).split())[:PROMPT_MAX]
    if not any(p in texto.lower() for p in PALABRAS_ESTILO):
        texto = (texto + SUFJO_ESTILO)[:PROMPT_MAX + len(SUFJO_ESTILO)]
    return texto.replace('"', "'")


def _funciones_video(api_key: str) -> list[dict[str, str]]:
    """Funciones de GENERACION de video entitled hoy en la cuenta."""
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
        if re.search(RE_VIDEO, nombre, re.IGNORECASE) and not re.search(RE_EXCLUIR, nombre, re.IGNORECASE):
            filas.append({"modelo": nombre.removeprefix("ai-"), "function_id": fn.get("id", "")})
    return filas


def _es_mp4(datos: bytes | None) -> bool:
    return bool(datos) and len(datos) > 16 and datos[4:8] == b"ftyp"


def _descargar(url: str, api_key: str) -> bytes | None:
    cabeceras = {"Authorization": f"Bearer {api_key}"} if "nvidia.com" in url else {}
    try:
        res = requests.get(url, headers=cabeceras, timeout=300)
        return res.content if res.status_code == 200 else None
    except requests.RequestException as exc:
        print(f"[AVISO] Fallo descargando artefacto: {exc}")
        return None


def _desde_cadena(valor: str, api_key: str) -> bytes | None:
    if valor.startswith("http"):
        return _descargar(valor, api_key)
    try:
        return base64.b64decode(valor, validate=True)
    except Exception:
        return None


def _extraer_video(res: requests.Response, api_key: str) -> bytes | None:
    tipo = (res.headers.get("Content-Type") or "").lower()
    if "mp4" in tipo or "video/" in tipo or "octet-stream" in tipo or "binary" in tipo:
        return res.content or None
    if "json" not in tipo:
        return None
    try:
        datos: dict[str, Any] = res.json()
    except ValueError:
        return None
    for salida in datos.get("outputs") or []:
        data = salida.get("data") or []
        if not data or not isinstance(data[0], str):
            continue
        valor: str = data[0]
        if salida.get("name") == "status" and len(valor) < 4096:
            if "fail" in valor.lower() or "error" in valor.lower():
                print(f"[ERROR] El modelo reporto fallo: {valor[:200]}")
                return None
            continue
        video = _desde_cadena(valor, api_key)
        if _es_mp4(video):
            return video
    for clave in ("b64_video", "video", "b64_json", "output"):
        valor = datos.get(clave)
        if isinstance(valor, str) and len(valor) > 64:
            video = _desde_cadena(valor, api_key)
            if _es_mp4(video):
                return video
    artefactos = datos.get("artifacts") or []
    if artefactos and isinstance(artefactos[0], dict):
        artefacto = artefactos[0]
        inline = artefacto.get("base64") or artefacto.get("data")
        url = artefacto.get("url")
        for valor in (inline, url):
            if isinstance(valor, str) and valor:
                video = _desde_cadena(valor, api_key)
                if _es_mp4(video):
                    return video
    asset_url = datos.get("asset_url")
    if isinstance(asset_url, str) and asset_url.startswith("http"):
        video = _descargar(asset_url, api_key)
        if _es_mp4(video):
            return video
    print(f"[AVISO] Forma de respuesta no reconocida. Claves: {list(datos.keys())}")
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
        print("[NIM] Generando video en la nube... (poll)")
    return None


def _informar_sin_video(filas: list[dict[str, str]]) -> None:
    print("[INFO] Funciones de video entitled hoy: 0.")
    print("       NVIDIA rota funciones sin aviso; el catalogo de la cuenta manda.")
    print("       Rutas para desbloquear video:")
    print("       1. Entitlement NIM: build.nvidia.com -> cosmos-predict/ltx/wan -> 'Get API Key'")
    print("          (cuando la cuenta obtenga la funcion, este script la usara solo).")
    print("       2. Tier premium ya cableado: MCP muapi (kling, veo, hailuo...) con recarga.")
    print("       3. Trials gratuitos por API: WaveSpeed ($1), ApiPass (starter credits).")
    print("       4. Lanes manuales gratuitas (web): Kling 66 creditos/dia, Krea 100/dia, Flow 50/dia.")
    sys.exit(3)


def generar_video(args: argparse.Namespace) -> None:
    api_key = _leer_api_key()
    if not api_key:
        sys.exit(1)

    filas = _funciones_video(api_key)
    if not filas:
        _informar_sin_video(filas)

    objetivo = (args.modelo or "").lower().replace("-", "_").replace(".", "_")
    eleccion: dict[str, str] | None = None
    if objetivo:
        for f in filas:
            if f["modelo"].lower().replace("-", "_").replace(".", "_") == objetivo:
                eleccion = f
                break
        if not eleccion:
            print(f"[ERROR] '{args.modelo}' no es una funcion de video entitled hoy.")
    else:
        eleccion = filas[0]
    if not eleccion:
        print("[INFO] Disponibles:")
        for f in filas:
            print(f"       - {f['modelo']}")
        sys.exit(7)

    modelo = eleccion["modelo"]
    print(f"[NIM] Modelo de video: {modelo} (function_id={eleccion['function_id'][:8]}...)")

    prompt = _prompt_estilizado(args.prompt)
    # Familia cosmos-predict1: KServe command; resto: JSON simple con prompt+seed.
    if "predict1" in modelo.lower():
        cuerpo: dict[str, Any] = {"inputs": [
            {"name": "command", "shape": [1], "datatype": "BYTES",
             "data": [f'text2world --prompt="{prompt}" --seed={args.seed}']}]}
    else:
        cuerpo = {"prompt": prompt, "seed": args.seed}

    res = requests.post(
        f"{URL_PEXEC}/{eleccion['function_id']}",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json",
                 "Content-Type": "application/json"},
        json=cuerpo,
        timeout=90,
    )
    if res.status_code == 202:
        reqid = res.headers.get("NVCF-REQID")
        if not reqid:
            print("[ERROR] 202 sin NVCF-REQID.")
            sys.exit(6)
        print(f"[NIM] Trabajo aceptado (reqid={reqid[:8]}...). Sondeando NVCF...")
        res = _poll(reqid, api_key) or res
    if res.status_code != 200:
        print(f"[ERROR] NVCF respondio {res.status_code}: {res.text[:300]}")
        sys.exit(1)

    video = _extraer_video(res, api_key)
    if not _es_mp4(video):
        print("[ERROR] La respuesta no trajo video MP4 decodificable.")
        sys.exit(2)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, args.archivo)
    with open(out_path, "wb") as f:
        f.write(video)
    print(f"[EXITO] Video guardado en: {out_path}")
    print(f"[INFO] Modelo: {modelo} · {len(video) / 1_000_000:.1f} MB")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generacion de video NIM (catalogo vivo).")
    parser.add_argument("prompt", help="Prompt en ingles")
    parser.add_argument("archivo", help="Nombre del archivo de salida en output/videos/")
    parser.add_argument("--modelo", default="", help="Modelo de video del catalogo (opcional)")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    generar_video(args)


if __name__ == "__main__":
    main()

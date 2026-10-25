"""Generacion de voz (TTS) con el motor NVIDIA NIM — catalogo vivo, modelo agnostico.

Uso (terminal, desde la raiz del repositorio):
    python scripts/nvidia_tts.py "<TEXTO_EN_CUALQUIER_IDIOMA>" "<archivo>"
    python scripts/nvidia_tts.py "Hola, soy Nexus." bienvenida
    python scripts/nvidia_tts.py "Hola." test --modelo magpie-tts-multilingual

- --modelo acepta cualquier funcion de voz (TTS) del catalogo de la cuenta
  (ver: python scripts/media_catalogo.py, categoria audio). Por defecto:
  chatterbox-multilingual-tts (multilingual: espanol incluido).
- Mecanismo identico a scripts/nvidia_flux.py: NVCF pexec por function_id
  (catalogo consultado en vivo), candidatos de cuerpo con auto-correccion
  ante 400/422, y sondeo asincrono cuando NVCF responde 202.
- La clave se lee de D:/AI_Nexus_Core/.secrets/nvidia.key (la misma del
  proveedor LLM nvidia de opencode.json — creditos de desarrollador gratuitos).
- El audio se guarda en output/audio/<archivo>.<ext detectada> (wav/mp3/ogg).
- Estado (2026-10-24): las funciones TTS figuran ACTIVE en el catalogo pero con
  apiBodyFormat=CUSTOM (servidores Triton/gRPC, ownedByDifferentAccount): pexec
  responde 500/404 para cuerpos JSON. En preparacion: protocolo binario Triton.
  El motor de voz OPERATIVO hoy es VoiceStudio local (MCP/REST en :3900) y
  muapi premium; este script quedara listo para cuando el protocolo opere.
"""
import argparse
import base64
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

BASE_DIR = Path("D:/AI_Nexus_Core")
KEY_PATH = BASE_DIR / ".secrets" / "nvidia.key"
OUTPUT_DIR = BASE_DIR / "output" / "audio"

URL_FUNCIONES = "https://api.nvcf.nvidia.com/v2/nvcf/functions"
URL_PEXEC = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions"
URL_POLL = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status"
POLL_INTERVALO_S = 5
POLL_TOPE_S = 300

MODELO_DEFECTO = "chatterbox-multilingual-tts"
RE_TTS = r"tts|studiovoice"


def _leer_api_key() -> str | None:
    try:
        return KEY_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        print(f"[ERROR] No se encontro la clave en {KEY_PATH}")
        return None


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
        filas.append({"modelo": nombre.lower().replace("ai-", "", 1).strip(), "function_id": fn.get("id", "")})
    return filas


def _resolver_function_id(api_key: str, modelo: str) -> tuple[str, str]:
    """Busca el modelo de voz pedido en el catalogo vivo; exige categoria audio."""
    objetivo = modelo.lower().replace("-", "_").replace(".", "_")
    candidatas = [f for f in _catalogo(api_key) if re.search(RE_TTS, f["modelo"], re.IGNORECASE)]
    for f in candidatas:
        if f["modelo"].lower().replace("-", "_").replace(".", "_") == objetivo:
            return f["function_id"], f["modelo"]
    print(f"[ERROR] '{modelo}' no esta en el catalogo de voz (TTS) de esta cuenta.")
    print("[INFO] Modelos de voz disponibles hoy:")
    for f in candidatas:
        print(f"       - {f['modelo']}")
    sys.exit(7)


def _cuerpos_candidatos(texto: str) -> list[dict[str, Any]]:
    """Perfiles de cuerpo por familia + fallbacks genericos (la forma varia por NIM)."""
    # Chatterbox exige idioma BCP-47 (model card: "Language code required");
    # otros NIM de voz aceptan solo texto. Se itera ante 400/422/5xx.
    return [
        {"text": texto, "language": "es"},
        {"text": texto, "language": "es-CO"},
        {"text": texto, "language": "auto"},
        {"text": texto, "language": "es", "exaggeration": 0.5},
        {"text": texto},
        {"text": texto, "voice": "default"},
        {"input": texto},
    ]


def _detectar_ext(bytes_audio: bytes) -> str:
    if bytes_audio[:4] == b"RIFF":
        return "wav"
    if bytes_audio[:3] == b"ID3" or bytes_audio[:2] == b"\xff\xfb" or bytes_audio[:2] == b"\xff\xf3":
        return "mp3"
    if bytes_audio[:4] == b"OggS":
        return "ogg"
    if bytes_audio[:4] == b"fLaC":
        return "flac"
    return "bin"


def _descargar_si_url(valor: str) -> bytes | None:
    if valor.startswith(("http://", "https://")):
        try:
            res = requests.get(valor, timeout=120)
            if res.status_code == 200:
                return res.content
        except requests.RequestException:
            return None
    return None


def _extraer_audio(res_json: dict[str, Any]) -> bytes | None:
    """Busca el audio en las formas habituales de respuesta de los NIM de voz."""
    for bloque in (res_json, res_json.get("data") or {}, res_json.get("output") or {}):
        if not isinstance(bloque, dict):
            continue
        artifacts = bloque.get("artifacts")
        if isinstance(artifacts, list) and artifacts:
            b64 = artifacts[0].get("base64")
            if b64:
                return base64.b64decode(b64)
        for clave in ("audio", "b64_audio", "audio_base64", "b64", "data"):
            valor = bloque.get(clave)
            if isinstance(valor, str) and len(valor) > 64:
                if valor.startswith("http"):
                    descargado = _descargar_si_url(valor)
                    if descargado:
                        return descargado
                try:
                    return base64.b64decode(valor)
                except (ValueError, TypeError):
                    continue
        for clave in ("audio_url", "url", "audio_uri"):
            valor = bloque.get(clave)
            if isinstance(valor, str):
                descargado = _descargar_si_url(valor)
                if descargado:
                    return descargado
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
        print("[NIM] Sintetizando voz en la nube... (poll)")
    return None


def generar_voz(args: argparse.Namespace) -> None:
    api_key = _leer_api_key()
    if not api_key:
        sys.exit(1)

    function_id, modelo_real = _resolver_function_id(api_key, args.modelo)
    print(f"[NIM] Modelo de voz: {modelo_real} (function_id={function_id[:8]}...)")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    nombre = Path(args.archivo).stem
    cabeceras = {"Authorization": f"Bearer {api_key}", "Accept": "application/json",
                 "Content-Type": "application/json"}

    ultimo_error = ""
    for cuerpo in _cuerpos_candidatos(args.texto):
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
                audio = _extraer_audio(res.json())
            except ValueError:
                audio = None
            if audio:
                ext = _detectar_ext(audio)
                out_path = OUTPUT_DIR / f"{nombre}.{ext}"
                out_path.write_bytes(audio)
                print(f"[EXITO] Audio guardado en: {out_path}")
                print(f"[INFO] Modelo: {modelo_real} · {len(audio) / 1_000_000:.2f} MB · formato {ext}")
                return
            ultimo_error = "200 sin audio decodificable"
            continue
        if res.status_code in (400, 422, 500, 502, 503, 504):
            ultimo_error = f"{res.status_code}: {res.text[:160]}"
            continue  # cuerpo incorrecto o fallo transitorio -> probar el siguiente perfil
        print(f"[ERROR] NVCF respondio {res.status_code}: {res.text[:300]}")
        sys.exit(1)

    print(f"[ERROR] Ningun perfil de cuerpo funciono para {modelo_real}. Ultimo: {ultimo_error}")
    sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generacion de voz NIM (catalogo vivo).")
    parser.add_argument("texto", help="Texto a sintetizar (cualquier idioma del modelo)")
    parser.add_argument("archivo", help="Nombre del archivo de salida en output/audio/ (sin extension)")
    parser.add_argument("--modelo", default=MODELO_DEFECTO,
                        help="Modelo de voz del catalogo (media_catalogo.py, categoria audio)")
    args = parser.parse_args()
    generar_voz(args)


if __name__ == "__main__":
    main()

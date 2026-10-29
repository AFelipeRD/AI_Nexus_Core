"""Regenera la narración del tutorial v10.5 con texto LIMPIO (sin mojibake) y fonetizado.

Causa raíz corregida: segmentos.ts tenía mojibake («PA-dele una pA¡gina») y el TTS
leyó exactamente eso — audio trabado + "Ia nexus cors". Ahora:
  - "Éi Nexus Core" (fonética española de AI Nexus Core)
  - Tildes y eñes correctas (encoding="utf-8" en todo el pipeline)
  - Speeds por tono (1.05 gancho → 0.88 CTA)

Usa la API OpenAI-compatible de VoiceStudio (POST /v1/audio/speech, model tts-1,
voice 4af72ed9 = perfil nexus-presentador). Guarda WAV directo a disco.
Uso: python scripts/regenerar_narracion.py
"""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

API = "http://127.0.0.1:3900/v1/audio/speech"
VOICE = "4af72ed9"  # perfil «nexus-presentador»
OUT = Path(r"D:\Nexus_Remotion\public\audio")

# (id, texto limpio, speed por tono)
SEGMENTOS: list[tuple[str, str, float]] = [
    ("s0", "Éi Nexus Core. Tu computadora trabajando sola.", 1.05),
    ("s1", "Pídele una página para tu negocio. Y mírala nacer: planifica, diseña, programa y verifica. Sola.", 0.98),
    ("s2", "Se instala en dos minutos. Clona el repositorio, entra a la carpeta y ejecuta Opencode.", 0.96),
    ("s3", "Diecinueve agentes y cincuenta y una habilidades despiertan en tu terminal.", 0.95),
    ("s4", "Pide un tablero kanban. Y ahí está: construyéndose en vivo, con tu estilo.", 0.95),
    ("s5", "Imágenes, voz y video: motores reales, gratis por defecto, en tu propia máquina.", 0.92),
    ("s6", "Y cuando algo falla, el sistema se estudia a sí mismo, encuentra la causa y mejora cada día.", 0.90),
    ("s7", "Clona. Pide. Deja que el sistema evolucione.", 0.88),
]


def generar(sid: str, texto: str, speed: float) -> tuple[bool, int]:
    payload = json.dumps({
        "model": "tts-1", "input": texto, "voice": VOICE,
        "response_format": "wav", "speed": speed,
    }).encode("utf-8")
    req = urllib.request.Request(API, data=payload, headers={"Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=180)
        datos = r.read()
        if not datos.startswith(b"RIFF"):
            return False, 0
        (OUT / f"{sid}.wav").write_bytes(datos)
        return True, len(datos)
    except Exception as e:  # noqa: BLE001 — reporte accionable
        print(f"  {sid}: ERROR {e}")
        return False, 0


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ok = 0
    for sid, texto, speed in SEGMENTOS:
        print(f"{sid} (speed {speed}): {texto[:60]}...")
        exito, nb = generar(sid, texto, speed)
        if exito:
            ok += 1
            print(f"  -> {nb} bytes")
        time.sleep(1.0)
    print(f"\n{ok}/8 segmentos generados")
    return 0 if ok == 8 else 1


if __name__ == "__main__":
    raise SystemExit(main())

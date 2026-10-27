"""Mezclador de audio v9 — pipeline determinista 100 % local (solo stdlib).

Pasos:
 1. Mide duraciones REALES de public/audio/s[0-7].wav (ffprobe).
 2. Normaliza narracion loudnorm I=-16 TP=-1.5 LRA=11 -> public/audio/v9/sX_n.wav (48 kHz estéreo).
 3. Escribe src/segmentos_reales.ts con duraciones reales (fuente de verdad de la composicion).
 4. Construye public/audio/bgm_mezcla.wav: BGM resampleado a 48 kHz, normalizado a RMS -20 dBFS,
    compas-loop de 2 s, ducking 0.32 bajo voz (attack instantaneo, release 0.25 s), fades 0.5/1.2 s.
 5. Copia SFX de media-use (Pixabay, credito documentado) a public/audio/sfx/.
 6. Imprime la tabla de inicios reales.

Uso: python scripts/mezclar_v9.py
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import wave
from array import array
from pathlib import Path

BASE = Path(r"D:\Nexus_Remotion")
AUDIO = BASE / "public" / "audio"
V9 = AUDIO / "v9"
SFX_SRC = Path(r"D:\AI_Nexus_Core\.agents\skills\media-use\audio\assets\sfx")
SFX_DST = AUDIO / "sfx"

SR = 48000
AIRE = 0.5
COLA = 0.4
COLA_FINAL = 1.5
BAR_S = 2.0
IDZ = [f"s{i}" for i in range(8)]
SFX_ELEGIDOS = ["whoosh.mp3", "whoosh-short.mp3", "click.mp3", "click-soft.mp3",
                "impact-bass-1.mp3", "riser.mp3", "sparkle.mp3", "pop.mp3"]


def ffprobe_dur(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", str(p)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    mm = re.search(r'"duration":\s*"?([\d.]+)"?', out)
    return float(mm.group(1)) if mm else 0.0


def leer_wav_mono(p: Path) -> tuple[array, int]:
    """PCM16 -> floats mono [-1,1]."""
    with wave.open(str(p), "rb") as w:
        sr = w.getframerate()
        ncan = w.getnchannels()
        if w.getsampwidth() != 2:
            raise SystemExit(f"{p.name}: requerido PCM16")
        raw = w.readframes(w.getnframes())
    n = len(raw) // (2 * ncan)
    d = array("h")
    d.frombytes(raw)
    mono = array("d", [0.0] * n)
    if ncan == 1:
        for i in range(n):
            mono[i] = d[i] / 32768.0
    else:
        for i in range(n):
            mono[i] = (d[i * ncan] + d[i * ncan + 1]) / (2.0 * 32768.0)
    return mono, sr


def resamplea(muestras: array, sr_in: int, sr_out: int) -> array:
    if sr_in == sr_out:
        return muestras
    raz = sr_out / sr_in
    n_out = int(len(muestras) * raz)
    out = array("d", [0.0] * n_out)
    for j in range(n_out):
        x = j / raz
        i0 = int(x)
        f = x - i0
        i1 = min(i0 + 1, len(muestras) - 1)
        out[j] = muestras[i0] * (1 - f) + muestras[i1] * f
    return out


def guardar_stereo(p: Path, muestras: array, sr: int = SR) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    con = array("h", [0] * (len(muestras) * 2))
    for i, v in enumerate(muestras):
        x = max(-32767, min(32767, int(v * 32767)))
        con[2 * i] = x
        con[2 * i + 1] = x
    with wave.open(str(p), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(con.tobytes())


def rms_dbfs(v: array) -> float:
    if not v:
        return -99.0
    s = sum(x * x for x in v) / len(v)
    return 10 * math.log10(s) if s > 1e-12 else -99.0


def normalizar_narracion() -> dict[str, float]:
    reales: dict[str, float] = {}
    for sid in IDZ:
        src = AUDIO / f"{sid}.wav"
        dst = V9 / f"{sid}_n.wav"
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2", str(dst)],
            check=True, capture_output=True)
        reales[sid] = ffprobe_dur(dst)
        print(f"  {sid}: {reales[sid]:.2f}s (normalizado)")
    return reales


def escribir_segmentos(reales: dict[str, float]) -> None:
    textos = {}
    for a, b, _ in re.findall(r'id:\s*"([^"]+)",\s*text:\s*"([^"]*)",\s*duracion:\s*([\d.]+)',
                              (BASE / "src" / "segmentos.ts").read_text(encoding="utf-8")):
        textos[a] = b
    lineas = ["// DURACIONES REALES medidas por ffprobe (mezclar_v9.py) — NO editar a mano."]
    lineas.append("export const SEGMENTOS = [")
    for sid in IDZ:
        lineas.append(f'  {{ id: "{sid}", text: {json.dumps(textos[sid], ensure_ascii=False)}, duracion: {reales[sid]:.2f} }},')
    lineas.append("];")
    (BASE / "src" / "segmentos_reales.ts").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def construir_bgm(reales: dict[str, float]) -> float:
    bgm, sr_bgm = leer_wav_mono(AUDIO / "bgm.wav")
    bgm = resamplea(bgm, sr_bgm, SR)
    # puntos de inicio de cada escena en el timeline
    inicios = [AIRE + COLA * i + sum(list(reales.values())[:i]) for i in range(8)]
    total = AIRE + sum(reales[s] + COLA for s in IDZ) - COLA + COLA_FINAL
    total_m = int(total * SR)
    # compas-loop hasta cubrir
    largo_bar = int(BAR_S * SR)
    while len(bgm) < total_m:
        bgm.extend(bgm[:min(largo_bar, total_m - len(bgm))])
    bgm = bgm[:total_m]
    # normalizar a RMS -20 dBFS
    r = rms_dbfs(bgm[: SR * 5])
    if r > -89:
        g = 10 ** ((-20.0 - r) / 20.0)
        bgm = array("d", [v * g for v in bgm])
    # gate de voz por bins de 10 ms
    hop_s, win_s = 0.01, 0.02
    n_bins = int(total / hop_s) + 1
    activo = bytearray(n_bins)
    for idx, sid in enumerate(IDZ):
        voz, _ = leer_wav_mono(V9 / f"{sid}_n.wav")
        voz_sr_est = reales[sid]
        vozm = voz if len(voz) else voz
        t0 = inicios[idx]
        # barrido por bins dentro de la escena
        fin_escena = t0 + reales[sid] + COLA
        b = int(t0 / hop_s)
        while b < n_bins and b * hop_s < fin_escena:
            local = b * hop_s - t0
            if 0 <= local * SR < len(vozm) - 1:
                vseg = vozm[int(local * SR): int(local * SR) + int(win_s * SR)]
                if rms_dbfs(vseg) > -45:
                    activo[b] = 1
            b += 1
    # envolvente: subida instantanea al entrar voz; caida 1/rel por bin al salir
    rel_bins = int(0.25 / hop_s)
    env = array("d", [1.0] * n_bins)
    nivel = 0.0
    for b in range(n_bins):
        if activo[b]:
            nivel = 1.0
        elif nivel > 0:
            nivel = max(0.0, nivel - 1.0 / rel_bins)
        env[b] = 0.32 + 0.68 * nivel
    # aplicar ducking + fades
    fade_in, fade_out = int(0.5 * SR), int(1.2 * SR)
    for i in range(total_m):
        v = bgm[i] * env[min(i // int(hop_s * SR), n_bins - 1)]
        if i < fade_in:
            v *= i / fade_in
        if i >= total_m - fade_out:
            v *= (total_m - 1 - i) / fade_out
        bgm[i] = v
    guardar_stereo(AUDIO / "bgm_mezcla.wav", bgm)
    print("  bgm_mezcla.wav listo:", round(total, 2), "s")
    return total


def copiar_sfx() -> None:
    SFX_DST.mkdir(parents=True, exist_ok=True)
    n = 0
    for nombre in SFX_ELEGIDOS:
        s = SFX_SRC / nombre
        if s.exists():
            (SFX_DST / nombre).write_bytes(s.read_bytes())
            n += 1
    print("  sfx copiados:", n)


def main() -> None:
    V9.mkdir(parents=True, exist_ok=True)
    print("1) normalizando narracion (loudnorm -> -16 LUFS):")
    reales = normalizar_narracion()
    print("2) escribiendo segmentos_reales.ts:")
    escribir_segmentos(reales)
    print("3) mezclando BGM con ducking:")
    total = construir_bgm(reales)
    print("4) copiando SFX:")
    copiar_sfx()
    inicios = [round(AIRE + COLA * i + sum(list(reales.values())[:i]), 2) for i in range(8)]
    print("5) TABLA TIMELINE REAL:")
    for sid, ini in zip(IDZ, inicios):
        print(f"   {sid}: inicio {ini:6.2f}s  duracion {reales[sid]:5.2f}s  fin {ini + reales[sid] + COLA:.2f}s")
    frames = int(math.ceil(total * 30)) + 10
    print(f"6) total {total:.2f}s -> durInFrames recomendado: {frames} @30fps")


if __name__ == "__main__":
    main()

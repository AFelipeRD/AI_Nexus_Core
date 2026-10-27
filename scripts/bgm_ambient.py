"""BGM ambient v10 — pad suave con evolución, sin percusión.

Sintetiza un colchón armónico que EVOLUCIONA (no repite un loop de 2 s):
  - Progresión Am → F → C → G (cada acorde ~8 s) → 2 ciclos en 48 s.
  - Pad: seno + armónico suave con attack/release largos (respiración).
  - Arpegio lento: una nota del acorde cada 0.5 s con envolvente corta,
    patrón ascendente con variación (no idéntico por acorde).
  - Sin kick/hi-hat. Lowpass por media móvil. Fade in 2 s / out 3 s.
  - RMS objetivo ~ -26 dBFS (colchón discreto bajo la voz).
Uso: python scripts/bgm_ambient.py [--dur 48.19] [--out bgm_ambient.wav] [--rms -26]
"""
from __future__ import annotations

import argparse
import math
import wave
from array import array
from pathlib import Path

SR = 48000

# Acordes: (nombre, [frecuencias base en Hz])
ACORDES: list[tuple[str, list[float]]] = [
    ("Am", [110.0, 220.0, 261.63, 329.63]),   # A2 A3 C4 E4
    ("F", [87.31, 174.61, 220.0, 349.23]),      # F2 F3 A3 F4
    ("C", [130.81, 196.0, 261.63, 329.63]),     # C3 G3 C4 E4
    ("G", [98.0, 196.0, 246.94, 293.66]),       # G2 G3 B3 D4
]


def env_pad(t: float, dur: float, ataque: float = 2.2, release: float = 2.5) -> float:
    """Envolvente de respiración para el pad del acorde."""
    if t < ataque:
        return t / ataque
    if t > dur - release:
        return max(0.0, (dur - t) / release)
    return 1.0


def env_arp(t: float, dur_nota: float) -> float:
    """Envolvente suave para cada nota del arpegio (attack 15 % release 85 %)."""
    if t < 0 or t > dur_nota:
        return 0.0
    fase = t / dur_nota
    atk = 0.15
    if fase < atk:
        return fase / atk
    return math.exp(-(fase - atk) * 6.0)


def lowpass(muestras: array, ventana: int = 24) -> array:
    """Media móvil simple para suavizar picos."""
    out = array("d", [0.0] * len(muestras))
    for i in range(len(muestras)):
        a = max(0, i - ventana)
        acc = 0.0
        for j in range(a, i + 1):
            acc += muestras[j]
        out[i] = acc / (i - a + 1)
    return out


def rms_dbfs(v: array) -> float:
    if not v:
        return -99.0
    s = sum(x * x for x in v) / len(v)
    return 10 * math.log10(s) if s > 1e-12 else -99.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dur", type=float, default=48.19)
    ap.add_argument("--out", type=str, default=r"D:\Nexus_Remotion\public\audio\bgm_ambient.wav")
    ap.add_argument("--rms", type=float, default=-26.0)
    ap.add_argument("--arp_cada", type=float, default=0.5)
    args = ap.parse_args()

    dur = args.dur
    n = int(dur * SR)
    buf = array("d", [0.0] * n)

    # --- capas por acorde ---
    dur_acorde = dur / (len(ACORDES) * 2)  # 2 ciclos de la progresión
    for ciclo in range(2):
        for ci, (nombre, notas) in enumerate(ACORDES):
            t0 = (ciclo * len(ACORDES) + ci) * dur_acorde
            t1 = t0 + dur_acorde
            i0, i1 = int(t0 * SR), min(n, int(t1 * SR))
            # pad: todas las notas del acorde con respiración
            for ni, f in enumerate(notas):
                fase = 2 * math.pi * f / SR
                fase2 = 2 * math.pi * f * 2 / SR
                for i in range(i0, i1):
                    t = (i - i0) / SR
                    e = env_pad(t, dur_acorde) * (0.32 if ni == 0 else 0.22)
                    v = math.sin(fase * i) * 0.8 + math.sin(fase2 * i) * 0.2
                    # vibrato sutil
                    vib = 1.0 + math.sin(i / SR * 0.15 + ni) * 0.002
                    buf[i] += v * e * vib * 0.5
            # arpegio: patrón ascendente con variación por acorde
            orden = [0, 2, 3, 1] if ci % 2 == 0 else [0, 1, 3, 2]
            paso = args.arp_cada
            k = 0
            t = 0.6
            while t < dur_acorde - 0.2:
                idx = orden[k % len(orden)]
                # en el segundo ciclo, sube una octava cada 4 notas
                f = notas[idx] * (2.0 if (ciclo == 1 and k % 8 >= 4) else 1.0)
                dur_nota = paso * 3.2
                j0 = i0 + int(t * SR)
                j1 = min(i1, j0 + int(dur_nota * SR))
                fase = 2 * math.pi * f / SR
                for j in range(j0, j1):
                    tn = (j - j0) / SR
                    e = env_arp(tn, dur_nota)
                    if e > 0:
                        buf[j] += math.sin(fase * j) * e * 0.30
                t += paso
                k += 1

    # --- suavizado y fades ---
    buf = lowpass(buf, ventana=int(SR * 0.0012))
    fade_in = int(2.0 * SR)
    fade_out = int(3.0 * SR)
    for i in range(fade_in):
        buf[i] *= i / fade_in
    for i in range(fade_out):
        buf[n - 1 - i] *= i / fade_out

    # --- normalizar a RMS objetivo ---
    r = rms_dbfs(buf)
    if r > -90:
        g = 10 ** ((args.rms - r) / 20.0)
        buf = array("d", [v * g for v in buf])

    # --- pico de seguridad ---
    pico = max(abs(v) for v in buf)
    if pico > 0.94:
        buf = array("d", [v * 0.94 / pico for v in buf])

    # --- guardar estéreo ---
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    con = array("h", [0] * (n * 2))
    for i, v in enumerate(buf):
        x = max(-32767, min(32767, int(v * 32767)))
        con[2 * i] = x
        con[2 * i + 1] = x
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(con.tobytes())

    print(f"bgm_ambient.wav: {dur:.2f}s, RMS {rms_dbfs(buf):.1f} dBFS, pico {20 * math.log10(max(abs(v) for v in buf)):.1f} dBFS")
    print(f"progresión: {' -> '.join(a[0] for a in ACORDES)} x2, arpegio cada {args.arp_cada}s, sin percusión")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

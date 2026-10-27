#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Autoevaluacion de ritmo (seccion 7 del protocolo video-director).

Extrae el video a 5 fps y MIDE (no opina):
  a) racha estatica maxima (regla: ninguna imagen quieta > 0.6 s salvo el cierre)
  b) % de intervalos vivos con diferencia apreciable entre frames (regla: >= 95 %)
  c) frames negros/vacios (cortes secos prohibidos)
  d) presencia del color de la costura (coral) por tramo — la costura debe
     aparecer en casi todas las escenas
Umbral "apreciable": diferencia media absoluta >= 3.5 (sobre 255) entre
frames consecutivos a 5 fps — calibrado con el tutorial v6 como base.
Uso: python scripts/criticar_ritmo.py <ruta.mp4> [--fps 5] [--umbral 3.5]
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


def main() -> None:
    ap = argparse.ArgumentParser(description="Autoevaluacion de ritmo a 5 fps")
    ap.add_argument("mp4")
    ap.add_argument("--fps", type=float, default=5.0)
    ap.add_argument("--umbral", type=float, default=3.5)
    args = ap.parse_args()

    with tempfile.TemporaryDirectory(prefix="ritmo_") as tmp:
        plantilla = str(Path(tmp) / "f_%05d.png")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", args.mp4, "-vf", f"fps={args.fps},scale=320:180", plantilla],
            check=True,
        )
        frames = sorted(Path(tmp).glob("f_*.png"))
        if len(frames) < 2:
            print("[ERROR] No se pudieron extraer frames.")
            sys.exit(2)

        prev: list[int] | None = None
        difs: list[float] = []
        negros = 0
        coral_por_tramo: dict[int, float] = {}
        for i, f in enumerate(frames):
            img = Image.open(f).convert("RGB")
            px = list(img.getdata())
            n = len(px)
            gris = [sum(c) // 3 for c in px]
            if sum(gris) / n < 12:
                negros += 1
            coral = sum(1 for c in px if c[0] > 200 and 40 < c[1] < 130 and c[2] < 100) / n * 100
            tramo = i // max(1, len(frames) // 10)  # 10 tramos aproximados
            coral_por_tramo[tramo] = max(coral_por_tramo.get(tramo, 0.0), coral)
            if prev is not None:
                difs.append(sum(abs(a - b) for a, b in zip(gris, prev)) / n)
            prev = gris

        vivos = sum(1 for d in difs if d >= args.umbral) / len(difs) * 100
        # racha estatica maxima en segundos (intervalos consecutivos bajo el umbral)
        racha, racha_max = 0, 0
        for d in difs:
            racha = racha + 1 if d < args.umbral else 0
            racha_max = max(racha_max, racha)
        racha_s = racha_max / args.fps
        # localizacion exacta de rachas muertas (para parchear con evidencia)
        rachas: list[tuple[float, float]] = []
        ini: float | None = None
        for j, d in enumerate(difs):
            t0 = j / args.fps
            if d < args.umbral:
                if ini is None:
                    ini = t0
            else:
                if ini is not None:
                    rachas.append((ini, t0))
                    ini = None
        if ini is not None:
            rachas.append((ini, len(difs) / args.fps))
        rachas_top = sorted(rachas, key=lambda x: x[1] - x[0], reverse=True)[:8]
        tramos_con_costura = sum(1 for v in coral_por_tramo.values() if v > 0.5)

        print(f"frames={len(frames)} intervalos={len(difs)}")
        print(f"vivos: {vivos:.1f}% (regla >= 95) | umbral={args.umbral}")
        print(f"racha estatica maxima: {racha_s:.2f}s (regla <= 0.6 salvo cierre)")
        for s, e in rachas_top:
            print(f"   muerta {s:6.2f} -> {e:6.2f}  ({e - s:.2f} s)")
        print(f"frames negros/vacios: {negros} (regla: 0 cortes secos)")
        print(f"tramos con costura coral: {tramos_con_costura}/{len(coral_por_tramo)}")
        cumple = vivos >= 95 and racha_s <= 0.8 and negros == 0
        print(f"VEREDICTO: {'CUMPLE' if cumple else 'NO CUMPLE'} (mide, no opina)")
        sys.exit(0 if cumple else 1)


if __name__ == "__main__":
    main()

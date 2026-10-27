"""Auditoría de canvas v10: desbordes de texto en bordes y esquinas vacías.

Para cada frame (a N fps): 
  a) BORDES: contenido con contraste alto en los últimos 15 px del frame
     (texto recortándose contra la resolución) -> desbordes con timestamp.
  b) ESQUINAS VACÍAS: divide el frame en 4 cuadrantes y mide desviación
     estándar de luminancia; valores < 8 = esquina muerta (sin contenido).
Uso: python scripts/auditar_canvas.py <video.mp4> [--fps 2] [--umbral_std 8]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image
import math


def main() -> int:
    ap = argparse.ArgumentParser(description="Auditoría de composición: desbordes y esquinas vacías")
    ap.add_argument("mp4")
    ap.add_argument("--fps", type=float, default=2.0)
    ap.add_argument("--umbral_std", type=float, default=8.0)
    ap.add_argument("--margen_px", type=int, default=15)
    args = ap.parse_args()

    with tempfile.TemporaryDirectory(prefix="canvas_") as tmp:
        plantilla = str(Path(tmp) / "f_%05d.jpg")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", args.mp4, "-vf", f"fps={args.fps}", "-q:v", "2", plantilla],
            check=True,
        )
        frames = sorted(Path(tmp).glob("f_*.jpg"))
        if not frames:
            print("[ERROR] Sin frames")
            return 2

        desbordes: list[tuple[float, str]] = []
        esquinas_muertas: dict[str, int] = {"TL": 0, "TR": 0, "BL": 0, "BR": 0}
        w_half = h_half = 0
        for i, f in enumerate(frames):
            t = i / args.fps
            img = Image.open(f).convert("L")
            w, h = img.size
            w_half, h_half = w // 2, h // 2
            m = args.margen_px
            px = img.load()
            # a) desbordes: contraste en franja de borde
            for lado in ("izq", "der", "sup", "inf"):
                if lado == "izq":
                    franja = [px[x, y] for x in range(m) for y in range(0, h, 4)]
                elif lado == "der":
                    franja = [px[x, y] for x in range(w - m, w) for y in range(0, h, 4)]
                elif lado == "sup":
                    franja = [px[x, y] for y in range(m) for x in range(0, w, 4)]
                else:
                    franja = [px[x, y] for y in range(h - m, h) for x in range(0, w, 4)]
                if not franja:
                    continue
                mx = max(franja)
                mn = min(franja)
                # contraste alto en el borde = contenido tocándolo (texto recortándose)
                if mx - mn > 90 and mx > 160:
                    desbordes.append((t, f"{lado} (max={mx} min={mn})"))
            # b) esquinas vacías: std de luminancia por cuadrante
            for nombre, box in {
                "TL": (0, 0, w_half, h_half),
                "TR": (w_half, 0, w, h_half),
                "BL": (0, h_half, w_half, h),
                "BR": (w_half, h_half, w, h),
            }.items():
                q = img.crop(box)
                datos = list(q.getdata())
                n = len(datos)
                media = sum(datos) / n
                std = math.sqrt(sum((d - media) ** 2 for d in datos) / n)
                if std < args.umbral_std:
                    esquinas_muertas[nombre] += 1

        total = len(frames)
        print(f"frames={total} fps={args.fps} margen={args.margen_px}px umbral_std={args.umbral_std}")
        print(f"\n=== DESBORDES (contenido de alto contraste tocando el borde) ===")
        if desbordes:
            # agrupar por lado y rangos de tiempo
            por_lado: dict[str, list[tuple[float, str]]] = {}
            for t, info in desbordes:
                lado = info.split(" ")[0]
                por_lado.setdefault(lado, []).append((t, info))
            for lado, lst in sorted(por_lado.items()):
                rangos = []
                ini = lst[0][0]
                prev = lst[0][0]
                for t, _ in lst[1:]:
                    if t - prev > 1.5 / args.fps:
                        rangos.append((ini, prev))
                        ini = t
                    prev = t
                rangos.append((ini, prev))
                top = sorted(rangos, key=lambda x: x[1] - x[0], reverse=True)[:6]
                print(f"  {lado}: {len(lst)} frames | rangos: " + ", ".join(f"{a:.1f}-{b:.1f}s" for a, b in top))
        else:
            print("  ninguno")
        print(f"\n=== ESQUINAS MUERTAS (std < {args.umbral_std}) ===")
        for nombre, n in esquinas_muertas.items():
            pct = n / total * 100
            marca = "VACIA" if pct > 40 else ("parcial" if pct > 15 else "viva")
            print(f"  {nombre}: {n}/{total} frames ({pct:.0f}%) {marca}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

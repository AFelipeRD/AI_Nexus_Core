"""Inspección del personaje Pixel: dimensiones, paleta y estructura del SVG."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from PIL import Image

BASE = Path(r"D:\AI_Nexus_Core\assets\character")

for n in ("pixel_cara.png", "pixel_cara_1x.png"):
    img = Image.open(BASE / n)
    print(f"{n}: {img.size} {img.mode}")
    small = img.convert("RGBA").resize((48, 48))
    q = small.quantize(colors=6)
    pal = q.getpalette()
    for cnt, idx in sorted(q.getcolors(), reverse=True)[:6]:
        r, g, b = pal[idx * 3: idx * 3 + 3]
        print(f"   {cnt / (48 * 48) * 100:5.1f}%  #{r:02X}{g:02X}{b:02X}")

svg = (BASE / "pixel_cara.svg").read_text(encoding="utf-8")
vb = re.search(r'viewBox="([^"]+)"', svg)
w = re.search(r'width="([^"]+)"', svg)
h = re.search(r'height="([^"]+)"', svg)
print(f"SVG: viewBox={vb.group(1) if vb else 'NO'} width={w.group(1) if w else 'NO'} height={h.group(1) if h else 'NO'} bytes={len(svg)}")
cols = Counter(re.findall(r'fill="(#[0-9A-Fa-f]{6})"', svg))
print("Colores SVG:", cols.most_common(10))
elems = Counter(re.findall(r"<(rect|circle|path|ellipse|polygon|image|g)\b", svg))
print("Elementos:", dict(elems))
# ¿tiene animación o <image> embebido?
print("¿<image>?:", "<image" in svg, "| ¿animate?:", "<animate" in svg, "| ¿data URI?:", "data:" in svg)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BGM sintetizado en codigo puro (stdlib) a 120 BPM — leccion 22.
Kick en cada beat, hi-hat en los offbeats, bajo con patron A-A-E-G y
lead arpegiado suave; 30 s exactos (60 beats), fade in/out, mono 44.1 kHz.
Salida: D:/Nexus_Remotion/public/audio/bgm.wav
"""
import math
import struct
import wave
from pathlib import Path

SR = 44100
BPM = 120.0
BEAT = 60.0 / BPM          # 0.5 s
DUR = 30.0
N = int(SR * DUR)
OUT = Path("D:/Nexus_Remotion/public/audio/bgm.wav")

def seno(frec: float, t: float) -> float:
    return math.sin(2 * math.pi * frec * t)

def kick(t: float) -> float:
    """Golpe: seno con caida de tono y envolvente exponencial."""
    if t < 0 or t > 0.22:
        return 0.0
    f = 52 * math.exp(-t * 22) + 40
    return seno(f, t) * math.exp(-t * 16)

def hat(t: float) -> float:
    """Hi-hat: ruido con caida rapidisima."""
    if t < 0 or t > 0.05:
        return 0.0
    import random
    random.seed(int(t * 1e6) + 7)
    return (random.random() * 2 - 1) * math.exp(-t * 90) * 0.5

def bajo(nota: float, t: float, dur: float) -> float:
    if t < 0 or t > dur:
        return 0.0
    return seno(nota, t) * math.exp(-t * 3.2) * 0.55

def lead(nota: float, t: float) -> float:
    if t < 0 or t > 0.42:
        return 0.0
    env = math.exp(-t * 6) * min(1.0, t * 160)
    return seno(nota, t) * env * 0.22

A2, E2, G2 = 110.0, 82.41, 98.0
A4, CS5, E5, A5 = 440.0, 554.37, 659.26, 880.0
patron_bajo = [A2, A2, E2, G2]
arpegio = [A4, CS5, E5, A5, E5, CS5, A4, E5]

muestras = [0.0] * N
for i in range(N):
    t = i / SR
    # beats y compases
    beat_idx = int(t / BEAT)
    t_beat = t - beat_idx * BEAT
    sub_bar = beat_idx // 4
    # kick en cada beat (mas suave en compases pares para respirar)
    g = kick(t_beat) * (0.9 if sub_bar % 2 == 0 else 0.62)
    # hat en offbeat
    g += hat(t_beat - BEAT / 2)
    # bajo por beat
    g += bajo(patron_bajo[beat_idx % 4], t_beat, BEAT * 1.05)
    # lead en corcheas
    if beat_idx >= 4:  # entra despues del gancho
        corchea = int(t / (BEAT / 2)) % 8
        g += lead(arpegio[corchea], t % (BEAT / 2))
    # fade global in/out
    fade = min(1.0, t / 0.5, (DUR - t) / 0.8)
    val = g * 0.5 * fade
    # soft clip
    muestras[i] = math.tanh(val)

OUT.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(OUT), "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = b"".join(struct.pack("<h", int(max(-1.0, min(1.0, m)) * 32000)) for m in muestras)
    w.writeframes(frames)
print(f"BGM listo: {OUT} ({DUR}s, {BPM} BPM, {len(muestras)} muestras)")

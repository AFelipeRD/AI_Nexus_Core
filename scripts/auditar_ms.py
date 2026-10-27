"""Auditor milisegundo de video + audio (estandar v9 de videos).

Evidencia: (1) duraciones reales de los WAV vs lo declarado en segmentos,
(2) barras de vida visual a 10 muestras/s (rachas estaticas con rango exacto),
(3) nivel de mezcla por ~100 ms (silencios, clipping, RMS).
Sin dependencias externas: solo stdlib + ffmpeg/ffprobe en PATH.
Uso: python scripts/auditar_ms.py <video.mp4> [--wavs <carpeta>]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

BIN_STREAK = 0.2   # s por bin de vida visual
BIN_AUDIO = 0.1    # s por bin de audio (~5 frames de audio a 48 kHz)
YDIF_SECO = 1.00   # umbral de movimiento PERCEPTIBLE (grain solo llega a ~0.3; elementos vivos > 1)


def _run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout + "\n" + r.stderr


def ffprobe_json(path: Path) -> dict:
    out = _run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    m = re.search(r"\{.*\}", out, re.S)
    return json.loads(m.group(0)) if m else {}


def rachas_visuales(path: Path, fps_out: float = 10.0) -> dict:
    """YDIF medio por bin -> rachas sin movimiento, con rangos exactos."""
    ff = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf",
         f"fps={fps_out},signalstats,metadata=print:file=-", "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    pares: list[tuple[float, float]] = []
    t_pend: float | None = None
    for linea in ff.stdout:  # type: ignore[union-attr]
        if "pts_time:" in linea:
            tm = re.search(r"pts_time:([\d.]+)", linea)
            if tm:
                t_pend = float(tm.group(1))
        else:
            vm = re.search(r"signalstats\.YDIF=([\d.]+|-Inf)", linea)
            if vm and t_pend is not None:
                val = 0.0 if vm.group(1) in ("-Inf", "inf") else float(vm.group(1))
                pares.append((t_pend, val))
                t_pend = None
    ff.wait()
    if not pares:
        return {"error": "sin muestras YDIF"}
    bins: dict[int, list[float]] = {}
    for t, v in pares:
        bins.setdefault(int(t // BIN_STREAK), []).append(v)
    medias = sorted((b * BIN_STREAK, sum(vs) / len(vs)) for b, vs in bins.items())
    rachas: list[tuple[float, float]] = []
    inicio: float | None = None
    fin_anterior = medias[-1][0] + BIN_STREAK
    for t, m in medias:
        if m < YDIF_SECO:
            if inicio is None:
                inicio = t
        else:
            if inicio is not None and t - inicio >= BIN_STREAK - 1e-9:
                rachas.append((inicio, t))
            inicio = None
    if inicio is not None and fin_anterior - inicio >= BIN_STREAK - 1e-9:
        rachas.append((inicio, fin_anterior))
    vivos = sum(1 for _, m in medias if m >= YDIF_SECO)
    return {
        "umbral_ydif": YDIF_SECO,
        "muestras": len(pares),
        "bins": len(medias),
        "pct_vivos": round(100 * vivos / len(medias), 1),
        "racha_max_s": round(max((e - s for s, e in rachas), default=0.0), 2),
        "rachas_top": [{"desde_s": round(s, 2), "hasta_s": round(e, 2), "dur_s": round(e - s, 2)}
                       for s, e in sorted(rachas, key=lambda x: x[1] - x[0], reverse=True)[:10]],
    }


def _num(txt: str) -> float | None:
    try:
        f = float(txt)
        return None if f != f else f  # NaN -> None
    except ValueError:
        return None


def audio_por_100ms(path: Path) -> dict:
    """RMS/pico del audio por frame real con pts_time: silencios y clipping reales."""
    out = _run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-af",
                "astats=metadata=1:reset=1:measure_perchannel=none,ametadata=print:file=-", 
                "-f", "null", "-"])
    # secuencia: frame header (pts_time) -> tags de ese frame
    serie: list[tuple[float, float]] = []  # (t, rms)
    picos: list[float] = []
    t_actual = 0.0
    rms_pend: float | None = None
    for linea in out.splitlines():
        tm = re.search(r"pts_time:([\d.]+)", linea)
        if tm:
            t_actual = float(tm.group(1))
            continue
        mk = re.search(r"astats\.Overall\.RMS_level=(\S+)", linea)
        pk = re.search(r"astats\.Overall\.Peak_level=(\S+)", linea)
        if mk:
            v = _num(mk.group(1))
            if v is not None and rms_pend is None:
                rms_pend = -99.0 if v <= -99.5 else min(v, 12.0)
        if pk:
            v = _num(pk.group(1))
            if v is not None:
                picos.append(-99.0 if v <= -99.5 else min(v, 12.0))
        if rms_pend is not None and pk:
            serie.append((t_actual, rms_pend))
            rms_pend = None
    if not serie:
        return {"error": "sin muestras astats"}
    bins_audio = 1024 / 48000  # tamaño real del frame de audio astats (~21.33 ms a 48 kHz)
    bajos = [t for t, r in serie if r < -45]
    silencios: list[list[float]] = []
    if bajos:
        ini, prev = bajos[0], bajos[0]
        for t in bajos[1:]:
            if t - prev > bins_audio * 12:
                silencios.append([round(ini, 2), round(prev + bins_audio, 2)])
                ini = t
            prev = t
        silencios.append([round(ini, 2), round(prev + bins_audio, 2)])
    pico_max = max(picos) if picos else -99.0
    return {
        "rms_medio_db": round(sum(r for _, r in serie) / len(serie), 1),
        "pico_max_db": round(pico_max, 1),
        "clipping_riesgo": pico_max >= -1.0,
        "silencio_inicial_s": round(serie[0][0] if serie[0][1] < -45 else 0.0, 2),
        "gaps_mayores_0.4s": [g for g in silencios if g[1] - g[0] >= 0.4][:12],
        "frames_audio": len(serie),
    }


def compara_wavs(carpeta: Path, declarado: dict[str, float]) -> list[dict]:
    filas: list[dict] = []
    for sid, dur in declarado.items():
        wav = carpeta / f"{sid}.wav"
        if not wav.exists():
            filas.append({"id": sid, "declarado": dur, "real": None, "delta_ms": None})
            continue
        info = ffprobe_json(wav)
        real = float(info.get("format", {}).get("duration", 0.0))
        filas.append({"id": sid, "declarado": dur, "real": round(real, 2),
                      "delta_ms": round((real - dur) * 1000)})
    return filas


def declarado_desde_segmentos(ruta_ts: Path) -> dict[str, float]:
    texto = ruta_ts.read_text(encoding="utf-8", errors="replace")
    pares = re.findall(r'id:\s*"([^"]+)",\s*text:\s*"([^"]*)",\s*duracion:\s*([\d.]+)', texto)
    return {a: float(c) for a, _, c in pares}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    video = Path(sys.argv[1])
    info = ffprobe_json(video)
    video_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), {})
    informe = {
        "video": video.name,
        "video_codec": video_stream.get("codec_name"),
        "resolucion": f'{video_stream.get("width")}x{video_stream.get("height")}',
        "fps": video_stream.get("avg_frame_rate"),
        "dur_s": round(float(info.get("format", {}).get("duration", 0.0)), 2),
        "audio_codec": audio_stream.get("codec_name"),
        "visual": rachas_visuales(video),
        "audio": audio_por_100ms(video),
    }
    if "--wavs" in sys.argv:
        idx = sys.argv.index("--wavs") + 1
        carpeta = Path(sys.argv[idx])
        ts = Path(r"D:\Nexus_Remotion\src\segmentos.ts")
        informe["wavs_vs_declarado"] = compara_wavs(carpeta, declarado_desde_segmentos(ts))
    print(json.dumps(informe, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

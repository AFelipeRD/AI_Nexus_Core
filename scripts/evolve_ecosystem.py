#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Barrido de evolución del ecosistema AI Nexus Core: skills, MCP, conectores y plugins.

Ejecuta `npx -y skills find <término>` para cada dominio del ecosistema y consulta
la API de GitHub para detectar servidores MCP, conectores, plugins y utilidades de IA
nuevos o consolidados. Redacta un informe fechado en `output/evolution_report.md`
para que `auto-researcher` lo evalúe e integre siguiendo `skills/ecosystem-evolution/SKILL.md`.

Uso:
    python scripts/evolve_ecosystem.py [--top 5] [--salida output/evolution_report.md]

Programación semanal opcional (Windows, decisión del usuario):
    schtasks /create /tn "AI_Nexus_Evolve" ^
        /tr "python D:\\AI_Nexus_Core\\scripts\\evolve_ecosystem.py" ^
        /sc weekly /d MON /st 09:00
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA_DEFECTO = RAIZ / "output" / "evolution_report.md"
# Windows: `npx` es un .cmd que subprocess no resuelve solo; which() consulta PATHEXT.
NPX = shutil.which("npx") or "npx"

# Dominio del ecosistema -> términos de búsqueda en el registro abierto (Vercel Labs)
DOMINIOS: dict[str, list[str]] = {
    "Fullstack / Web": ["react", "nextjs", "typescript"],
    "GenAI / RAG": ["rag", "prompt engineering", "multimodal"],
    "Video": ["ffmpeg", "video", "playwright"],
    "Imagen": ["image generation", "svg", "canvas design"],
    "Audio": ["audio", "tts", "whisper"],
    "Datos / OLAP": ["duckdb", "polars", "data analysis"],
    "ML / Redes neuronales": ["pytorch", "machine learning"],
    "Diseño / UI": ["frontend design", "animation", "design system"],
    "Seguridad / Revisión": ["code review", "security audit"],
    "Memoria / Grafo": ["obsidian", "knowledge graph", "memory"],
    "Navegador / Scraping": ["web scraping", "browser automation"],
    "Git / Commits": ["conventional commits", "pre-commit"],
}

# Utilidades de IA -> términos en el registro abierto (MCP, conectores, plugins)
DOMINIOS_UTILIDADES: dict[str, list[str]] = {
    "Servidores MCP / Utilidades IA": ["mcp", "agent tools"],
    "Conectores / Plugins": ["connector", "plugin"],
}

ANSI = re.compile(r"\x1b\[[0-9;]*m")
PATRON_HALLAZGO = re.compile(r"^(.+?)\s+([\d.]+[KM]?)\s+installs\s*$", re.UNICODE)


def instalaciones_a_numero(texto: str) -> float:
    """Convierte «123.4K» o «3.5M» en número de instalaciones."""
    try:
        if texto.endswith("K"):
            return float(texto[:-1]) * 1_000
        if texto.endswith("M"):
            return float(texto[:-1]) * 1_000_000
        return float(texto)
    except ValueError:
        return 0.0


def barrer(termino: str, top: int) -> list[tuple[str, float]]:
    """Ejecuta find-skills para un término y devuelve (habilidad, instalaciones) top."""
    try:
        resultado = subprocess.run(
            [NPX, "-y", "skills", "find", termino],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120, cwd=RAIZ,
        )
    except (subprocess.TimeoutExpired, OSError) as error:
        print(f"AVISO: fallo al barrer «{termino}»: {error}", file=sys.stderr)
        return []
    hallazgos: dict[str, float] = {}
    for linea in ANSI.sub("", resultado.stdout).splitlines():
        coincidencia = PATRON_HALLAZGO.search(linea.strip())
        if coincidencia:
            habilidad, instalaciones = coincidencia.groups()
            hallazgos[habilidad] = max(hallazgos.get(habilidad, 0.0),
                                       instalaciones_a_numero(instalaciones))
    return sorted(hallazgos.items(), key=lambda par: par[1], reverse=True)[:top]


def barrer_github(consulta: str, top: int) -> list[tuple[str, int, str]]:
    """Busca repositorios en GitHub (MCP, conectores, utilidades) por estrellas."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    cabeceras = {"Accept": "application/vnd.github+json"}
    if token:
        cabeceras["Authorization"] = f"Bearer {token}"
    url = ("https://api.github.com/search/repositories?"
           + urllib.parse.urlencode({"q": consulta, "sort": "stars",
                                      "order": "desc", "per_page": top}))
    peticion = urllib.request.Request(url, headers=cabeceras)
    try:
        with urllib.request.urlopen(peticion, timeout=30) as respuesta:
            datos = json.load(respuesta)
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as error:
        print(f"AVISO: fallo al consultar GitHub «{consulta}»: {error}", file=sys.stderr)
        return []
    return [(repo["full_name"], int(repo["stargazers_count"]),
             (repo["description"] or "").strip())
            for repo in datos.get("items", [])]


def consultas_github() -> dict[str, str]:
    """Consultas de GitHub con ventana móvil de 90 días para lo emergente."""
    hace_90_dias = (dt.date.today() - dt.timedelta(days=90)).isoformat()
    return {
        "MCP emergentes (90 días)": f"topic:model-context-protocol stars:>400 created:>{hace_90_dias}",
        "MCP consolidados": "topic:model-context-protocol stars:>3000",
        "Compresión de contexto": "llm context compression stars:>100",
    }


def skills_locales() -> list[str]:
    """Lista las habilidades nativas instaladas en .opencode/skills/."""
    carpeta = RAIZ / ".opencode" / "skills"
    return sorted(d.name for d in carpeta.iterdir() if (d / "SKILL.md").exists())


def tabla_habilidades(titulo: str, hallazgos: list[tuple[str, float]]) -> list[str]:
    """Sección Markdown con una tabla de (habilidad, instalaciones)."""
    lineas = [f"## {titulo}"]
    if not hallazgos:
        lineas.append("- Sin resultados.")
    else:
        lineas.extend(["| Habilidad | Instalaciones |", "|---|---|"])
        lineas.extend(f"| `{h}` | {v:,.0f} |" for h, v in hallazgos)
    lineas.append("")
    return lineas


def tabla_repos(titulo: str, repos: list[tuple[str, int, str]]) -> list[str]:
    """Sección Markdown con una tabla de repositorios de GitHub."""
    lineas = [f"## {titulo}"]
    if not repos:
        lineas.append("- Sin resultados.")
    else:
        lineas.extend(["| Repositorio | Estrellas | Descripción |", "|---|---|---|"])
        for nombre, estrellas, descripcion in repos:
            texto = descripcion.replace("|", "\\|")[:110]
            lineas.append(f"| [`{nombre}`](https://github.com/{nombre}) | {estrellas:,} | {texto} |")
    lineas.append("")
    return lineas


def redactar(dominios: dict[str, list[tuple[str, float]]],
             utilidades: dict[str, list[tuple[str, float]]],
             github: dict[str, list[tuple[str, int, str]]],
             locales: list[str]) -> str:
    """Construye el informe Markdown del barrido."""
    hoy = dt.date.today().isoformat()
    lineas = [
        "# Informe de evolución del ecosistema — skills, MCP, conectores y plugins",
        "",
        f"> Generado automáticamente el {hoy} por `scripts/evolve_ecosystem.py`.",
        "> Protocolo de evaluación e integración: `skills/ecosystem-evolution/SKILL.md`.",
        "",
        f"**Habilidades nativas instaladas ({len(locales)})**: "
        + ", ".join(f"`{s}`" for s in locales),
        "",
        "# Habilidades comunitarias (registro find-skills)",
        "",
    ]
    for dominio, hallazgos in dominios.items():
        lineas.extend(tabla_habilidades(dominio, hallazgos))
    lineas.append("# Utilidades de IA — MCP, conectores y plugins")
    lineas.append("")
    for dominio, hallazgos in utilidades.items():
        lineas.extend(tabla_habilidades(dominio, hallazgos))
    lineas.append("# Ecosistema GitHub — servidores MCP y utilidades")
    lineas.append("")
    for consulta, repos in github.items():
        lineas.extend(tabla_repos(consulta, repos))
    lineas.extend([
        "## Criterios de evaluación",
        "1. Autoridad del mantenedor (oficial de la tecnología > comunidad grande).",
        "2. Volumen de instalaciones/estrellas y mantenimiento reciente.",
        "3. Licencia compatible (MIT / Apache).",
        "4. Solapamiento con lo nativo: integrar heurísticas con atribución, no duplicar.",
        "5. **MCP — seguridad primero**: se ejecutan localmente con permisos de sesión;",
        "   exige código auditable; oficial (`@modelcontextprotocol/servers`) > comunidad",
        "   estable > desconocidos; decláralo en `opencode.json` con `enabled: false`",
        "   hasta probarlo con una tarea real.",
        "",
    ])
    return "\n".join(lineas) + "\n"


def main() -> int:
    """Punto de entrada: barre dominios, utilidades y GitHub; escribe el informe."""
    parser = argparse.ArgumentParser(
        description="Barrido find-skills + GitHub del ecosistema")
    parser.add_argument("--top", type=int, default=5, help="hallazgos por término")
    parser.add_argument("--salida", type=Path, default=SALIDA_DEFECTO, help="ruta del informe")
    args = parser.parse_args()

    def barrer_grupo(grupo: dict[str, list[str]]) -> dict[str, list[tuple[str, float]]]:
        resultados: dict[str, list[tuple[str, float]]] = {}
        for dominio, terminos in grupo.items():
            print(f"Barrido: {dominio}...")
            vistos: dict[str, float] = {}
            for termino in terminos:
                for habilidad, instalaciones in barrer(termino, args.top):
                    vistos[habilidad] = max(vistos.get(habilidad, 0.0), instalaciones)
            resultados[dominio] = sorted(vistos.items(), key=lambda par: par[1],
                                         reverse=True)[: args.top * 2]
        return resultados

    dominios = barrer_grupo(DOMINIOS)
    utilidades = barrer_grupo(DOMINIOS_UTILIDADES)

    github: dict[str, list[tuple[str, int, str]]] = {}
    for nombre, consulta in consultas_github().items():
        print(f"Barrido GitHub: {nombre}...")
        github[nombre] = barrer_github(consulta, args.top * 2)

    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(redactar(dominios, utilidades, github, skills_locales()),
                           encoding="utf-8", newline="\n")
    print(f"Informe escrito en {args.salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

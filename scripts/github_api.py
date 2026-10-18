#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Consulta la API de GitHub con GITHUB_TOKEN (solo biblioteca estándar).
#
# Uso:
#   python scripts/github_api.py trending --tema "ai agent" --dias 7 --min-estrellas 100 [--notificar]
#   python scripts/github_api.py repo propietario/nombre
#   python scripts/github_api.py rate
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
API = "https://api.github.com"


def cargar_env():
    # Lee .env de la raíz sin sobrescribir variables ya definidas.
    ruta = RAIZ / ".env"
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))


def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not t:
        sys.exit("Error: define GITHUB_TOKEN (o GITHUB_PERSONAL_ACCESS_TOKEN) en el entorno o en .env")
    return t


def peticion(ruta, parametros=None):
    url = API + ruta
    if parametros:
        url += "?" + urllib.parse.urlencode(parametros)
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + token(),
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "AI-Nexus-Core",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", errors="replace")[:300]
        sys.exit("Error HTTP %s en %s: %s" % (e.code, ruta, cuerpo))
    except urllib.error.URLError as e:
        sys.exit("Error de red: %s" % e.reason)


def resumen(r):
    return {
        "repo": r["full_name"],
        "estrellas": r["stargazers_count"],
        "lenguaje": r.get("language"),
        "licencia": (r.get("license") or {}).get("spdx_id"),
        "descripcion": r.get("description"),
        "creado": r["created_at"][:10],
        "url": r["html_url"],
    }


def notificar(titulo, mensaje, url):
    script = RAIZ / "scripts" / "notifier.ps1"
    if os.name != "nt" or not script.exists():
        print("(Toast omitido: requiere Windows y scripts/notifier.ps1)")
        return
    subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
                    "-Titulo", titulo[:60], "-Mensaje", mensaje[:150], "-Url", url], check=False)


def cmd_trending(a):
    desde = (datetime.now(timezone.utc) - timedelta(days=a.dias)).strftime("%Y-%m-%d")
    consulta = "%s created:>%s stars:>=%d fork:false" % (a.tema, desde, a.min_estrellas)
    datos = peticion("/search/repositories", {"q": consulta, "sort": "stars", "order": "desc", "per_page": a.limite})
    repos = [resumen(r) for r in datos.get("items", [])]
    print(json.dumps(repos, ensure_ascii=False, indent=2))
    if a.notificar:
        for r in repos[:3]:
            notificar(r["repo"], "%d estrellas · %s" % (r["estrellas"], r["descripcion"] or "sin descripción"), r["url"])


def cmd_repo(a):
    print(json.dumps(resumen(peticion("/repos/" + a.nombre)), ensure_ascii=False, indent=2))


def cmd_rate(_a):
    n = peticion("/rate_limit")["resources"]["core"]
    reinicio = datetime.fromtimestamp(n["reset"]).strftime("%H:%M:%S")
    print("Límite: %d · Restantes: %d · Reinicia: %s" % (n["limit"], n["remaining"], reinicio))


def main():
    cargar_env()
    ap = argparse.ArgumentParser(description="Consulta la API de GitHub")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("trending", help="repositorios recientes con más estrellas")
    t.add_argument("--tema", default="ai agent")
    t.add_argument("--dias", type=int, default=7)
    t.add_argument("--min-estrellas", type=int, default=100)
    t.add_argument("--limite", type=int, default=10)
    t.add_argument("--notificar", action="store_true", help="enviar Toast de Windows (máx. 3)")
    t.set_defaults(f=cmd_trending)
    r = sub.add_parser("repo", help="datos de un repositorio")
    r.add_argument("nombre", help="propietario/nombre")
    r.set_defaults(f=cmd_repo)
    sub.add_parser("rate", help="estado del límite de tasa").set_defaults(f=cmd_rate)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

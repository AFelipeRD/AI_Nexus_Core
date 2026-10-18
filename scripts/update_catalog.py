#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Indexa agentes, habilidades y comandos y regenera el bloque de catálogo de sus README.md.
# Solo se reescribe lo que está entre <!-- CATALOGO:INICIO --> y <!-- CATALOGO:FIN -->;
# el resto del README (parámetros, modo de uso) se conserva. Biblioteca estándar únicamente.
#
# Uso: python scripts/update_catalog.py [--dry-run]
import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / ".opencode"
INI, FIN = "<!-- CATALOGO:INICIO -->", "<!-- CATALOGO:FIN -->"


def frontmatter(ruta):
    texto = ruta.read_text(encoding="utf-8")
    datos = {}
    if not texto.startswith("---"):
        return datos
    for linea in texto.split("\n")[1:]:
        if linea.strip() == "---":
            break
        if linea[:1] in (" ", "\t") or ":" not in linea:
            continue
        k, v = linea.split(":", 1)
        datos[k.strip()] = v.strip().strip('"').strip("'")
    return datos


def tabla(cabeceras, filas):
    out = ["| " + " | ".join(cabeceras) + " |", "|" + "|".join(["---"] * len(cabeceras)) + "|"]
    for f in filas:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in f) + " |")
    return "\n".join(out)


def escribir_bloque(readme, contenido, simulacro):
    bloque = "%s\n%s\n%s" % (INI, contenido, FIN)
    texto = readme.read_text(encoding="utf-8") if readme.exists() else "# Catálogo\n"
    if INI in texto and FIN in texto:
        antes = texto.split(INI)[0]
        despues = texto.split(FIN, 1)[1]
        nuevo = antes + bloque + despues
    else:
        nuevo = texto.rstrip("\n") + "\n\n## Catálogo (generado)\n" + bloque + "\n"
    if not simulacro:
        readme.write_text(nuevo, encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no escribe archivos")
    a = ap.parse_args()
    avisos = []

    # Agentes
    filas = []
    for f in sorted((BASE / "agents").glob("*.md")):
        if f.name.lower() == "readme.md":
            continue
        d = frontmatter(f)
        if not d.get("description"):
            avisos.append("Agente sin description: %s" % f.name)
        filas.append(("`%s`" % f.stem, d.get("mode", "?"), "`%s`" % d.get("model", "?"), d.get("description", "")))
    escribir_bloque(BASE / "agents" / "README.md", tabla(["Agente", "Modo", "Modelo", "Descripción"], filas), a.dry_run)
    n_ag = len(filas)

    # Habilidades
    filas = []
    for f in sorted((BASE / "skills").glob("*/SKILL.md")):
        d = frontmatter(f)
        if d.get("name") != f.parent.name:
            avisos.append("El name de %s no coincide con su carpeta" % f.parent.name)
        if not d.get("description"):
            avisos.append("Skill sin description: %s" % f.parent.name)
        filas.append(("`%s`" % f.parent.name, d.get("description", "")))
    escribir_bloque(BASE / "skills" / "README.md", tabla(["Skill", "Descripción"], filas), a.dry_run)
    n_sk = len(filas)

    # Comandos
    filas = []
    for f in sorted((BASE / "commands").glob("*.md")):
        if f.name.lower() == "readme.md":
            continue
        d = frontmatter(f)
        if not d.get("description"):
            avisos.append("Comando sin description: %s" % f.name)
        filas.append(("`/%s`" % f.stem, "`%s`" % d.get("agent", "?"), d.get("description", "")))
    escribir_bloque(BASE / "commands" / "README.md", tabla(["Comando", "Agente", "Descripción"], filas), a.dry_run)
    n_cm = len(filas)

    print("Catálogo %s: %d agentes, %d habilidades, %d comandos" % ("(simulacro)" if a.dry_run else "actualizado", n_ag, n_sk, n_cm))
    for aviso in avisos:
        print("AVISO:", aviso)
    sys.exit(1 if avisos else 0)


if __name__ == "__main__":
    main()

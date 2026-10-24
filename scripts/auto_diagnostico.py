#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-diagnóstico del sistema: métricas de sesiones + coherencia del repositorio (§13.3).

Uso:
  python scripts/auto_diagnostico.py                # ambos pases
  python scripts/auto_diagnostico.py --sesiones     # solo métricas de sesiones
  python scripts/auto_diagnostico.py --coherencia   # solo integridad del repo
  python scripts/auto_diagnostico.py --dias 14      # ventana de análisis (por defecto 7)

Fuentes: telemetría del plugin `.opencode/plugins/telemetria.js` (logs/telemetria.jsonl)
y la base local de OpenCode (opencode.db, copiada a temporal antes de leerla).
Salida: output/auto_diagnostico/informe_<marca>.md. Biblioteca estándar únicamente.
"""
import argparse
import json
import re
import shutil
import sqlite3
import sys
import tempfile
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TELEMETRIA = RAIZ / "logs" / "telemetria.jsonl"
SALIDA = RAIZ / "output" / "auto_diagnostico"
DB_ORIGEN = Path.home() / ".local" / "share" / "opencode" / "opencode.db"
DIRS_SKILLS = [RAIZ / ".opencode" / "skills", RAIZ / ".agents" / "skills"]

# Heurística de corrección del usuario (mensajes que redirigen, repiten o re-explican).
MARCAS_CORRECCION = (
    "otra vez", "te dije", "ya te lo", "no era eso", "vuelve a", "de nuevo",
    "no entendiste", "repite", "repítelo", "no, ", "eso no", "otra oportunidad",
    "sigue sin", "no funciona", "sigue pasando", "otra vez",
)


def leer_telemetria() -> list:
    """Devuelve los eventos válidos del JSONL de telemetría (tolera líneas corruptas)."""
    eventos = []
    if not TELEMETRIA.exists():
        return eventos
    for linea in TELEMETRIA.read_text(encoding="utf-8", errors="ignore").splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            eventos.append(json.loads(linea))
        except json.JSONDecodeError:
            continue
    return eventos


def _columnas(con, tabla):
    return [r[1] for r in con.execute("PRAGMA table_info('%s')" % tabla)]


def _textos_usuario(con, tablas):
    """Textos del usuario. Esquema verificado de opencode.db:
    `session_message` (type='user', data={'text': ...}) con reserva en
    `message` (data.role) unida con `part` (data.type='text')."""
    out = []
    if "session_message" in tablas:
        try:
            for tipo, dato in con.execute("SELECT type, data FROM session_message"):
                if tipo != "user":
                    continue
                if isinstance(dato, bytes):
                    dato = dato.decode("utf-8", "ignore")
                if not isinstance(dato, str):
                    continue
                try:
                    j = json.loads(dato)
                except json.JSONDecodeError:
                    out.append(dato)
                    continue
                if isinstance(j, dict) and j.get("text"):
                    out.append(str(j["text"]))
        except sqlite3.Error:
            pass
    if out or "message" not in tablas:
        return out
    try:  # reserva: message (role en data JSON) + part (texto en data JSON)
        roles = {}
        for mid, dato in con.execute("SELECT id, data FROM message"):
            try:
                roles[mid] = json.loads(dato).get("role") if isinstance(dato, str) else None
            except json.JSONDecodeError:
                roles[mid] = None
        for mid, dato in con.execute("SELECT message_id, data FROM part"):
            if roles.get(mid) != "user":
                continue
            try:
                j = json.loads(dato if isinstance(dato, str) else "{}")
                if isinstance(j, dict) and j.get("type") == "text" and j.get("text"):
                    out.append(str(j["text"]))
            except json.JSONDecodeError:
                continue
    except sqlite3.Error:
        pass
    return out


def pase_sesiones(dias: int) -> dict:
    """Métricas: telemetría del plugin + base de OpenCode (mensajes/sesiones)."""
    desde = datetime.now() - timedelta(days=dias)
    m = {"ventana_dias": dias, "aviso": None}
    # --- Telemetría del plugin ---
    ev = [e for e in leer_telemetria() if e.get("ts", "") >= desde.isoformat()]
    por_sesion = {}
    for e in ev:
        s = por_sesion.setdefault(e.get("sesion", "desconocida"), Counter())
        s[e.get("tipo", "?")] += 1
    m["telemetria"] = {
        "eventos": len(ev),
        "sesiones": {k: dict(v) for k, v in por_sesion.items()},
    }
    # --- Base de OpenCode (copia temporal, sin bloquear la sesión viva) ---
    m["db"] = {"disponible": DB_ORIGEN.exists(), "tablas": [], "por_sesion": []}
    if not DB_ORIGEN.exists():
        m["aviso"] = "No se encontró opencode.db; métricas solo de telemetría."
        return m
    with tempfile.TemporaryDirectory(prefix="nexus_diag_") as tmp:
        conexion = None
        try:
            for sufijo in ("", "-wal", "-shm"):
                origen = Path(str(DB_ORIGEN) + sufijo)
                if origen.exists():
                    shutil.copy2(origen, Path(tmp) / (DB_ORIGEN.name + sufijo))
            conexion = sqlite3.connect(str(Path(tmp) / DB_ORIGEN.name))
            tablas = [r[0] for r in conexion.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")]
            m["db"]["tablas"] = tablas
            t_ses = "session_v2" if "session_v2" in tablas else next((t for t in tablas if "session" in t.lower()), None)
            if True:
                textos = _textos_usuario(conexion, tablas)
                intentos = len(textos)
                correcciones = sum(1 for t in textos
                                   if any(marca in t.lower() for marca in MARCAS_CORRECCION))
                re_explicaciones = sum(1 for t in textos
                                       if any(marca in t.lower() for marca in
                                              ("te dije", "ya te lo", "ya expliqué", "otra vez")))
                m["db"]["mensajes"] = {
                    "intentos": intentos,
                    "correcciones": correcciones,
                    "re_explicaciones": re_explicaciones,
                    "tasa_reintento": round(correcciones / intentos, 2) if intentos else 0.0,
                }
            if t_ses:
                try:
                    desde_ms = (datetime.now() - timedelta(days=dias)).timestamp() * 1000
                    sesiones = []
                    for sid, titulo, t_cre, t_comp, reanud, padre in con.execute(
                            "SELECT id, title, time_created, time_compacting, resume_attempts, parent_id FROM %s" % t_ses):
                        if t_cre and t_cre < desde_ms:
                            continue
                        sesiones.append({
                            "id": sid,
                            "titulo": (titulo or "")[:60],
                            "reinicios": reanud or 0,
                            "compactada": bool(t_comp),
                            "derivada": bool(padre),
                        })
                    m["db"]["sesiones_ventana"] = sesiones
                    m["db"]["sesiones_totales"] = con.execute(
                        "SELECT COUNT(*) FROM %s" % t_ses).fetchone()[0]
                except sqlite3.Error:
                    pass
        except sqlite3.Error as err:
            m["aviso"] = "opencode.db legible solo parcialmente: %s" % err
        finally:
            if conexion:
                conexion.close()
    return m


def frontmatter(ruta: Path) -> dict:
    datos = {}
    try:
        texto = ruta.read_text(encoding="utf-8")
    except OSError:
        return datos
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


def _matriz_de_agente(texto: str):
    """Devuelve (skills, mcps) declaradas en la MATRIZ de un agente."""
    skills, mcps = set(), set()
    seccion = None
    for linea in texto.split("\n"):
        l = linea.lower()
        if "skills obligatorias" in l:
            seccion = "skills"
        elif "servidores mcp" in l:
            seccion = "mcp"
        elif "comandos slash" in l:
            seccion = None
        elif seccion and linea.strip().startswith("|"):
            match = re.match(r"\|\s*`([a-zA-Z0-9_.:-]+)`", linea.strip())
            if match:
                (skills if seccion == "skills" else mcps).add(match.group(1))
    return skills, mcps


def skills_en_disco() -> dict:
    """slug -> ruta de SKILL.md (nativas primero si hubiera colisión de nombres)."""
    halladas = {}
    for d in DIRS_SKILLS:
        if not d.exists():
            continue
        for f in d.glob("*/SKILL.md"):
            halladas.setdefault(f.parent.name, f)
    return halladas


def pase_coherencia() -> list:
    """Puerta de Coherencia §13.3: referencias cruzadas de todo el ecosistema."""
    hallazgos = []  # (estado, verificacion, detalle)
    ok = lambda v, d: hallazgos.append(("OK", v, d))
    alerta = lambda v, d: hallazgos.append(("ALERTA", v, d))
    fallo = lambda v, d: hallazgos.append(("FALLO", v, d))

    disco = skills_en_disco()
    agentes = {f.stem: f for f in (RAIZ / ".opencode" / "agents").glob("*.md")
               if f.name.lower() != "readme.md"}
    comandos = {f.stem: f for f in (RAIZ / ".opencode" / "commands").glob("*.md")
                if f.name.lower() != "readme.md"}

    # opencode.json (gitignored pero presente en local)
    mcp_declarados = set()
    cfg = RAIZ / "opencode.json"
    if cfg.exists():
        try:
            mcp_declarados = set(json.loads(cfg.read_text(encoding="utf-8")).get("mcp", {}).keys())
            ok("opencode.json", "MCP declarados: %s" % ", ".join(sorted(mcp_declarados)) or "—")
        except json.JSONDecodeError:
            fallo("opencode.json", "JSON inválido")
    else:
        alerta("opencode.json", "ausente (gitignore); no se validan MCP")

    usadas_por = {}
    for nombre, ruta in sorted(agentes.items()):
        fm = frontmatter(ruta)
        if not fm.get("description"):
            alerta("Agentes", "%s sin description" % nombre)
        skills, mcps = _matriz_de_agente(ruta.read_text(encoding="utf-8"))
        for s in skills:
            usadas_por.setdefault(s, set()).add(nombre)
            if s not in disco:
                fallo("Matriz skills", "`%s` declarada en %s pero no existe en disco" % (s, nombre))
        for m in sorted(mcps):
            if mcp_declarados and m not in mcp_declarados:
                fallo("Matriz MCP", "`%s` declarada en %s pero ausente en opencode.json" % (m, nombre))

    for slug, ruta in sorted(disco.items()):
        fm = frontmatter(ruta)
        if fm.get("name") and fm["name"] != slug:
            alerta("Skills", "`%s`: name del frontmatter ('%s') != carpeta" % (slug, fm["name"]))
        if not fm.get("description"):
            alerta("Skills", "`%s` sin description" % slug)

    for nombre, ruta in sorted(comandos.items()):
        fm = frontmatter(ruta)
        agente = fm.get("agent", "")
        if agente and agente not in agentes:
            fallo("Comandos", "/%s apunta al agente `%s` que no existe" % (nombre, agente))

    huerfanas = sorted(s for s in disco if s not in usadas_por
                       and not any(re.search(r"`%s`" % re.escape(s),
                                             r.read_text(encoding="utf-8", errors="ignore"))
                                  for r in comandos.values()))
    if huerfanas:
        alerta("Skills huérfanas", "sin matriz ni comando que las invoque: %s"
               % ", ".join("`%s`" % s for s in huerfanas))

    ok("Agentes", "%d agentes con MATRIZ verificada" % len(agentes))
    ok("Skills", "%d skills en disco (%d nativas, %d del registro)"
       % (len(disco), len([s for s in disco if (RAIZ / ".opencode" / "skills" / s / "SKILL.md").exists()]),
          len(disco) - len([s for s in disco if (RAIZ / ".opencode" / "skills" / s / "SKILL.md").exists()])))
    return hallazgos


def hallazgos_automaticos(m: dict) -> list:
    """Reglas deterministas sobre las métricas; el agente interpreta y decide."""
    out = []
    ses = m.get("telemetria", {}).get("sesiones", {})
    for sid, tipos in ses.items():
        fallos_h = tipos.get("fallo_herramienta", 0)
        if fallos_h > 2:
            out.append("La sesión `%s` acumuló %d fallos de herramienta (> umbral 2): revisa si alguna tool/script está rota." % (sid, fallos_h))
        if tipos.get("compactacion", 0) > 2:
            out.append("La sesión `%s` se compactó %d veces: contexto saturado; audita si se leyeron archivos completos en vez de fragmentos." % (sid, tipos.get("compactacion")))
        if tipos.get("fallo_sesion", 0) > 0:
            out.append("La sesión `%s` registró %d errores de sesión (`session.error`): posible fallo de proveedor o runtime." % (sid, tipos.get("fallo_sesion")))
    por_dia = Counter(e.get("ts", "")[:10] for e in leer_telemetria() if e.get("tipo") == "sesion_creada")
    for dia, n in sorted(por_dia.items()):
        if n > 2:
            out.append("El %s se crearon %d sesiones nuevas: patrón de reinicio/reintento — valida si la tarea anterior quedó inconclusa." % (dia, n))
    msg = m.get("db", {}).get("mensajes")
    if msg and msg["tasa_reintento"] > 0.5:
        out.append("tasa_reintento global %.2f (> 0.5 = fallo sistémico): el usuario corrigió %d de %d mensajes." % (msg["tasa_reintento"], msg["correcciones"], msg["intentos"]))
    for s in m.get("db", {}).get("sesiones_ventana", []):
        if s.get("reinicios", 0) > 2:
            out.append("La sesión «%s» necesitó %d reanudaciones (resume_attempts): proveedor o contexto rotos repetidamente." % (s.get("titulo") or s.get("id", "?"), s["reinicios"]))
    ventana = m.get("db", {}).get("sesiones_ventana", [])
    compactadas = [s for s in ventana if s.get("compactada")]
    if ventana and len(compactadas) > 2:
        out.append("%d de %d sesiones requirieron compactación: revisa si el Headroom del 50 %% se está respetando." % (len(compactadas), len(ventana)))
    return out[:6]


def main():
    ap = argparse.ArgumentParser(description="Auto-diagnóstico del sistema AI_Nexus_Core")
    ap.add_argument("--sesiones", action="store_true", help="solo métricas de sesiones")
    ap.add_argument("--coherencia", action="store_true", help="solo integridad del repositorio")
    ap.add_argument("--dias", type=int, default=7, help="ventana de análisis (días)")
    args = ap.parse_args()
    hacer_sesiones = args.sesiones or not args.coherencia
    hacer_coherencia = args.coherencia or not args.sesiones

    marca = datetime.now().strftime("%Y%m%d_%H%M")
    lineas = ["# Auto-diagnóstico del sistema — %s" % datetime.now().strftime("%Y-%m-%d %H:%M"), ""]
    resumen, m = {}, {}
    if hacer_sesiones:
        m = pase_sesiones(args.dias)
        resumen["sesiones"] = m
        t = m.get("telemetria", {})
        lineas += ["## Métricas de sesiones (últimos %d días)" % args.dias, "",
                   "| Origen | Valor |", "|---|---|",
                   "| Eventos de telemetría | %d |" % t.get("eventos", 0),
                   "| Sesiones con telemetría | %d |" % len(t.get("sesiones", {})),
                   "| Sesiones en la ventana (opencode.db) | %d |" % len(m.get("db", {}).get("sesiones_ventana", []))]
        if m.get("db", {}).get("mensajes"):
            j = m["db"]["mensajes"]
            lineas += ["| Mensajes de usuario (intentos) | %d |" % j["intentos"],
                       "| Correcciones detectadas | %d |" % j["correcciones"],
                       "| Re-explicaciones | %d |" % j["re_explicaciones"],
                       "| tasa_reintento | %.2f |" % j["tasa_reintento"]]
        if m.get("aviso"):
            lineas += ["", "> Aviso: %s" % m["aviso"]]
        hal = hallazgos_automaticos(m)
        resumen["hallazgos"] = hal
        if hal:
            lineas += ["", "### Hallazgos automáticos", ""]
            lineas += ["- %s" % h for h in hal]
        else:
            lineas += ["", "### Hallazgos automáticos", "", "- Sin umbrales superados: sesión fluida."]

    fallos = 0
    if hacer_coherencia:
        hallazgos = pase_coherencia()
        resumen["coherencia"] = [(e, v, d) for e, v, d in hallazgos]
        lineas += ["", "## Coherencia del repositorio (§13.3)", "",
                   "| Verificación | Estado | Detalle |", "|---|---|---|"]
        for estado, verif, detalle in hallazgos:
            lineas.append("| %s | %s | %s |" % (verif, estado, detalle))
            fallos += estado == "FALLO"

    lineas += ["", "## Siguientes pasos sugeridos", ""]
    if fallos:
        lineas.append("- Corregir los FALLO de coherencia antes de seguir (Puerta de Coherencia).")
    lineas.append("- `/improve` para que `self-improvement-auditor` interprete estas métricas y aplique mejoras.")
    lineas.append("- `/evolve` si `output/evolution_report.md` tiene más de 7 días.")

    SALIDA.mkdir(parents=True, exist_ok=True)
    informe = SALIDA / ("informe_%s.md" % marca)
    informe.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print("Informe: %s" % informe)
    print("Resumen: sesiones=%s coherencia_fallos=%d hallazgos=%d"
          % (hacer_sesiones, fallos, len(resumen.get("hallazgos", []))))
    if args.dias and m:
        print(json.dumps(resumen, ensure_ascii=False, default=str)[:2000])
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()

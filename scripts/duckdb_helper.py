#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ejecuta consultas SQL analíticas locales con DuckDB sobre CSV, Parquet o JSON.
#
# Uso:
#   python scripts/duckdb_helper.py --archivo data/raw/ventas.csv --sql "SELECT * FROM datos LIMIT 5"
#   python scripts/duckdb_helper.py --archivo "data/raw/*.parquet" --sql "SELECT COUNT(*) FROM datos"
#   python scripts/duckdb_helper.py --sql "SELECT 42" --salida json
import argparse
import json
import re
import sys
from pathlib import Path

ESCRITURA = re.compile(r"^\s*(insert|update|delete|drop|alter|create|copy|attach|truncate|install|load|pragma)\b", re.I)


def lector(ruta):
    ext = Path(ruta.replace("*", "x")).suffix.lower()
    if ext in (".parquet", ".pq"):
        return "read_parquet"
    if ext in (".json", ".jsonl", ".ndjson"):
        return "read_json_auto"
    return "read_csv_auto"


def main():
    ap = argparse.ArgumentParser(description="Consultas SQL locales con DuckDB")
    ap.add_argument("--archivo", help="CSV, Parquet o JSON (admite comodines). Se expone como la vista `datos`")
    ap.add_argument("--sql", required=True, help="consulta SQL")
    ap.add_argument("--salida", choices=["tabla", "json", "csv", "parquet"], default="tabla")
    ap.add_argument("--destino", help="ruta de salida para csv o parquet")
    ap.add_argument("--limite", type=int, default=50, help="filas a mostrar en tabla/json (0 = todas)")
    ap.add_argument("--permitir-escritura", action="store_true", help="autoriza sentencias que modifican datos")
    a = ap.parse_args()

    try:
        import duckdb
    except ImportError:
        sys.exit("Falta duckdb. Instala con: pip install duckdb")

    if ESCRITURA.match(a.sql) and not a.permitir_escritura:
        sys.exit("Consulta de escritura bloqueada. Usa --permitir-escritura si es intencional.")

    con = duckdb.connect()
    if a.archivo:
        ruta = a.archivo.replace("\\", "/").replace("'", "''")
        con.execute("CREATE VIEW datos AS SELECT * FROM %s('%s')" % (lector(a.archivo), ruta))

    try:
        if a.salida in ("csv", "parquet"):
            if not a.destino:
                sys.exit("--destino es obligatorio con salida csv o parquet")
            destino = a.destino.replace("\\", "/").replace("'", "''")
            formato = "CSV, HEADER" if a.salida == "csv" else "PARQUET"
            Path(a.destino).parent.mkdir(parents=True, exist_ok=True)
            con.execute("COPY (%s) TO '%s' (FORMAT %s)" % (a.sql.rstrip("; \n"), destino, formato))
            print("Escrito: %s" % a.destino)
            return
        cursor = con.execute(a.sql)
        columnas = [d[0] for d in cursor.description]
        filas = cursor.fetchall() if a.limite == 0 else cursor.fetchmany(a.limite)
    except duckdb.Error as e:
        sys.exit("Error de DuckDB: %s" % e)

    if a.salida == "json":
        print(json.dumps([dict(zip(columnas, f)) for f in filas], ensure_ascii=False, default=str, indent=2))
        return
    ancho = [max(len(str(c)), *(len(str(f[i])) for f in filas)) if filas else len(str(c)) for i, c in enumerate(columnas)]
    print(" | ".join(str(c).ljust(ancho[i]) for i, c in enumerate(columnas)))
    print("-+-".join("-" * w for w in ancho))
    for f in filas:
        print(" | ".join(str(v).ljust(ancho[i]) for i, v in enumerate(f)))
    print("\n%d filas mostradas" % len(filas))


if __name__ == "__main__":
    main()

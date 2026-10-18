---
description: "Lanza análisis SQL local con DuckDB y Polars."
agent: data-engineer
---
Analiza con la skill `duckdb-analytics`:

$ARGUMENTS

1. Inspecciona el esquema (`DESCRIBE`) y una muestra.
2. Escribe la consulta SQL y ejecútala con `python scripts\duckdb_helper.py --archivo <ruta> --sql "<consulta>"`.
3. Valida con conteos y nulos.
4. Resume el resultado con tiempo y filas procesadas; guarda salidas en `output/`.

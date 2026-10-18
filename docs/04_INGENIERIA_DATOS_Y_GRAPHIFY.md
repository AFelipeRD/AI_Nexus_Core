# 04 · Ingeniería de datos y Graphify

Enlaces: [[02_REDES_NEURONALES_Y_DEEP_LEARNING]] · [[05_GRAFO_LIGHTRAG_Y_OBSIDIAN]]

## DuckDB y Polars
- Agente `data-engineer`, skill `duckdb-analytics`, comando `/analyze-data`.
- DuckDB consulta CSV/Parquet/JSON directamente: `SELECT ... FROM read_csv_auto('data/raw/*.csv')`.
- Polars en modo lazy (`pl.scan_csv`) para transformaciones encadenadas grandes.
- Convierte a Parquet en `data/processed/` para análisis repetidos mucho más rápidos.

## Utilería
```
python scripts\duckdb_helper.py --archivo data\raw\ventas.csv --sql "SELECT region, SUM(total) AS t FROM datos GROUP BY 1 ORDER BY t DESC"
python scripts\duckdb_helper.py --archivo data\raw\ventas.csv --sql "SELECT * FROM datos" --salida csv --destino output\copia.csv
```
La tabla virtual del archivo se llama `datos`. Por defecto solo se permiten consultas de lectura.

## Reglas
- `data/raw/` es de solo lectura.
- Sin concatenar entradas de usuario en SQL.
- Valida siempre conteos, nulos y una muestra.

## Graphify
- Skill `graphify-codebase`, comando `/graphify`, paquete `graphifyy` (en `requirements.txt`).
- Genera un mapa del código (AST y clusters) en `.graphify/` y consúltalo antes de abrir archivos; ahorra tokens.
- Confirma la sintaxis de la versión instalada con `graphify --help`.
- Alternativa mínima: imports con el módulo `ast` de Python.

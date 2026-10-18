---
name: duckdb-analytics
description: "Consultas analíticas SQL de alto rendimiento sobre archivos locales CSV, Parquet y JSON con DuckDB y Polars. Úsala para explorar, agregar y transformar datos sin montar un servidor."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Duckdb Analytics

## Cuándo usar esta skill
- Explorar un archivo de datos.
- Agregar o unir archivos grandes.
- Convertir CSV a Parquet.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `archivo` | ruta a CSV, Parquet o JSON |
| `sql` | consulta a ejecutar (la tabla virtual se llama `datos`) |
| `salida` | tabla, json, csv o parquet |

## Procedimiento
1. **Inspeccionar**: `DESCRIBE SELECT * FROM read_csv_auto('x.csv')` y un `LIMIT 5`.
2. **Consultar en sitio**: DuckDB lee CSV/Parquet en streaming sin cargarlos por completo; usa comodines (`'data/raw/*.csv'`) y mantente bajo el límite estricto de 500 MB de RAM.
3. **Ejecutar con la utilería**: `python scripts\duckdb_helper.py --archivo data\raw\ventas.csv --sql "SELECT region, SUM(total) FROM datos GROUP BY 1"`.
4. **Transformaciones encadenadas**: Polars en modo lazy (`pl.scan_csv(...).filter(...).group_by(...).collect()`). Todo intercambio DuckDB ↔ Polars usa **Apache Arrow zero-copy** (`resultado.arrow()` → `pl.from_arrow(...)`): prohibido materializar copias intermedias.
5. **Convertir a Parquet** para repetir análisis rápido: `COPY (SELECT * FROM datos) TO 'data/processed/x.parquet' (FORMAT parquet)`.
6. **Validar esquema y resultados**: nombres y tipos de columnas, conteo de filas, nulos y una muestra; compara con la fuente.
7. **Rendimiento**: `EXPLAIN ANALYZE`, selecciona solo las columnas necesarias y filtra pronto.

## Ejemplo
```sql
SELECT region, COUNT(*) AS pedidos, ROUND(SUM(total), 2) AS ingresos
FROM read_csv_auto('data/raw/ventas.csv')
WHERE fecha >= DATE '2026-01-01'
GROUP BY region
ORDER BY ingresos DESC;
```

## Errores a evitar
- `SELECT *` sobre archivos enormes.
- Exceder 500 MB de RAM: particiona en lotes y procesa en streaming.
- Copiar datos entre DuckDB y Polars sin Apache Arrow (copia materializada).
- Concatenar entradas del usuario dentro del SQL.
- Escribir en `data/raw/`.

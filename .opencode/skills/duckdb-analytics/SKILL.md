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
8. **Sesiones con estado** (DuckDB oficial): para análisis repetidos, mantén un `state.sql` con `ATTACH` de bases y verifícalo con `SHOW DATABASES;` antes de reutilizarlo; si un `ATTACH` falla, cae a modo ad-hoc contra los archivos.

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

## Referencias comunitarias validadas (find-skills)
- `duckdb/duckdb-skills` — **DuckDB oficial** (`query`, `duckdb-docs`, `read-file`, `attach-db`): SQL Friendly, sesiones con estado vía `ATTACH` y verificación de accesibilidad.
- `k-dense-ai/scientific-agent-skills@polars` — patrones Polars para computación científica.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.
- **Sandbox de seguridad para SQL ad-hoc** (antes de consultar archivos no confiables): `SET allowed_paths=['<archivo>']; SET enable_external_access=false; SET allow_persistent_secrets=false; SET lock_configuration=true;` — blinda la lectura de archivos arbitrarios y los secretos persistentes durante la consulta.
- **Puerta de presupuesto de tokens ANTES de ejecutar**: nunca lances una consulta que devolvería >1 M de filas sin `LIMIT` ni agregación — estima el tamaño del resultado primero y pide confirmación al usuario; >10 GB de datos de entrada → avisa del coste en tiempo. Es el headroom 50/80 aplicado a consultas de datos.
- **Idiomas Friendly SQL modernos**: `FROM`-first, `GROUP BY ALL` / `ORDER BY ALL`, `SELECT * EXCLUDE/REPLACE`, `LIMIT 10%`, `COLUMNS(*)` con regex y lambdas, `count() FILTER (WHERE ...)`, top-N por grupo con `max(col, 3)`, `SUMMARIZE`, `PIVOT`/`UNPIVOT`, joins `ASOF`/`POSITIONAL`/`LATERAL`, dot-chaining (`'x'.trim()`), list comprehensions e `INSERT ... BY NAME` — SQL más breve y legible que el clásico.
- **Taxonomía de errores con recuperación**: clasifica el fallo (sintaxis / extensión no instalada / tabla inexistente / archivo ilegible) → localiza la función o tabla con `find` y reintenta; usa heredocs `<<'SQL'` para evitar el quoting de shell en consultas largas.
- **Excel como fuente de datos válida**: lee hojas con openpyxl o pandas (`pd.read_excel`) para explorar y cargar; al leer un modelo, `data_only=True` devuelve valores calculados sin fórmulas y la carga por defecto devuelve las fórmulas sin valores — recarga dos veces si necesitas ambos.

_Atribuciones: duckdb/duckdb-skills@query (oficial de DuckDB) · anthropics/skills@xlsx._

# Convenciones de código y estilo

- Idioma: español en documentación, comentarios, mensajes de usuario y commits.
- Python 3.10+: tipado cuando aporte claridad, `pathlib` para rutas, `encoding="utf-8"` al abrir archivos de texto.
- Rutas en Windows: usa `pathlib.Path` o cadenas crudas (`r"D:\AI_Nexus_Core"`); nunca concatenes con `+` y `\`.
- Funciones cortas, un propósito; abstracción solo con 3 usos reales (YAGNI).
- Errores: mensajes accionables; no silencies excepciones.
- Seguridad: sin secretos en el código; entradas validadas; consultas parametrizadas.
- Pruebas: cada corrección de fallo añade una prueba que lo reproduce.
- Git: commits semánticos en español (`feat`, `fix`, `docs`, `security`, `perf`, `refactor`, `test`, `chore`).
- Markdown: títulos jerárquicos, tablas para comparar, bloques de código con lenguaje indicado.

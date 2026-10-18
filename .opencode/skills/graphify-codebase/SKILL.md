---
name: graphify-codebase
description: "Mapeo estructural del código mediante AST y clusters de dependencias (Graphify) para no leer archivos innecesarios. Úsala antes de refactorizar o explorar un repositorio desconocido."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Graphify Codebase

## Cuándo usar esta skill
- Antes de explorar o refactorizar código.
- Para ubicar puntos de entrada y dependencias.
- Para ahorrar tokens evitando lecturas completas.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `ruta` | carpeta del proyecto (por defecto, la raíz) |
| `pregunta` | qué se necesita localizar |

## Procedimiento
1. **Instalar**: `pip install graphifyy` (nombre de paquete según `requirements.txt`) y ejecuta `graphify --help` para confirmar la sintaxis de la versión instalada.
2. **Generar el mapa** del proyecto y guárdalo en `.graphify/` (ignorado por Git).
3. **Consultar el mapa** antes de abrir archivos: módulos, funciones, quién llama a quién, clusters acoplados.
4. **Leer solo lo necesario**: abre los archivos señalados, con rangos de líneas.
5. **Alternativa mínima** si Graphify no está disponible: lista imports con el módulo `ast` de Python (`ast.walk` y nodos `Import`/`ImportFrom`) o `rg "^(import|from) "` para otros lenguajes.
6. **Reportar** puntos de entrada, módulos centrales y ciclos de dependencia.

## Ejemplo
```python
import ast, pathlib
for archivo in pathlib.Path(".").rglob("*.py"):
    arbol = ast.parse(archivo.read_text(encoding="utf-8"))
    mods = {n.module or "" for n in ast.walk(arbol) if isinstance(n, ast.ImportFrom)}
    print(archivo, sorted(mods))
```

## Errores a evitar
- Leer el repositorio entero en lugar de consultar el mapa.
- Usar un mapa desactualizado tras cambios grandes.
- Asumir la sintaxis del CLI sin `--help`.

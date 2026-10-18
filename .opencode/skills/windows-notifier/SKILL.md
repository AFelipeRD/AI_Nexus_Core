---
name: windows-notifier
description: "Disparo de alertas Toast nativas de Windows 11 mediante PowerShell para avisos en segundo plano. Úsala cuando una tarea larga termine o se encuentre algo relevante."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Windows Notifier

## Cuándo usar esta skill
- Termina una tarea larga (entrenamiento, indexado, pruebas).
- `github-scout` encuentra un repositorio relevante.
- Un fallo requiere atención del usuario.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `titulo` | texto breve del encabezado |
| `mensaje` | detalle de una o dos líneas |
| `url` | enlace opcional que se abre al pulsar la notificación |

## Procedimiento
1. **Ejecutar** con Windows PowerShell 5.1 (`powershell.exe`), no con PowerShell 7: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\notifier.ps1 -Titulo "..." -Mensaje "..." -Url "https://..."`.
2. **Mensajes breves**: título ≤ 60 caracteres, mensaje ≤ 150.
3. **Frecuencia**: máximo 3 por ejecución; agrupa los hallazgos.
4. **Comprobar** que las notificaciones de Windows y el modo No molestar no bloquean los avisos.
5. **Si falla**, informa por texto en el chat; no reintentes en bucle.

## Ejemplo
```
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\notifier.ps1 -Titulo "Entrenamiento terminado" -Mensaje "val_acc=0.94 · output\modelo.pt"
```

## Errores a evitar
- Invocar el script desde PowerShell 7 (las APIs WinRT no están disponibles).
- Incluir secretos en el texto.
- Notificar en exceso.

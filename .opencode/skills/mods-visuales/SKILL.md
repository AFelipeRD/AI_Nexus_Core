---
name: mods-visuales
description: "Tema visual OLED unificado v5 para Open Code y Warp: paleta Nexus sofisticada (#020617 fondo, #22d3ee acento cian, #8b5cf6 púrpura secundario). Predeterminado y automático, sin comandos. Coordinado para que Warp + Open Code se vean como un solo entorno de IA moderna. Cero consumo de tokens."
license: MIT
compatibility: opencode, warp
metadata:
  idioma: es
  version: "5.0.0"
  consumo_tokens: 0
  consumo_gpu: "solo pantalla (CSS/terminal, sin WebGL)"
  componentes:
    - tema-opencode-chat-v5
    - tema-warp-v5
    - plugin-rainbow
---

# Mods Visuales — Open Code + Warp (tema único predeterminado v5)

## Objetivo

Que Open Code y Warp se vean como una interfaz de IA moderna (estilo Claude Code / ChatGPT) de forma **automática y predeterminada**, sin que tengas que ejecutar ningún comando. Paleta Nexus OLED unificada: fondo profundo, acento cian neón, púrpura eléctrico secundario, vidrio difuminado en Warp, paneles elevados y burbujas de chat en Open Code.

## ¿Qué incluye?

| Componente | Archivo | Estado |
|------------|---------|--------|
| Tema Open Code `ai-nexus-core-chat` v5 | `~/.config/opencode/themes/ai-nexus-core-chat.json` | ✅ Activo y predeterminado |
| Config CLI Open Code | `~/.config/opencode/cli.json` | ✅ Tema `ai-nexus-core-chat`, modo `dark` |
| Plugin visual `oc-plugin-rainbow` | `cli.json` | ✅ Bandas de color animadas |
| Tema Warp `AI Nexus Core` v5 | `C:\Users\AFrSe\AppData\Roaming\warp\Warp\data\themes\ai-nexus-core.yaml` | ✅ Instalado |
| settings.toml Warp | `C:\Users\AFrSe\AppData\Local\warp\Warp\config\settings.toml` | ✅ `theme = "ai-nexus-core"` |
| Workflows Warp | `~/.warp/workflows/` | ✅ `open-code-visual`, `opencode-rapido` |
| Paleta unificada (documentación) | `assets/palette-unificada.md` | ✅ Referencia de colores |

## Cómo se activa (sin cerrar sesiones)

### Open Code
El tema ya está escrito como predeterminado en tu `cli.json`. Para aplicarlo en tu sesión actual:
1. Presiona `Ctrl+P` → **Open settings** → **Theme**
2. Selecciona **`ai-nexus-core-chat`** (modo `dark`)
3. Se ve inmediatamente

### Warp
El tema ya está instalado en la ruta correcta de Windows y `settings.toml` ya apunta a él.
1. Ve a **Settings → Appearance → Theme picker**
2. Selecciona **`AI Nexus Core`**
3. Se aplica al instante, sin cerrar Warp

Si no aparece tras reiniciar Warp una vez, selecciónalo manualmente desde el Theme Picker.

### Truecolor (colores completos en PowerShell de Warp)
```powershell
$env:COLORTERM="truecolor"
```

## Consumo

- **Tokens:** 0 (solo es un tema de colores, no llama a ninguna IA).
- **GPU:** solo la de tu terminal/navegador al renderizar la interfaz. Sin WebGL, sin Canvas, sin generación de imagen.

## Archivos del proyecto

- `.opencode/themes/ai-nexus-core-chat.json` — tema V5 de Open Code
- `assets/palette-unificada.md` — paleta de referencia
- `assets/warp/workflows/*.yaml` — workflows de Warp

No hay scripts que ejecutar. La visualización es automática una vez seleccionado el tema en cada aplicación.

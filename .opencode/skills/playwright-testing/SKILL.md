---
name: playwright-testing
description: "Procedimientos para pruebas en navegador real con Playwright: navegación, clics, formularios, capturas y pruebas E2E visuales, tanto con el MCP como con scripts. Úsala para validar aplicaciones web."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Playwright Testing

## Cuándo usar esta skill
- Tras construir o modificar una interfaz.
- Para reproducir un error visual o de flujo.
- Para regresión E2E.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `url` | dirección de la aplicación |
| `escenario` | flujo de usuario a verificar |
| `viewports` | tamaños, por defecto 390x844 y 1440x900 |

## Procedimiento
1. **Preparar**: `pip install playwright` y `playwright install chromium` (o `npx playwright install chromium`).
2. **Arrancar la app** y confirmar que responde antes de probar.
3. **Con el MCP `playwright`**: `browser_navigate` → `browser_snapshot` (árbol de accesibilidad) → `browser_click` / `browser_type` → `browser_take_screenshot`.
4. **Selectores**: prefiere `get_by_role`, `get_by_label` y `get_by_text` antes que CSS.
5. **Esperas**: por condición (`expect(...).to_be_visible()`), nunca `sleep` fijo.
6. **Cubrir** camino feliz, un error de validación y un estado vacío; repetir en móvil y escritorio.
7. **Rendimiento**: verifica 60 FPS estables en animaciones y canvas, y cero errores en la consola del navegador.
8. **Evidencias**: guarda capturas en `output/capturas/` y reporta URL, pasos y resultado.
9. **Limpiar**: cierra navegador y servidores levantados.

## Ejemplo
```python
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={"width": 390, "height": 844})
    pag.goto("http://localhost:3000")
    pag.get_by_role("button", name="Entrar").click()
    expect(pag.get_by_role("heading", name="Panel")).to_be_visible()
    pag.screenshot(path="output/capturas/panel-movil.png")
    nav.close()
```

## Errores a evitar
- Esperas fijas con `sleep`.
- Declarar éxito con errores en consola o con menos de 60 FPS en pantallas animadas.

## Referencias comunitarias validadas (find-skills)
- `anthropics/skills@webapp-testing` — **Anthropic oficial, 180 K instalaciones**: pruebas E2E de aplicaciones web con Playwright.
- `currents-dev/playwright-best-practices-skill@playwright-best-practices` — Currents: POM, fixtures, autenticación, regresión visual, canvas/WebGL.
- `microsoft/playwright-cli@playwright-cli` — Microsoft oficial, 188 K: CLI de Playwright.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.
- Selectores CSS frágiles.
- Declarar éxito sin captura ni aserción.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validación visual del preview AI Nexus Core con Playwright."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML_PATH = Path("output/preview_visual.html").resolve().as_uri()
CAPTURAS = Path("output/capturas")
CAPTURAS.mkdir(parents=True, exist_ok=True)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Escritorio
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(HTML_PATH)
        page.wait_for_selector("header h1", state="visible")
        page.wait_for_selector(".tarjeta", state="visible")
        expect(page.locator("header h1")).to_be_visible()
        expect(page.locator(".marca img")).to_be_visible()
        page.screenshot(path=str(CAPTURAS / "preview_escritorio.png"), full_page=True)
        page.close()
        # Móvil
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(HTML_PATH)
        page.wait_for_selector("header h1", state="visible")
        page.screenshot(path=str(CAPTURAS / "preview_movil.png"), full_page=True)
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.close()
        browser.close()
    print(f"Validación completa. Capturas en: {CAPTURAS}")
    if console_errors:
        print("Errores de consola:", console_errors)
    else:
        print("Sin errores de consola.")

if __name__ == "__main__":
    main()

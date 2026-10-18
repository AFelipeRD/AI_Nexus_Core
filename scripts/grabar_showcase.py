"""Graba el showcase motion de AI Nexus Core como video de 10 s.

Abre Chromium a 1280x720, carga assets/motion_showcase.html,
espera 10.5 s y cierra el navegador para que Playwright guarde
el video en assets/video/.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
HTML = RAIZ / "assets" / "motion_showcase.html"
DIR_VIDEO = RAIZ / "assets" / "video"
DURACION_MS = 10_500  # 10 s de animación + 0.5 s de margen

def main() -> None:
    DIR_VIDEO.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        contexto = navegador.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(DIR_VIDEO),
            record_video_size={"width": 1280, "height": 720},
        )
        pagina = contexto.new_page()
        pagina.goto(HTML.as_uri())
        pagina.wait_for_timeout(DURACION_MS)
        # Cerrar el contexto fuerza el guardado del video en disco
        ruta_video = pagina.video.path()
        contexto.close()
        navegador.close()

    destino = DIR_VIDEO / "showcase_ai_nexus_core.webm"
    if Path(ruta_video) != destino:
        Path(ruta_video).replace(destino)
    print(f"Video guardado: {destino}")

if __name__ == "__main__":
    main()

---
name: image-creative-suite
description: "Dirección artística y generación de imágenes: gramática visual de prompts, herramienta oficial FLUX 3 Klein en NVIDIA Build vía scripts/nvidia_flux.py, composición áurea, teoría del color por dominio, manipulación con Pillow/Canvas y optimización WebP/AVIF. Úsala al dirigir o generar imágenes."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.1"
---

# Image Creative Suite

## Cuándo usar esta skill
- Generar imágenes con modelos generativos (herramienta oficial: FLUX en NVIDIA Build).
- Definir la dirección artística de un producto visual.
- Manipular u optimizar imágenes localmente.

## Herramienta oficial de generación (FLUX en NVIDIA Build)
Invocación en terminal (`bash`) desde la raíz del repositorio, con parámetros en inglés:

```bash
python scripts/nvidia_flux.py "<PROMPT_EN_INGLES>" "<NOMBRE_ARCHIVO.png>"
```

| Parámetro | Descripción |
|---|---|
| `PROMPT_EN_INGLES` | prompt cinematográfico en inglés (si se omite, usa uno de demostración) |
| `NOMBRE_ARCHIVO.png` | archivo de salida (por defecto `robot_publicidad.png`) |

- Resolución fija: **1024×1024 px**, `steps=50`, `seed=0`.
- Requiere la clave en `.secrets/nvidia.key` (si falta, aborta con `[ERROR]`).
- La imagen se guarda automáticamente en `output/images/<NOMBRE_ARCHIVO.png>`.

**Protocolo de uso:**
1. Traduce y enriquece la petición del usuario a un prompt cinematográfico en inglés (iluminación, estilo — 3D Pixar / fotorrealista / vector —, encuadre y composición).
2. Ejecuta el comando en terminal mediante `bash`.
3. Verifica el mensaje `[EXITO]` y la existencia real del archivo en `output/images/`.
4. Informa al usuario de la ruta final; para web, exporta WebP/AVIF tras verificar peso y nitidez.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `brief` | intención, dominio y emoción buscada |
| `modelo` | FLUX (herramienta oficial) o manipulación local |
| `formato` | ráster (WebP/AVIF) o SVG paramétrico |

## Procedimiento
1. **Dirección por dominio**: paleta, luz y estilo nacen del brief (agricultura → tierra/verde; salud → neutros limpios; finanzas → sobrio); cero paletas fijas.
2. **Filosofía visual primero** (heurística Anthropic): antes de generar, nombra la dirección como un movimiento estético de 1-2 palabras («Silencio Cromático») y articula cómo se manifiesta en espacio, forma, color, escala, ritmo y jerarquía; el resultado debe ser 90 % expresión visual y 10 % texto esencial, con acabado de artesanía meticulosa.
3. **Gramática del prompt**: sujeto → acción/pose → luz (dirección, calidad) → encuadre/lente → estilo/época → parámetros técnicos; cada término debe cambiar el resultado o sobra.
4. **Composición**: proporción áurea o tercios, un solo punto focal, jerarquía de contraste; el ojo debe saber a dónde ir en menos de 1 segundo.
5. **Generación oficial**: ejecuta `scripts/nvidia_flux.py` con el prompt pulido en inglés y verifica el archivo resultante en `output/images/`.
6. **Manipulación local**: Pillow/Canvas para color, recorte y composición; ajustes no destructivos cuando sea posible.
7. **SVG paramétrico**: para iconos, patrones y gráficos que escalan sin pérdida; genera con parámetros, no con píxeles sueltos.
8. **Optimizar**: WebP/AVIF con calidad perceptual; verifica peso y nitidez antes de entregar.

## Ejemplo
```text
Prompt: agricultora inspeccionando cultivo al amanecer, luz lateral cálida y volumétrica,
encuadre medio 35 mm, neblina en primer plano, paleta tierra y verdes saturados,
fotorrealista, alta gama dinámica
```

## Errores a evitar
- Invocar el script sin traducir el prompt al inglés o sin verificar el archivo generado.
- Paletas por defecto ignorando el dominio.
- Prompts acumulando términos sin efecto comprobado.
- Texto dentro de imágenes generativas sin verificar legibilidad.
- Entregar PNG pesados donde WebP/AVIF pesa la mitad.

## Referencias comunitarias validadas (find-skills)
- `anthropics/skills@canvas-design` — **Anthropic oficial, 118 K instalaciones**: creación de filosofías visuales como movimientos estéticos antes de expresarlas en el lienzo.
- `openai/skills@imagegen` — OpenAI oficial: generación de imágenes con su API.
- `leonxlnx/taste-skill@brandkit` / `@image-to-code` — sistema de gusto visual y traducción de imagen a código (382 K instalaciones).
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

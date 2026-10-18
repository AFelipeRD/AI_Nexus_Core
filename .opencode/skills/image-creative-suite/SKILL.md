---
name: image-creative-suite
description: "Gramática visual para prompts generativos (Flux, Midjourney, SDXL, DALL-E), composición áurea, teoría del color por dominio y manipulación local de píxeles con Pillow/Canvas. Úsala al dirigir o generar imágenes."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Image Creative Suite

## Cuándo usar esta skill
- Generar imágenes con modelos generativos.
- Definir la dirección artística de un producto visual.
- Manipular u optimizar imágenes localmente.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `brief` | intención, dominio y emoción buscada |
| `modelo` | Flux, Midjourney, SDXL, DALL-E o manipulación local |
| `formato` | ráster (WebP/AVIF) o SVG paramétrico |

## Procedimiento
1. **Dirección por dominio**: paleta, luz y estilo nacen del brief (agricultura → tierra/verde; salud → neutros limpios; finanzas → sobrio); cero paletas fijas.
2. **Gramática del prompt**: sujeto → acción/pose → luz (dirección, calidad) → encuadre/lente → estilo/época → parámetros técnicos; cada término debe cambiar el resultado o sobra.
3. **Composición**: proporción áurea o tercios, un solo punto focal, jerarquía de contraste; el ojo debe saber a dónde ir en menos de 1 segundo.
4. **Manipulación local**: Pillow/Canvas para color, recorte y composición; ajustes no destructivos cuando sea posible.
5. **SVG paramétrico**: para iconos, patrones y gráficos que escalan sin pérdida; genera con parámetros, no con píxeles sueltos.
6. **Optimizar**: WebP/AVIF con calidad perceptual; verifica peso y nitidez antes de entregar.

## Ejemplo
```text
Prompt: agricultora inspeccionando cultivo al amanecer, luz lateral cálida y volumétrica,
encuadre medio 35 mm, neblina en primer plano, paleta tierra y verdes saturados,
fotorrealista, alta gama dinámica
```

## Errores a evitar
- Paletas por defecto ignorando el dominio.
- Prompts acumulando términos sin efecto comprobado.
- Texto dentro de imágenes generativas sin verificar legibilidad.
- Entregar PNG pesados donde WebP/AVIF pesa la mitad.

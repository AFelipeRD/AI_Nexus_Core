# Rúbrica de la Arena

Cada variante se puntúa de 1 (deficiente) a 5 (excelente) con una frase de evidencia por criterio.

| Criterio | Peso | 1 punto | 3 puntos | 5 puntos |
|---|---|---|---|---|
| Seguridad | 30 % | Expone secretos o acepta entradas sin validar | Validaciones básicas | Mínimo privilegio, entradas validadas, sin secretos |
| Robustez | 30 % | Falla ante casos límite | Maneja errores comunes | Casos límite, reintentos y pruebas que lo demuestran |
| Simplicidad | 20 % | Capas y dependencias superfluas | Razonable | Solución nativa, mínima, fácil de leer (escalera YAGNI) |
| Velocidad | 20 % | Lenta o con complejidad mala | Aceptable | Medida y adecuada al volumen real |

**Puntaje ponderado** = 0,30·Seguridad + 0,30·Robustez + 0,20·Simplicidad + 0,20·Velocidad.

**Reglas del dictamen**
1. Seguridad ≤ 2 descalifica la variante.
2. Diferencia entre las dos mejores ≥ 0,5 → gana la primera.
3. Diferencia < 0,5 → síntesis que combine lo mejor de ambas, con su propio puntaje estimado.
4. Todo dictamen incluye riesgos residuales y pasos de verificación.

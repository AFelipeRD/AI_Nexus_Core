---
name: audio-sound-suite
description: "Fórmulas de síntesis con Web Audio API (osciladores, frecuencias, envolventes ADSR), diseño sonoro micro-táctil de baja latencia, TTS/Whisper y análisis espectral. Úsala al crear sonido para interfaces o procesar audio."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Audio Sound Suite

## Cuándo usar esta skill
- Diseñar sonido de interfaz o micro-interacciones.
- Sintetizar audio en el navegador (Web Audio API).
- Procesar voz: TTS o transcripción (Whisper).

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `intencion` | feedback, atmósfera, alerta o narración |
| `plataforma` | navegador (Web Audio) o pipeline local |
| `latencia` | presupuesto (interactiva: < 100 ms) |

## Procedimiento
1. **Intención primero**: define qué comunica el sonido (éxito, error, transición, atmósfera); si no comunica, no existe (YAGNI).
2. **Síntesis Web Audio**: `AudioContext` tras gesto del usuario; osciladores (sine/triangle/square/sawtooth) y ruido; filtros (lowpass/highpass) para timbre.
3. **Envolventes ADSR**: attack corto (5-20 ms) para lo percusivo, release suave (80-300 ms) para evitar clics; `setTargetAtTime` para transiciones sin chasquido.
4. **Micro-interacciones**: < 100 ms de latencia percibida; el sonido acompaña `transform`/`opacity`, nunca los reemplaza.
5. **Voz**: TTS para narración (velocidad y pausas explícitas); Whisper para transcripción con idioma y formato de salida declarados.
6. **Análisis y verificación**: `AnalyserNode` para el espectro; pico ≤ -3 dBFS (headroom), sin clipping; prueba en navegador real sin errores de consola.

## Ejemplo
```js
const ctx = new AudioContext();          // tras gesto del usuario
const osc = ctx.createOscillator();      // triangle: suave para "éxito"
const gain = ctx.createGain();
osc.connect(gain).connect(ctx.destination);
const t = ctx.currentTime;
gain.gain.setValueAtTime(0.0001, t);                  // attack
gain.gain.exponentialRampToValueAtTime(0.3, t + 0.015);
gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.25); // release
osc.frequency.setValueAtTime(880, t);
osc.start(t); osc.stop(t + 0.3);
```

## Errores a evitar
- Iniciar `AudioContext` sin gesto del usuario (autoplay bloqueado).
- Clics por cortes de muestra abruptos (sin envolvente).
- Sonidos largos para feedback instantáneo.
- Entregar con clipping o sin headroom.

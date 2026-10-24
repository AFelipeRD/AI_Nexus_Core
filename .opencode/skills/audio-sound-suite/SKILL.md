---
name: audio-sound-suite
description: "Fórmulas de síntesis con Web Audio API (osciladores, frecuencias, envolventes ADSR), diseño sonoro micro-táctil de baja latencia, TTS/Whisper y análisis espectral. Úsala al crear sonido para interfaces o procesar audio."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.1"
---

# Audio Sound Suite

## Cuándo usar esta skill
- Diseñar sonido de interfaz o micro-interacciones.
- Sintetizar audio en el navegador (Web Audio API).
- Procesar voz: TTS o transcripción (Whisper).
- Generar música o audio completo en la nube (Suno, MMAudio) cuando la síntesis local no basta.

## Generación en la nube vía MCP muapi
Para música completa o bandas sonoras cuando la síntesis local no alcanza (la Web Audio local sigue siendo la base de esta skill):
- `muapi_audio_create` (Suno): música completa con voz e instrumentos desde un prompt.
- `muapi_audio_from_text` (MMAudio): audio generado desde texto.
- Chequeo previo de saldo con `muapi_account_balance`; los artefactos se descargan a `output/`.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `intencion` | feedback, atmósfera, alerta o narración |
| `plataforma` | navegador (Web Audio) o pipeline local |
| `latencia` | presupuesto (interactiva: < 100 ms) |

## Procedimiento
1. **Intención primero**: define qué comunica el sonido (éxito, error, transición, atmósfera); si no comunica, no existe (YAGNI).
2. **La mezcla es relaciones, no una pila de procesadores** (heurística HeyGen): dos pistas que suenan bien por separado pueden ser insoportables juntas; el arreglo casi nunca es «bajar una», es encontrar por qué compiten (frecuencia, espacio) y dárselo a quien lo necesita.
3. **Síntesis Web Audio**: `AudioContext` tras gesto del usuario; osciladores (sine/triangle/square/sawtooth) y ruido; filtros (lowpass/highpass) para timbre.
4. **Envolventes ADSR**: attack corto (5-20 ms) para lo percusivo, release suave (80-300 ms) para evitar clics; `setTargetAtTime` para transiciones sin chasquido. Micro-interacciones: < 100 ms de latencia percibida; el sonido acompaña `transform`/`opacity`, nunca los reemplaza.
5. **Cadenas de efectos por familias**: ganancia, EQ (paso alto/bajo, shelving, peaking), compresor, limitador, gate, saturación, delay, reverb, chorus, phaser, bitcrush — en orden de señal deliberado, no apilado.
6. **Ducking / carve de voz en off**: cuando la música pelea con la voz, automatiza la ganancia de la música bajo la voz en lugar de bajarla a mano.
7. **Voz**: TTS para narración (velocidad y pausas explícitas); Whisper para transcripción con idioma y formato de salida declarados.
8. **Análisis y verificación**: `AnalyserNode` para el espectro; pico ≤ -3 dBFS (headroom), sin clipping; lo que oyes al previsualizar debe ser exactamente lo que se renderiza; prueba en navegador real sin errores de consola.

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

## Referencias comunitarias validadas (find-skills)
- `heygen-com/hyperframes@hyperframes-audio` — **HeyGen oficial, 615 K instalaciones**: mezcla como relaciones, familias de efectos (EQ, compresor, limitador, gate, saturación, delay, reverb), automatización y ducking de voz en off.
- `aahl/skills@edge-tts` — TTS con Edge sin costo de API.
- `theplasmak/faster-whisper@faster-whisper` — transcripción local acelerada con Whisper.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

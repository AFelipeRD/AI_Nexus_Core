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

## Voz y TTS — triple motor (directiva: gratuito y local por defecto)
1. **VoiceStudio (100 % local, motor primario)** — app de escritorio alternativa open source a ElevenLabs (AGPL-3.0, 84.6K estrellas). Con la app abierta expone: MCP `voicestudio` en `http://127.0.0.1:3900/mcp/` (tools `generate_speech`, `clone_voice`, `design_voice`, `transcribe`, `list_voices`, `check_health`) y API OpenAI-compatible en `127.0.0.1:3900` (`/v1/audio/speech`, `/v1/audio/transcriptions`). Clonación de voz con permiso del dueño. Hardware GTX 1050 Ti 4 GB: usa el motor por defecto OmniVoice (k2-fsa) o los del catálogo que quepan en 4 GB VRAM / CPU; la app detecta el hardware y marca compatibilidad por motor. Skill de agente: `voicestudio`.
2. **NVIDIA NIM (cloud gratuita, en preparación)** — `scripts/nvidia_tts.py` resuelve los modelos de voz del catálogo vivo, pero las funciones TTS están publicadas con `apiBodyFormat=CUSTOM` (Triton/gRPC): pendiente el protocolo binario. Hoy no producen audio; cuando NVIDIA habilite JSON o se implemente Triton HTTP, el script las usará solo. Mientras tanto: VoiceStudio (local) o muapi (premium).
3. **muapi (premium)** — variaciones avanzadas de voz/música con chequeo de saldo previo.
**Regla de elección**: si VoiceStudio está abierto → local (privacidad total, voces propias); si no → NIM cloud; premium solo a petición explícita.

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

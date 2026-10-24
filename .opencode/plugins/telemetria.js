// Telemetría de sesiones para el bucle de auto-mejora (self-improvement-auditor).
// Escucha eventos del runtime de OpenCode y anota SOLO contadores y metadatos
// (nunca contenido de mensajes) en logs/telemetria.jsonl, que agrega
// scripts/auto_diagnostico.py. La telemetría jamás debe romper una sesión:
// todo va envuelto en try/catch y fallo silencioso.
import { appendFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";

export const TelemetriaPlugin = async ({ directory }) => {
  const destino = join(directory, "logs", "telemetria.jsonl")

  const anotar = (tipo, datos) => {
    try {
      mkdirSync(dirname(destino), { recursive: true })
      appendFileSync(destino, JSON.stringify({ ts: new Date().toISOString(), tipo, ...datos }) + "\n", "utf8")
    } catch {
      // telemetría best-effort: nunca interrumpir la sesión
    }
  }

  const idSesion = (props) => props?.id ?? props?.sessionID ?? props?.session ?? "desconocida"

  return {
    event: async ({ event }) => {
      try {
        const p = event.properties
        switch (event.type) {
          case "session.created":
            anotar("sesion_creada", { sesion: idSesion(p) })
            break
          case "session.idle":
            anotar("turno_completado", { sesion: idSesion(p) })
            break
          case "session.error":
            anotar("fallo_sesion", { sesion: idSesion(p) })
            break
          case "session.compacted":
            anotar("compactacion", { sesion: idSesion(p) })
            break
          case "permission.asked":
            anotar("permiso_pedido", { sesion: idSesion(p) })
            break
        }
      } catch {
        // ignorar
      }
    },
    "tool.execute.after": async (input, output) => {
      try {
        const fallo =
          output?.error != null ||
          (typeof output?.exitCode === "number" && output.exitCode !== 0) ||
          (output?.canceled === true)
        if (fallo) {
          anotar("fallo_herramienta", {
            sesion: input?.sessionID ?? "desconocida",
            herramienta: input?.tool ?? "desconocida",
          })
        }
      } catch {
        // ignorar
      }
    },
  }
}

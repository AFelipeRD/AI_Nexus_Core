// Telemetria de sesiones para el bucle de auto-mejora (self-improvement-auditor).
// Formato plugin v2 de OpenCode: export default { id, setup } (verificado contra
// packages/core/src/plugin/module.ts de anomalyco/opencode).
// EVIDENCIA DE ERROR PREVIO: el host v2 NO pasa `directory` en el contexto de
// setup (TypeError: "paths[0]" property must be of type string, got undefined
// en join), por eso la raiz del proyecto se deriva de la ubicacion del propio
// plugin (.opencode/plugins/telemetria.js -> ../../ = D:\AI_Nexus_Core) y solo
// se usa ctx.directory si llega como string no vacio.
// Escucha eventos del runtime y anota SOLO contadores y metadatos (nunca
// contenido de mensajes) en logs/telemetria.jsonl, que agrega
// scripts/auto_diagnostico.py. La telemetria jamas debe romper una sesion.
import { appendFileSync, mkdirSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const RAIZ_PLUGIN = fileURLToPath(new URL("../../../", import.meta.url))

export default {
  id: "telemetria",
  setup: async (ctx) => {
    const base =
      typeof ctx?.directory === "string" && ctx.directory.length > 0
        ? ctx.directory
        : RAIZ_PLUGIN
    const destino = join(base, "logs", "telemetria.jsonl")

    const anotar = (tipo, datos) => {
      try {
        mkdirSync(dirname(destino), { recursive: true })
        appendFileSync(destino, JSON.stringify({ ts: new Date().toISOString(), tipo, ...datos }) + "\n", "utf8")
      } catch {
        // telemetria best-effort: nunca interrumpir la sesion
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
            output?.canceled === true
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
  },
}

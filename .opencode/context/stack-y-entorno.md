# Stack y entorno

| Componente | Detalle |
|---|---|
| Sistema | Windows 11, terminal Warp, PowerShell |
| Agente de código | OpenCode (configuración en `opencode.json`) |
| Modelo local | `ollama/qwen2.5-coder:7b` · `http://127.0.0.1:11434/v1` |
| Embeddings locales | `nomic-embed-text` (Ollama, 768 dimensiones) |
| Fallback | OmniRoute (`OMNIROUTE_BASE_URL`), costo cero |
| Python | 3.10+ con entorno `.venv` (ver `requirements.txt`) |
| Node | LTS actual, necesario para `npx` de los servidores MCP |
| Datos | DuckDB y Polars sobre `data/` |
| Memoria | `MEMORY.md` + `memoria/` + `.lightrag/` + MCP Claude-Mem |
| Bóveda | Obsidian abriendo `D:\AI_Nexus_Core` |

Comprobaciones rápidas:
```
ollama list
ollama pull qwen2.5-coder:7b
ollama pull nomic-embed-text
node --version
python --version
```

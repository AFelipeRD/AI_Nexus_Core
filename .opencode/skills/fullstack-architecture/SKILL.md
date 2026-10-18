---
name: fullstack-architecture
description: "Principios de integración frontend-backend con contratos tipados, gestión de estado mínima, APIs seguras y despliegue local rápido. Úsala al construir aplicaciones web completas."
license: MIT
compatibility: opencode
metadata:
  idioma: es
  version: "1.0"
---

# Fullstack Architecture

## Cuándo usar esta skill
- Construir o refactorizar una aplicación web completa.
- Definir el contrato entre frontend y backend.
- Montar un entorno local rápido y reproducible.

## Parámetros de entrada
| Parámetro | Descripción |
|---|---|
| `aplicacion` | qué se va a construir |
| `stack` | preferencias (Next.js/React, FastAPI/Node, SQLite/Postgres/DuckDB) |
| `contrato` | tipos o esquema compartido si ya existe |

## Procedimiento
1. **Contrato primero**: define los tipos compartidos (TypeScript) y el esquema de datos antes de implementar; frontend y backend importan la misma verdad.
2. **Estado mínimo**: server-first (Server Components, loaders); una librería de estado solo con 3 usos reales.
3. **APIs seguras**: validación de entradas en el servidor (zod/pydantic), consultas parametrizadas, errores accionables; REST para CRUD simple, GraphQL solo con grafos de datos reales.
4. **Datos proporcionales**: SQLite/DuckDB para local y prototipos; Postgres cuando existe concurrencia real.
5. **Despliegue local rápido**: un solo comando para levantar (dev server + BD embebida + seed mínimo).
6. **Verificar**: prueba real de cada endpoint (curl o script) y del flujo E2E crítico antes de declarar terminado.
7. **Rendimiento por prioridad** (heurística Vercel): primero elimina cascadas de `await` (paraleliza con `Promise.all`), luego el bundle (imports dinámicos, sin barrel imports), luego el servidor (hoist de IO estático, sin estado compartido entre módulos); re-render y micro-optimizaciones al final.

## Ejemplo
```ts
// contrato compartido — la única verdad de la frontera
export interface Venta {
  id: number;
  region: string;
  total_centavos: number; // dinero en enteros: sin flotantes
}
```

## Errores a evitar
- Implementar antes de definir el contrato.
- Librerías de estado globales para datos que ya viven en el servidor.
- Microservicios o colas «por si acaso» (YAGNI).
- Dinero en punto flotante.

## Referencias comunitarias validadas (find-skills)
- `vercel-labs/agent-skills@vercel-react-best-practices` — **Vercel oficial, 813 K instalaciones**: 70+ reglas de rendimiento React/Next.js priorizadas por impacto (cascadas, bundle, servidor, re-render, patrones avanzados).
- `addyosmani/agent-skills@api-and-interface-design` — Addy Osmani (Google): diseño de contratos de API e interfaces.
- `mattpocock/skills@setup-ts-deep-modules` — Matt Pocock: módulos TypeScript profundos y tipado estricto.
- Cuando la tarea lo exija, profundiza con `npx -y skills find <término>`.

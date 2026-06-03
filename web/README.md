# Fabric — TypeScript client (single language)

The platform standardizes on **one language: TypeScript**, because the browser
UI must run JS/TS — so TS is the only choice that unifies UI + logic.

## Architecture: SurrealDB is the backend

```
Browser / Node (TypeScript)  ──ws──▶  SurrealDB
                                       (auth · record/field permissions ·
                                        graph queries · live queries)
```

There is **no separate API server**. The browser connects directly to SurrealDB,
which enforces permissions and runs the queries. Same `fabric.ts` runs:

- in the browser against remote SurrealDB (`wss://…`)
- in the browser **fully embedded** (`indxdb://fabric`) — "browser as server"
- in Node/Deno/Bun for scripts and tests

## What this replaces

| Was | Now |
|-----|-----|
| `api/server.py` (Python prototype) | `web/fabric.ts` → SurrealDB direct |
| `fabric-db/` (Rust engine sketch) | SurrealDB (the real engine) + TS client |
| Python `codegen/` | keep for now; port to TS later |

`api/server.py` and `fabric-db/` remain as reference prototypes but are **legacy** —
the TypeScript + SurrealDB path is the single-language direction.

## "Implement all features"

SurrealDB **already implements** the features (multi-model, graph, live queries,
auth, permissions, full-text & vector search, transactions). We don't reimplement
a database — we **use** them via `fabric.ts` + the generated schema
(`gen/graph/schema.surql`). The feature catalog (`site/catalog/features.html`)
documents each one.

## Usage

```ts
import { connectFabric, signup, live } from "./fabric";

const db = await connectFabric();              // env-driven endpoint/creds
const ada = await signup(db, { name: "Ada", email: "ada@example.com" });
await live(db, "event", (action, ev) => console.log(action, ev));  // LIVE SELECT
```

Install: `npm install` · Typecheck: `npm run typecheck` · Demo: `npm run demo`

> Not compiled in this environment (no npm/network). Targets `surrealdb` JS SDK v1.x.

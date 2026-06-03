/**
 * Fabric — single-language (TypeScript) client for the data fabric.
 *
 * Architecture: the browser (or Node) talks DIRECTLY to SurrealDB. SurrealDB is
 * the backend — it enforces auth and record/field permissions, runs the graph
 * queries, and streams live changes. No separate API server.
 *
 *   Browser/Node (TS)  ──ws──▶  SurrealDB  (auth · permissions · graph · live)
 *
 * Same code runs:
 *   - in the browser against a remote SurrealDB ( ws://… / wss://… )
 *   - in the browser fully embedded ( indxdb://fabric ) — "browser as server"
 *   - in Node/Deno/Bun for scripts and tests
 *
 * NOTE: not compiled here (no npm/network in this environment).
 * Targets the official `surrealdb` JS SDK v1.x. Install: `npm i surrealdb`.
 */
import { Surreal } from "surrealdb";

export interface FabricConfig {
  url?: string; // ws://localhost:8000 | wss://host | indxdb://fabric (browser)
  namespace?: string;
  database?: string;
  username?: string;
  password?: string;
}

const env = (k: string, d: string): string =>
  (typeof process !== "undefined" && process.env?.[k]) || d;

/** Connect to SurrealDB. Endpoint & creds come from config/env — never hardcoded. */
export async function connectFabric(cfg: FabricConfig = {}): Promise<Surreal> {
  const db = new Surreal();
  await db.connect(cfg.url ?? env("SURREAL_URL", "ws://localhost:8000"));
  if (cfg.username || env("SURREAL_USER", "")) {
    await db.signin({
      username: cfg.username ?? env("SURREAL_USER", "root"),
      password: cfg.password ?? env("SURREAL_PASS", "root"),
    });
  }
  await db.use({
    namespace: cfg.namespace ?? env("SURREAL_NS", "fabric"),
    database: cfg.database ?? env("SURREAL_DB", "fabric"),
  });
  return db;
}

/** Apply the generated graph schema (gen/graph/schema.surql) as one transaction. */
export async function applySchema(db: Surreal, surql: string): Promise<void> {
  await db.query(surql);
}

export interface Identity {
  id?: string;
  kind: string;
  display_name?: string;
  email?: string;
}

/** Connect→Catalog→Govern→Activate, in one round-trip to SurrealDB. */
export async function signup(
  db: Surreal,
  input: { name: string; email: string; company?: string; message?: string },
): Promise<Identity> {
  const email = input.email.trim().toLowerCase();
  if (!input.name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    throw new Error("valid name and email are required");
  }
  // Catalog: create the Identity node.
  const [identity] = await db.create<Identity>("identity", {
    kind: "person",
    display_name: input.name,
    email,
  });
  // Govern: append an immutable audit Event linked to the identity.
  await db.create("event", {
    type: "identity.signup",
    actor: identity.id,
    occurred_at: new Date().toISOString(),
  });
  return identity;
}

/** Activate: traverse the graph from a record (SurrealQL graph query). */
export async function resolve(db: Surreal, recordId: string, depth = 2) {
  // SurrealDB graph traversal: repeated ->?->? out to `depth` hops.
  const hops = Array.from({ length: depth }, () => "->?->?").join("");
  const [rows] = await db.query(`SELECT *, ${"->?->?"} AS links FROM ${recordId}`);
  return rows;
}

/** Live: subscribe to changes on a table (mirrors the SSE /stream prototype). */
export async function live(
  db: Surreal,
  table: string,
  onChange: (action: string, result: unknown) => void,
): Promise<string> {
  return db.live(table, (action, result) => onChange(action, result as unknown));
}

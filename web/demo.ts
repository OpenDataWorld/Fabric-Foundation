/**
 * Fabric TS demo — one language, talking straight to SurrealDB.
 * Run: SURREAL_URL=ws://localhost:8000 npm run demo
 * (Requires a running SurrealDB; not executed in CI here.)
 */
import { connectFabric, applySchema, signup, live } from "./fabric.js";
import { readFileSync } from "node:fs";

async function main() {
  const db = await connectFabric();

  // Optional: apply the generated graph schema.
  try {
    const surql = readFileSync(new URL("../gen/graph/schema.surql", import.meta.url), "utf8");
    await applySchema(db, surql);
  } catch { /* schema optional for the demo */ }

  // Live: subscribe to the change feed of events (LIVE SELECT).
  await live(db, "event", (action, ev) => console.log("live:", action, ev));

  // Sign up — creates an Identity + audit Event in SurrealDB.
  const ada = await signup(db, { name: "Ada Lovelace", email: "ada@example.com" });
  console.log("registered:", ada);

  await new Promise((r) => setTimeout(r, 500));
  process.exit(0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});

/**
 * Fabric edge function — Cloudflare Worker (also adaptable to Vercel/Deno Edge).
 *
 * The ONE bit of server-side code: handles signup (and could host live relays)
 * so SurrealDB credentials stay server-side. Everything read-only (graph, model)
 * is served statically from site/data/model.json — no server needed for those.
 *
 * Set secrets:  wrangler secret put SURREAL_URL / SURREAL_USER / SURREAL_PASS
 * NOTE: not built here (no npm/network). Targets the `surrealdb` JS SDK v1.x.
 */
import { connectFabric, signup } from "../fabric";

interface Env {
  SURREAL_URL: string;
  SURREAL_USER: string;
  SURREAL_PASS: string;
  SURREAL_NS: string;
  SURREAL_DB: string;
}

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
    const path = new URL(req.url).pathname.replace(/\/$/, "");

    if (req.method === "POST" && path === "/signup") {
      const body = await req.json().catch(() => ({}));
      try {
        const db = await connectFabric({
          url: env.SURREAL_URL, username: env.SURREAL_USER, password: env.SURREAL_PASS,
          namespace: env.SURREAL_NS, database: env.SURREAL_DB,
        });
        const identity = await signup(db, body as any);
        return Response.json({ status: "registered", identity }, { headers: CORS });
      } catch (e: any) {
        return Response.json({ error: e.message }, { status: 400, headers: CORS });
      }
    }
    return Response.json({ error: "not found" }, { status: 404, headers: CORS });
  },
};

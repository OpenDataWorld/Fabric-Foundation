# Deploying Fabric (alpha) — let real people test

Architecture: **static site + SurrealDB + one tiny edge function**. No app server.

```
Visitor ─▶ Static site (CDN)         read-only: graph, agent browse site/data/model.json
        └▶ Edge function (TS) ─▶ SurrealDB     writes: signup, live
```

You can deploy in **two modes**:

## Mode A — Static only (fastest, read-only)
Graph, catalog, and the Fabric Agent's model browsing work with **zero backend**
(they fall back to `site/data/model.json`). Signup is disabled.

1. Regenerate the static model: `python3 codegen/generate_models.py --target json`
2. Deploy the `site/` folder to any static host (Vercel, Netlify, Cloudflare Pages, GitHub Pages).
3. Done — share the URL. Graph + catalog + agent (browse) work immediately.

## Mode B — Full (signups + live)
Adds the edge function and SurrealDB so real people can create accounts.

### 1. SurrealDB
- Use **SurrealDB Cloud** or self-host (`surreal start`). You said you have a client — point it at your instance.
- Load the schema:
  ```
  surreal import --conn $SURREAL_URL --user $U --pass $P --ns fabric --db fabric gen/graph/schema.surql
  ```

### 2. Edge function (Cloudflare Workers example)
```
cd web && npm install
cd edge
wrangler secret put SURREAL_URL    # wss://<host>.surreal.cloud
wrangler secret put SURREAL_USER
wrangler secret put SURREAL_PASS
wrangler deploy                     # prints https://fabric-edge.<you>.workers.dev
```
(Adaptable to Vercel Edge / Deno Deploy — same `fetch(req, env)` shape.)

### 3. Point the site at it
Edit `site/config.js`:
```js
window.FABRIC_API_BASE = "https://fabric-edge.<you>.workers.dev";
window.FABRIC_LLM_URL  = "https://<your-tinyllm-agent>/chat"; // optional
```
Redeploy `site/`. Signup now creates real `Identity` + audit `Event` records in SurrealDB; the Fabric Agent can call your tinyLLM.

## Optional — Fabric Agent (tinyLLM)
Set `FABRIC_LLM_URL` to your packed tinyLLM endpoint (accepts `{messages}`,
returns `{reply}` or OpenAI-style `{choices}`). Empty = command-only agent.

## What you provide vs. what's ready
- **Ready:** static site, model export, edge function code, schema, config hooks.
- **You provide:** a SurrealDB instance + a host account, then set `config.js`.
That's the only gap between "runs locally" and "real people testing."

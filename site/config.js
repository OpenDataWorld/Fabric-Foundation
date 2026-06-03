// Fabric deployment config — edit these for production, no rebuild needed.
//
// FABRIC_API_BASE: URL of the Data Model API / edge function that handles
//   signup + live (writes to SurrealDB). Leave pointing at an unreachable
//   value to run the site in static, read-only mode (graph + agent browse the
//   bundled data/model.json; signup is disabled).
//
// FABRIC_LLM_URL: endpoint of your packed tinyLLM agent (takes {messages} and
//   returns {reply} or OpenAI-style {choices}). Empty = command-only agent.
window.FABRIC_API_BASE = "";   // e.g. "https://fabric-edge.<you>.workers.dev"
window.FABRIC_LLM_URL  = "";   // e.g. "https://<your-tinyllm-agent>/chat"
window.FABRIC_CONTACT_ENDPOINT = ""; // e.g. Formspree URL; empty = mailto fallback

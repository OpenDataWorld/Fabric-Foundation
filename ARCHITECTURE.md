# Fabric — Architecture & First Principles

This document states the design philosophy of the platform built on the Fabric
primitives. It is the *why* behind the model; the YAML primitives are the *what*.

> These principles were derived deliberately. They are not defaults — each one
> is a design decision with a cost the alternative would have incurred.

---

## 0. The law: everything important is a State

**If it matters, it is a `State` in the graph. If it is not in the graph, it
does not officially matter.**

Everything else follows from this:

- The core is fundamentally a **state store** (the graph / SurrealDB).
- The *only* way importance changes is an **`Event`** — `Event advances State`.
- **Memory** is the recorded states and events the runtime can read back.
- A **`Journey`** is the emergent *trace* of states — descriptive, never prescribed.
- Importance ⇒ observable, persisted, governed — because it is a State, not
  hidden in some service's RAM.

`State is real.`

---

## 1. The core is the graph

```
CORE (protocol-agnostic)
  Runtime = the graph (SurrealDB substrate)
          + Identity        (who acts / is acted upon)
          + Memory          (recorded Events / State, read back)
          + Agents          (which act on the graph)
  Runtime delivers an SLA   (guaranteed Objectives: availability, latency, durability)
```

- **SurrealDB is the substrate** — the one non-tool. Everything else is a tool.
- The core **never embeds a wire protocol**. It speaks graph, not HTTP.
- The core is a small, *stable* kernel (high fan-in, low fan-out) — which, in
  Martin's dependency metrics, is exactly what keeps architectural debt low.

---

## 2. Everything else is a tool; protocols are sidecars

```
        ┌──────────────── SIDECARS (protocols, = agents) ───────────────┐
        │  https · grpc · mcp · kafka · sql · custom …                   │
        │  each binds/translates a Protocol at the edge                  │
        └───────────────────────────┬────────────────────────────────────┘
                                     │  Touchpoints (speak a Protocol)
        ┌─────────────────────────────▼──────────────────────────────────┐
        │  CORE = the graph + identity + memory + agents                  │
        └───────────────────────────────────────────────────────────────────┘
```

- **Protocols are sidecars, never core.** Adding/changing a protocol means
  deploying an adapter — it must never require changing core code.
- **Sidecars *are* agents.** A protocol adapter is an Agent that guards a
  Touchpoint and does the binding. The edge is all agents; the core is the graph.

---

## 3. Touchpoints & protocols (the boundaries)

- A **`Touchpoint`** is a junction where two or more things interact. It is
  **only needed at a boundary** — where the things differ in *type* or
  *surface/protocol*. Same type + same surface on both sides is **seamless**
  (e.g. agent↔agent over **A2A** is *not* a touchpoint).
- Every touchpoint declares a **surface** and a **protocol**. If no protocol
  exists for a boundary, a **`Protocol` is defined** (a reusable asset).
- A boundary with **no covering touchpoint is a design gap** — it must be
  reported: *"the system design does not cover that touchpoint."*
- The **agent language is the binding language** that translates across
  heterogeneous touchpoints (agent↔tool uses **MCP**).
- **The binding language must be ambiguity-free.** Every term resolves to
  exactly one meaning — grounded in the graph's IRIs (each attribute carries a
  `schema:sameAs` mapping in the JSON-LD export). No term is overloaded; meaning
  is the same on both sides of a touchpoint, so translation is deterministic.
  Ambiguity at a boundary *is* a defect, not a tolerance.

---

## 4. Agents are autonomous; the path is emergent

- An agent's path through the state/journey graph is **emergent and
  non-mandatory**. The graph is *possibility space*, not a required flow.
- An agent is bounded **only by Policy / Constraint** — never by a prescribed
  route. Within those bounds it is free.
- This is the opposite of a rigid pipeline: the DAG is optional, the agent decides.
- **An agent's definition depends only on the stable core** (existing State,
  Identity, the graph) — **never on future or not-yet-real things.** You cannot
  define an agent on what doesn't exist yet. Depend toward stability; that is
  what keeps the agent layer free of the Unstable Dependency smell.

---

## 5. Debt discipline (why this shape)

Per architectural-debt research, the dangerous smells are **Cyclic**,
**Hub-Like**, and **Unstable** dependencies — at the *component* layer.

- **Semantic cycles are fine.** The model is an ontology; `Policy ↔ Constraint ↔
  Objective` referencing each other is *meaning*, not a dependency cycle.
- **The component layer stays acyclic.** "Protocols are sidecars" makes
  dependencies flow one way (sidecar → core), structurally preventing the
  core↔adapter cycle — the #1 smell.
- **The core avoids being a hub/god-object** because behaviour lives at the
  edge in many small agents, not in the kernel.

So the sidecar/core split isn't aesthetic — it's the ATD-minimizing decision.

---

## In one breath

> The core is the graph. Everything important is a State; Events advance it;
> Memory is what was recorded. Identity and Agents are core; everything else is
> a tool. Protocols live in sidecars (which are agents) at Touchpoints on the
> boundaries; define one where none exists. Agents are autonomous — the path is
> emergent, bounded only by governance. The runtime delivers an SLA.

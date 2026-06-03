# Fabric ↔ Adobe XDM alignment

Adobe's **Experience Data Model (XDM)** is the canonical, composable schema
system behind Adobe Experience Platform (a leading CDP). Aligning Fabric's data
model with XDM makes Fabric **interoperable with the standard the Customer Data
Platform market already speaks** — and validates Fabric's design, because the two
line up almost one-to-one.

## Concept mapping

| Adobe XDM | Fabric | Notes |
|-----------|--------|-------|
| **Class** — defines the base structure & behavior of data (e.g. *XDM Individual Profile*, *XDM ExperienceEvent*) | **Primitive** (`Thing`, `Identity`, `Event`, …) | The foundation a schema is built on. |
| **Schema** — a class composed with one or more field groups | **Composed asset type** | What you actually instantiate. |
| **Field group** — reusable bundle of fields that extends a class (e.g. *Demographic Details*) | **Attribute mixin** *(to add)* | Reusable, composable — the modular pattern that makes shared models succeed. |
| **Data type** — reusable multi-field structure (e.g. *Address*, *Person Name*) | Complex attribute types (`param`, `metric`, geo) | Building blocks inside field groups. |
| **Identity Map** | `Identity` primitive | Cross-source identity resolution. |
| **Behavior: Record** (time-stamped snapshot) | `State` primitive | "What condition is it in now?" |
| **Behavior: Time-series** (immutable events) | `Event` primitive | "What happened?" (append-only). |

## Why this matters

1. **CDP-market credibility.** XDM interop means Adobe Experience Platform
   customers can map their schemas onto Fabric — directly relevant to the
   Customer 360 / CDP solution and the *Customer Data Platforms* Gartner market.
2. **Design validation.** Fabric's `Event` vs `State` split independently
   reproduces XDM's Time-series vs Record behavior — strong evidence the
   primitive decomposition is sound.
3. **Modularity = the success pattern.** XDM's "class + field groups" composition
   is the loose, modular approach the data-fabric research found in every winning
   shared-semantics effort (schema.org, FIBO). Fabric should adopt it explicitly.

## The one gap to close: field groups

Fabric currently has **primitives (classes)** and **complex types**, but not the
middle layer of **reusable field groups**. Adding them lets domain schemas be
*composed* rather than redefined — e.g.:

```
schema: CustomerProfile
  class:  fabric:primitive:identity        # the base primitive
  field_groups:
    - contact-details        # email, phone, address (reusable)
    - demographics           # name, birthDate, gender (reusable)
    - consent-and-privacy    # governed by Policy
```

This mirrors XDM exactly and keeps Fabric loose and modular.

## Interop path

- **Import:** map XDM `class` → Fabric primitive, XDM `field group`/`data type` →
  Fabric field groups/types, XDM `identityMap` → `Identity`.
- **Export:** the data-model generator (`codegen/`) can emit XDM-compatible
  JSON Schema for the relevant primitives.
- **Both directions** stay schema.org-aligned, since XDM itself is influenced by
  schema.org and standard vocabularies.

## Status

This is an alignment **specification**, not an implementation. Next step if
pursued: add a `field-groups/` layer to the model and an XDM emit target in the
generator.

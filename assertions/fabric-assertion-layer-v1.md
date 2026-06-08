# Fabric Assertion Layer v1.0

## Purpose

The Fabric Assertion Layer extends the Fabric Foundation Primitive Layer with a signed, verifiable, append-only operating model.

The foundation primitives answer:

```text
What exists?
Who or what is it?
When and where does it apply?
How is it connected?
What can be done?
What is constrained?
What is allowed?
Why does it matter?
What proves it?
What can go wrong?
```

The assertion layer answers:

```text
Who claimed it?
Can it be verified?
Is it trusted?
What projection does it produce?
Has reality drifted?
How is conformance restored?
```

## Canonical Assertion Records

The assertion layer reduces governed operation to seven records:

1. `Entity`
2. `Relationship`
3. `Assertion`
4. `Observation`
5. `Projection`
6. `Drift`
7. `Reconciliation`

These records do not replace the existing Fabric Foundation primitives. They operationalize them.

## Mapping to Foundation Primitives

| Assertion Layer | Foundation Primitive Alignment |
|---|---|
| Entity | Thing, Identity |
| Relationship | Relationship |
| Assertion | Evidence, Policy, Capability, Constraint, Objective |
| Observation | Event, State, Evidence |
| Projection | State, Journey, Metric |
| Drift | Risk, Constraint, Control |
| Reconciliation | Policy, Control, Objective, Event |

## Core Rule

```text
Assertions are source of truth.
Projections are derived views.
Runtime state is never authoritative.
```

## Minimal Envelope

Every assertion-layer record MUST contain:

```yaml
apiVersion: fabric.opendataworld.org/v1
kind:
id:
issuer:
timestamp:
signature:
metadata:
```

## Required Protocol Verbs

A conformant Fabric implementation MUST support:

```text
ASSERT
OBSERVE
VERIFY
PROJECT
COMPARE
RECONCILE
```

## Kernel Boundary

The assertion-native kernel contains only:

```text
Identity
Assertion Store
Verification
Projection
Drift Detection
Reconciliation
```

Everything else is an extension.

## Canonical Law

```text
Identity establishes existence.
Relationships establish context.
Assertions establish truth.
Observations establish reality.
Projections establish visibility.
Drift establishes difference.
Reconciliation establishes order.
```

## Status

Draft v1.0 extension for the Fabric Foundation Primitive Layer.

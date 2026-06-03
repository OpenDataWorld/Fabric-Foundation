// Generated from Fabric primitives — DO NOT EDIT BY HAND.

/** What can this thing do?  (fabric:primitive:capability) */
export interface Capability {
  id: string;
  name: string;
  verb: string;
  inputs?: Record<string, unknown>[];
  outputs?: Record<string, unknown>[];
  requiresTools?: string[];
  requiresResources?: string[];
  maturity?: string;
}

/** What must hold or is forbidden?  (fabric:primitive:constraint) */
export interface Constraint {
  id: string;
  kind: string;
  expression: string;
  target?: string;
  severity?: string;
  onViolation?: string;
}

/** What happened?  (fabric:primitive:event) */
export interface Event {
  id: string;
  type: string;
  occurredAt: string;
  actor?: string;
  subject?: string;
  location?: string;
  payload?: Record<string, unknown>;
}

/** What proves this is true?  (fabric:primitive:evidence) */
export interface Evidence {
  id: string;
  kind: string;
  claim: string;
  source?: string;
  uri?: string;
  hash?: string;
  collectedAt?: string;
}

/** Who or what is it?  (fabric:primitive:identity) */
export interface Identity {
  id: string;
  kind: string;
  displayName?: string;
  controller?: string;
  credentials?: string[];
}

/** Where is it?  (fabric:primitive:location) */
export interface Location {
  id: string;
  kind: string;
  latitude?: number;
  longitude?: number;
  geometry?: string;
  address?: string;
  uri?: string;
}

/** Why are we doing it, and how is success judged?  (fabric:primitive:objective) */
export interface Objective {
  id: string;
  name: string;
  kind: string;
  statement: string;
  metrics?: Record<string, unknown>[];
  targetDate?: string;
  priority?: string;
  status?: string;
}

/** What is allowed, and under what conditions?  (fabric:primitive:policy) */
export interface Policy {
  id: string;
  name: string;
  effect: string;
  combine?: string;
  constraints: string[];
  scope?: Record<string, unknown>;
  precedence?: number;
  owner?: string;
}

/** How are things connected?  (fabric:primitive:relationship) */
export interface Relationship {
  id: string;
  predicate: string;
  source: string;
  target: string;
  directed?: boolean;
  validDuring?: string;
  weight?: number;
}

/** What is consumed, allocated, or required?  (fabric:primitive:resource) */
export interface Resource {
  id: string;
  kind: string;
  unit: string;
  capacity?: number;
  consumed?: number;
  owner?: string;
}

/** What could go wrong, and how bad?  (fabric:primitive:risk) */
export interface Risk {
  id: string;
  category: string;
  statement: string;
  likelihood?: string;
  impact?: string;
  severity?: string;
  status?: string;
}

/** What condition is it in now?  (fabric:primitive:state) */
export interface State {
  id: string;
  subject: string;
  value: string;
  lifecycle?: string;
  since?: string;
  allowedTransitions?: string[];
}

/** What is it?  (fabric:primitive:thing) */
export interface Thing {
  id: string;
  type: string;
  name?: string;
  description?: string;
  createdAt?: string;
  metadata?: Record<string, unknown>;
}

/** When does it occur or apply?  (fabric:primitive:time) */
export interface Time {
  id: string;
  kind: string;
  instant?: string;
  start?: string;
  end?: string;
  duration?: string;
  timezone?: string;
}

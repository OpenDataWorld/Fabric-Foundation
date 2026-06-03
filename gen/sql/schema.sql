-- Generated from Fabric primitives — DO NOT EDIT BY HAND.

CREATE TABLE IF NOT EXISTS capability (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    verb TEXT NOT NULL,
    inputs JSONB,
    outputs JSONB,
    requiresTools JSONB,
    requiresResources JSONB,
    maturity TEXT
);

CREATE TABLE IF NOT EXISTS constraint (
    id TEXT PRIMARY KEY NOT NULL,
    kind TEXT NOT NULL,
    expression TEXT NOT NULL,
    target TEXT,
    severity TEXT,
    onViolation TEXT
);

CREATE TABLE IF NOT EXISTS event (
    id TEXT PRIMARY KEY NOT NULL,
    type TEXT NOT NULL,
    occurredAt TIMESTAMPTZ NOT NULL,
    actor TEXT,
    subject TEXT,
    location TEXT,
    payload JSONB
);

CREATE TABLE IF NOT EXISTS identity (
    id TEXT PRIMARY KEY NOT NULL,
    kind TEXT NOT NULL,
    displayName TEXT,
    controller TEXT,
    credentials JSONB
);

CREATE TABLE IF NOT EXISTS location (
    id TEXT PRIMARY KEY NOT NULL,
    kind TEXT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    geometry JSONB,
    address TEXT,
    uri TEXT
);

CREATE TABLE IF NOT EXISTS objective (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    kind TEXT NOT NULL,
    statement TEXT NOT NULL,
    metrics JSONB,
    targetDate TEXT,
    priority TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS policy (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    effect TEXT NOT NULL,
    combine TEXT,
    constraints JSONB NOT NULL,
    scope JSONB,
    precedence INTEGER,
    owner TEXT
);

CREATE TABLE IF NOT EXISTS relationship (
    id TEXT PRIMARY KEY NOT NULL,
    predicate TEXT NOT NULL,
    source TEXT NOT NULL,
    target TEXT NOT NULL,
    directed BOOLEAN,
    validDuring TEXT,
    weight DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS state (
    id TEXT PRIMARY KEY NOT NULL,
    subject TEXT NOT NULL,
    value TEXT NOT NULL,
    lifecycle TEXT,
    since TIMESTAMPTZ,
    allowedTransitions JSONB
);

CREATE TABLE IF NOT EXISTS thing (
    id TEXT PRIMARY KEY NOT NULL,
    type TEXT NOT NULL,
    name TEXT,
    description TEXT,
    createdAt TIMESTAMPTZ,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS time (
    id TEXT PRIMARY KEY NOT NULL,
    kind TEXT NOT NULL,
    instant TIMESTAMPTZ,
    start TIMESTAMPTZ,
    end TIMESTAMPTZ,
    duration TEXT,
    timezone TEXT
);

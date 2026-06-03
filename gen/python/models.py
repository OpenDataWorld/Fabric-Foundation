"""Generated from Fabric primitives — DO NOT EDIT BY HAND."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Account:
    """Which provider account is this?  (fabric:primitive:account)"""
    id: str
    provider: str
    provider_sub: str
    email: Optional[str] = None
    username: Optional[str] = None


@dataclass
class Capability:
    """What can this thing do?  (fabric:primitive:capability)"""
    id: str
    name: str
    verb: str
    inputs: list[dict] = field(default_factory=list)
    outputs: list[dict] = field(default_factory=list)
    requiresTools: list[str] = field(default_factory=list)
    requiresResources: list[str] = field(default_factory=list)
    maturity: Optional[str] = None


@dataclass
class Constraint:
    """What must hold or is forbidden?  (fabric:primitive:constraint)"""
    id: str
    kind: str
    expression: str
    target: Optional[str] = None
    severity: Optional[str] = None
    onViolation: Optional[str] = None


@dataclass
class Credential:
    """What is verifiably asserted about an identity?  (fabric:primitive:credential)"""
    id: str
    type: str
    claim: Optional[dict] = None
    proof: Optional[str] = None


@dataclass
class DataType:
    """What reusable structure does this field hold?  (fabric:primitive:datatype)"""
    id: str
    name: str
    fields: list[dict] = field(default_factory=list)


@dataclass
class Device:
    """What endpoint was used?  (fabric:primitive:device)"""
    id: str
    kind: str
    fingerprint: Optional[str] = None


@dataclass
class Event:
    """What happened?  (fabric:primitive:event)"""
    id: str
    type: str
    occurredAt: datetime
    actor: Optional[str] = None
    subject: Optional[str] = None
    location: Optional[str] = None
    payload: Optional[dict] = None


@dataclass
class Evidence:
    """What proves this is true?  (fabric:primitive:evidence)"""
    id: str
    kind: str
    claim: str
    source: Optional[str] = None
    uri: Optional[str] = None
    hash: Optional[str] = None
    collectedAt: Optional[datetime] = None


@dataclass
class FieldGroup:
    """Which reusable set of fields extends a class?  (fabric:primitive:fieldgroup)"""
    id: str
    name: str
    fields: list[dict] = field(default_factory=list)


@dataclass
class Identity:
    """Who or what is it?  (fabric:primitive:identity)"""
    id: str
    kind: str
    displayName: Optional[str] = None
    controller: Optional[str] = None
    credentials: list[str] = field(default_factory=list)


@dataclass
class Location:
    """Where is it?  (fabric:primitive:location)"""
    id: str
    kind: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geometry: Optional[str] = None
    address: Optional[str] = None
    uri: Optional[str] = None


@dataclass
class Objective:
    """Why are we doing it, and how is success judged?  (fabric:primitive:objective)"""
    id: str
    name: str
    kind: str
    statement: str
    metrics: list[dict] = field(default_factory=list)
    targetDate: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


@dataclass
class Policy:
    """What is allowed, and under what conditions?  (fabric:primitive:policy)"""
    id: str
    name: str
    effect: str
    constraints: list[str]
    combine: Optional[str] = None
    scope: Optional[dict] = None
    precedence: Optional[int] = None
    owner: Optional[str] = None


@dataclass
class Relationship:
    """How are things connected?  (fabric:primitive:relationship)"""
    id: str
    predicate: str
    source: str
    target: str
    directed: Optional[bool] = None
    validDuring: Optional[str] = None
    weight: Optional[float] = None


@dataclass
class Resource:
    """What is consumed, allocated, or required?  (fabric:primitive:resource)"""
    id: str
    kind: str
    unit: str
    capacity: Optional[float] = None
    consumed: Optional[float] = None
    owner: Optional[str] = None


@dataclass
class Risk:
    """What could go wrong, and how bad?  (fabric:primitive:risk)"""
    id: str
    category: str
    statement: str
    likelihood: Optional[str] = None
    impact: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None


@dataclass
class Schema:
    """How is this entity's structure composed?  (fabric:primitive:schema)"""
    id: str
    name: str
    baseClass: str


@dataclass
class Session:
    """When and how was access established?  (fabric:primitive:session)"""
    id: str
    started: Optional[datetime] = None
    ip: Optional[str] = None


@dataclass
class Source:
    """Where does this data or account come from?  (fabric:primitive:source)"""
    id: str
    kind: str
    name: str
    endpoint: Optional[str] = None


@dataclass
class State:
    """What condition is it in now?  (fabric:primitive:state)"""
    id: str
    subject: str
    value: str
    lifecycle: Optional[str] = None
    since: Optional[datetime] = None
    allowedTransitions: list[str] = field(default_factory=list)


@dataclass
class Thing:
    """What is it?  (fabric:primitive:thing)"""
    id: str
    type: str
    name: Optional[str] = None
    description: Optional[str] = None
    createdAt: Optional[datetime] = None
    metadata: Optional[dict] = None


@dataclass
class Time:
    """When does it occur or apply?  (fabric:primitive:time)"""
    id: str
    kind: str
    instant: Optional[datetime] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    duration: Optional[str] = None
    timezone: Optional[str] = None


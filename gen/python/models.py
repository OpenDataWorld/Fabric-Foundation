"""Generated from Fabric primitives — DO NOT EDIT BY HAND."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


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


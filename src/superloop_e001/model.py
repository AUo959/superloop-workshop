"""Core E001 state and canonical trace representations."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


LOOP_IDS = ("A", "B", "C")
NEXT_LOOP = {"A": "B", "B": "C", "C": "A"}
ROUTES = {
    "A": ("A", "B", "C"),
    "B": ("B", "C", "A"),
    "C": ("C", "A", "B"),
}

TRACE_FIELDS = (
    "schema_version",
    "run_id",
    "configuration",
    "scenario",
    "seed",
    "workload_digest",
    "event_id",
    "simulation_tick",
    "event_type",
    "loop_id",
    "interlock_id",
    "work_id",
    "parent_event_ids",
    "validation_state",
    "credit_before",
    "credit_after",
    "occupancy_before",
    "occupancy_after",
    "lease_fresh_until",
    "obligation_created",
    "obligation_resolved",
    "provenance_complete",
    "invariant_checks",
    "terminal_state",
    "terminal_reason",
)


def canonical_json(value: Any) -> str:
    """Serialize a JSON-compatible value deterministically."""

    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def digest(value: Any) -> str:
    """Return a SHA-256 digest of canonical JSON."""

    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def raw_digest(value: str) -> str:
    """Return a SHA-256 digest of exact UTF-8 text bytes."""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Offer:
    """One externally offered work event."""

    tick: int
    work_id: str
    source_loop: str
    schema_version: str = "e001.work.v1"
    duplicate_replay: bool = False

    def canonical(self) -> dict[str, Any]:
        return {
            "duplicate_replay": self.duplicate_replay,
            "schema_version": self.schema_version,
            "source_loop": self.source_loop,
            "tick": self.tick,
            "work_id": self.work_id,
        }


@dataclass
class WorkItem:
    """Authoritative work state while an item is active."""

    work_id: str
    source_loop: str
    route: tuple[str, str, str]
    route_index: int
    created_at: int
    admitted_at: int
    deadline: int
    schema_version: str
    payload_digest: str
    priority: str = "normal"
    provenance: list[str] = field(default_factory=list)
    processed: bool = False

    @property
    def location(self) -> str:
        return self.route[self.route_index]

    @property
    def final_stage(self) -> bool:
        return self.route_index == len(self.route) - 1


@dataclass
class LoopState:
    """Bounded local reservoir and FIFO work ordering."""

    loop_id: str
    capacity: int
    queue: list[str] = field(default_factory=list)

    @property
    def occupancy(self) -> int:
        return len(self.queue)

    @property
    def free_capacity(self) -> int:
        return self.capacity - self.occupancy


class TraceRecorder:
    """Construct canonical, complete transition records."""

    def __init__(
        self,
        *,
        configuration: str,
        scenario: str,
        seed: int,
        workload_digest: str,
    ) -> None:
        self.configuration = configuration
        self.scenario = scenario
        self.seed = seed
        self.workload_digest = workload_digest
        self.run_id = f"{configuration}__{scenario}__seed-{seed}"
        self.events: list[dict[str, Any]] = []
        self._sequence = 0

    def emit(self, *, simulation_tick: int, event_type: str, **values: Any) -> str:
        self._sequence += 1
        event_id = f"{self.run_id}:{self._sequence:07d}"
        record = {field_name: None for field_name in TRACE_FIELDS}
        record.update(
            {
                "schema_version": "e001.trace.v1",
                "run_id": self.run_id,
                "configuration": self.configuration,
                "scenario": self.scenario,
                "seed": self.seed,
                "workload_digest": self.workload_digest,
                "event_id": event_id,
                "simulation_tick": simulation_tick,
                "event_type": event_type,
                "parent_event_ids": [],
                "obligation_created": False,
                "obligation_resolved": False,
                "invariant_checks": [],
            }
        )
        unknown = set(values) - set(TRACE_FIELDS)
        if unknown:
            raise ValueError(f"unknown trace fields: {sorted(unknown)}")
        record.update(values)
        self.events.append(record)
        return event_id

    def jsonl(self) -> str:
        if not self.events:
            return ""
        return "\n".join(canonical_json(event) for event in self.events) + "\n"

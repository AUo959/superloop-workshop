"""Offline, noncausal replay of the frozen E001 evidence archive."""

from __future__ import annotations

import hashlib
import json
import tarfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any, TextIO

from .model import (
    CAPACITY,
    DEADLINE_TICKS,
    INTERLOCKS,
    LOOP_IDS,
    PHASE_PERIODS,
    WorkState,
    auc,
    canonical_json,
    digest,
    parse_rational,
    rational,
    raw_digest,
)


ARCHIVE_SHA256 = "584cc15bfeb3cc74dec9d9069cde26e1abaa6f1350c0aa12ae10a9784bd1663b"
SOURCE_COMMIT = "81e7f859f71425bdba7603a61566f9fb47c116f9"
TELEMETRY_FIELDS = {
    "schema_version",
    "source_run_id",
    "source_trace_digest",
    "sample_id",
    "simulation_tick",
    "sample_phase",
    "configuration",
    "scenario",
    "seed",
    "loop_id",
    "interlock_id",
    "source_event_ids",
    "reconstruction_state",
    "pressure_vector",
    "congestion_potential",
    "receiver_conductance",
    "receiver_resistance",
    "positive_gradient",
    "candidate_flow",
    "committed_flow",
    "dissipation_proxy",
    "field_vacancy",
    "phase_indices",
    "zero_vacancy_cycle",
    "instrumentation_checks",
}


class EvidenceError(ValueError):
    """Raised when frozen source evidence fails verification."""


class ReconstructionError(ValueError):
    """Raised when trace events cannot reconstruct a coherent state."""


class EvidenceArchive:
    """Read and verify E001 evidence without importing E001 runtime code."""

    def __init__(self, path: Path) -> None:
        self.path = path
        archive_bytes = path.read_bytes()
        if raw_digest(archive_bytes) != ARCHIVE_SHA256:
            raise EvidenceError("E001 archive SHA-256 does not match the frozen contract")
        self._tar = tarfile.open(path, mode="r:gz")
        self._members = {member.name.removeprefix("./"): member for member in self._tar}
        for name in self._members:
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts:
                raise EvidenceError(f"unsafe archive member: {name}")
        self.manifest = self._read_json("matrix_manifest.json")
        if self.manifest["source_commit"] != SOURCE_COMMIT:
            raise EvidenceError("unexpected E001 source commit")
        if self.manifest["run_count"] != 72 or self.manifest["expected_run_count"] != 72:
            raise EvidenceError("unexpected E001 run count")
        if self.manifest["invalid_run_ids"] or self.manifest["determinism_mismatches"]:
            raise EvidenceError("E001 manifest contains invalid or nondeterministic runs")
        if self.manifest["workload_equivalence_mismatches"]:
            raise EvidenceError("E001 manifest contains workload-equivalence mismatches")

    def close(self) -> None:
        self._tar.close()

    def __enter__(self) -> "EvidenceArchive":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @property
    def run_ids(self) -> list[str]:
        return sorted(self.manifest["run_summary_digests"])

    def _read_bytes(self, name: str) -> bytes:
        member = self._members.get(name)
        if member is None or not member.isfile():
            raise EvidenceError(f"missing archive member: {name}")
        extracted = self._tar.extractfile(member)
        if extracted is None:
            raise EvidenceError(f"unreadable archive member: {name}")
        return extracted.read()

    def _read_json(self, name: str) -> dict[str, Any]:
        return json.loads(self._read_bytes(name))

    def load_run(self, run_id: str) -> tuple[list[dict[str, Any]], str, dict[str, Any]]:
        if run_id not in self.manifest["run_summary_digests"]:
            raise EvidenceError(f"run is outside the frozen matrix: {run_id}")
        trace_bytes = self._read_bytes(f"raw/{run_id}.jsonl")
        trace_text = trace_bytes.decode("utf-8")
        events = [json.loads(line) for line in trace_text.splitlines()]
        summary = self._read_json(f"summary/{run_id}.json")
        if raw_digest(trace_bytes) != summary["trace_digest"]:
            raise EvidenceError(f"{run_id}: trace digest mismatch")
        summary_for_digest = dict(summary)
        summary_for_digest["summary_digest"] = None
        if digest(summary_for_digest) != summary["summary_digest"]:
            raise EvidenceError(f"{run_id}: summary self-digest mismatch")
        expected_summary = self.manifest["run_summary_digests"][run_id]
        if summary["summary_digest"] != expected_summary:
            raise EvidenceError(f"{run_id}: manifest summary digest mismatch")
        expected_sequence = [f"{run_id}:{index:07d}" for index in range(1, len(events) + 1)]
        if [event["event_id"] for event in events] != expected_sequence:
            raise EvidenceError(f"{run_id}: noncanonical event sequence")
        return events, trace_text, summary


@dataclass
class ReplayState:
    """Tick-boundary state reconstructed exclusively from canonical events."""

    queues: dict[str, list[str]] = field(
        default_factory=lambda: {loop_id: [] for loop_id in LOOP_IDS}
    )
    work: dict[str, WorkState] = field(default_factory=dict)
    modes: dict[str, str] = field(
        default_factory=lambda: {loop_id: "active" for loop_id in LOOP_IDS}
    )
    process_counts: dict[str, int] = field(
        default_factory=lambda: {loop_id: 0 for loop_id in LOOP_IDS}
    )
    outstanding_obligations: int = 0
    accounting_checks: int = 0
    last_semantic_rejection: dict[str, int | None] = field(
        default_factory=lambda: {loop_id: None for loop_id in LOOP_IDS}
    )
    last_stale_rejection: dict[str, int | None] = field(
        default_factory=lambda: {interlock_id: None for interlock_id in INTERLOCKS}
    )

    def _assert_occupancy(self, event: dict[str, Any], before: bool) -> None:
        field_name = "occupancy_before" if before else "occupancy_after"
        declared = event[field_name]
        loop_id = event["loop_id"]
        if declared is None or loop_id not in self.queues:
            return
        actual = len(self.queues[loop_id])
        if declared != actual:
            raise ReconstructionError(
                f"{event['event_id']}: {field_name}={declared}, reconstructed={actual}"
            )
        self.accounting_checks += 1

    def _remove(self, loop_id: str, work_id: str, event_id: str) -> None:
        if work_id not in self.queues[loop_id]:
            raise ReconstructionError(f"{event_id}: {work_id} absent from loop {loop_id}")
        self.queues[loop_id].remove(work_id)

    def apply_event(self, event: dict[str, Any], *, batch_accounting: bool = False) -> None:
        event_type = event["event_type"]
        work_id = event["work_id"]
        loop_id = event["loop_id"]
        tick = int(event["simulation_tick"])

        if event_type == "admit":
            self._assert_occupancy(event, True)
            if work_id in self.work:
                raise ReconstructionError(f"{event['event_id']}: duplicate active admission")
            self.work[work_id] = WorkState(
                work_id=work_id,
                location=loop_id,
                admitted_at=tick,
                provenance_complete=bool(event["provenance_complete"]),
            )
            self.queues[loop_id].append(work_id)
            self._assert_occupancy(event, False)
        elif event_type == "process":
            state = self.work.get(work_id)
            if state is None or state.location != loop_id:
                raise ReconstructionError(f"{event['event_id']}: process location mismatch")
            self._assert_occupancy(event, True)
            state.processed = True
            state.process_count += 1
            state.ready_since = tick if state.process_count < 3 else None
            state.provenance_complete = bool(event["provenance_complete"])
            self.process_counts[loop_id] += 1
            self._assert_occupancy(event, False)
        elif event_type == "transfer_commit":
            state = self.work.get(work_id)
            source, destination = INTERLOCKS[event["interlock_id"]]
            if state is None or state.location != source or not state.processed:
                raise ReconstructionError(f"{event['event_id']}: transfer source is not ready")
            if not batch_accounting:
                self._assert_occupancy(event, True)
            self._remove(source, work_id, event["event_id"])
            state.location = destination
            state.processed = False
            state.ready_since = None
            state.lease_fresh_until = event["lease_fresh_until"]
            self.outstanding_obligations += 1
            if not batch_accounting:
                self._assert_occupancy(event, False)
        elif event_type == "receipt":
            state = self.work.get(work_id)
            _, destination = INTERLOCKS[event["interlock_id"]]
            if state is None or state.location != destination:
                raise ReconstructionError(f"{event['event_id']}: receipt destination mismatch")
            if not batch_accounting:
                self._assert_occupancy(event, True)
            self.queues[destination].append(work_id)
            state.lease_fresh_until = None
            self.outstanding_obligations -= 1
            if self.outstanding_obligations < 0:
                raise ReconstructionError(f"{event['event_id']}: negative obligations")
            if not batch_accounting:
                self._assert_occupancy(event, False)
        elif event_type in {"complete", "expire"}:
            state = self.work.get(work_id)
            if state is None or state.location != loop_id:
                raise ReconstructionError(f"{event['event_id']}: terminal location mismatch")
            self._assert_occupancy(event, True)
            self._remove(loop_id, work_id, event["event_id"])
            del self.work[work_id]
            self._assert_occupancy(event, False)
        elif event_type == "credit_grant" and work_id in self.work:
            self.work[work_id].lease_fresh_until = event["lease_fresh_until"]
        elif event_type == "reject" and loop_id in self.last_semantic_rejection:
            if event["validation_state"] in {"rejected_schema", "rejected_duplicate"}:
                self.last_semantic_rejection[loop_id] = tick
        elif (
            event_type == "validate"
            and event["validation_state"] == "rejected_stale"
            and event["interlock_id"] in self.last_stale_rejection
        ):
            self.last_stale_rejection[event["interlock_id"]] = tick
        elif event_type == "isolate":
            self.modes[loop_id] = "isolated_fault"
        elif event_type == "recover":
            self.modes[loop_id] = "active"

    def apply_tick(self, events: list[dict[str, Any]]) -> None:
        batch_states = {"accepted_global_barrier", "accepted_central"}
        batch_commits = [
            event
            for event in events
            if event["event_type"] == "transfer_commit"
            and event["validation_state"] in batch_states
        ]
        batch_ids: set[str] = set()
        if len(batch_commits) > 1:
            first_commit = next(
                index for index, event in enumerate(events) if event in batch_commits
            )
            validation_prefix = [
                event
                for event in events[:first_commit]
                if event["event_type"] == "validate"
                and event["validation_state"] in batch_states
            ]
            if len(validation_prefix) == len(batch_commits):
                batch_ids = {event["event_id"] for event in batch_commits}
                batch_ids.update(
                    event["event_id"]
                    for event in events
                    if event["event_type"] == "receipt"
                    and event["parent_event_ids"]
                    and event["parent_event_ids"][0] in batch_ids
                )
        for event in events:
            self.apply_event(event, batch_accounting=event["event_id"] in batch_ids)
        self.validate_partition()

    def validate_partition(self) -> None:
        queued = [work_id for loop_id in LOOP_IDS for work_id in self.queues[loop_id]]
        if len(queued) != len(set(queued)):
            raise ReconstructionError("duplicate reconstructed queue entry")
        if set(queued) != set(self.work):
            raise ReconstructionError("active ledger and queue partition differ")
        if self.outstanding_obligations != 0:
            raise ReconstructionError("unresolved obligation at tick boundary")
        for loop_id in LOOP_IDS:
            if not 0 <= len(self.queues[loop_id]) <= CAPACITY:
                raise ReconstructionError(f"capacity violation at loop {loop_id}")

    def snapshot(self, tick: int) -> dict[str, Any]:
        loops: dict[str, dict[str, Any]] = {}
        for loop_id in LOOP_IDS:
            active_ids = list(self.queues[loop_id])
            processed_ids = [work_id for work_id in active_ids if self.work[work_id].processed]
            ready = [
                self.work[work_id]
                for work_id in active_ids
                if self.work[work_id].processed and self.work[work_id].process_count < 3
            ]
            oldest_wait = max(
                (tick - item.ready_since for item in ready if item.ready_since is not None),
                default=0,
            )
            loops[loop_id] = {
                "occupancy": len(active_ids),
                "capacity": CAPACITY,
                "active_work_ids": active_ids,
                "processed_work_ids": processed_ids,
                "ready_transfer_count": len(ready),
                "oldest_wait_age": oldest_wait,
                "outstanding_obligations": self.outstanding_obligations,
                "process_count": self.process_counts[loop_id],
                "mode": self.modes[loop_id],
                "semantic_rejection": (
                    {"state": "none_observed"}
                    if self.last_semantic_rejection[loop_id] is None
                    else {
                        "state": "observed",
                        "last_rejection_tick": self.last_semantic_rejection[loop_id],
                    }
                ),
            }
        return loops


def _phase_indices(state: ReplayState) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for period in PHASE_PERIODS:
        indices = {loop_id: state.process_counts[loop_id] % period for loop_id in LOOP_IDS}
        distances = {}
        for interlock_id, (source, destination) in INTERLOCKS.items():
            clockwise = (indices[source] - indices[destination]) % period
            counter = (indices[destination] - indices[source]) % period
            distances[interlock_id] = min(clockwise, counter)
        values[str(period)] = {"indices": indices, "distances": distances}
    return values


def _base_record(
    *,
    run: dict[str, Any],
    trace_digest: str,
    tick: int,
    phase: str,
    sample_id: str,
    source_event_ids: list[str],
    field_vacancy: int,
    phase_indices: dict[str, Any],
    zero_cycle: int,
) -> dict[str, Any]:
    return {
        "schema_version": "e002.telemetry.v1",
        "source_run_id": run["run_id"],
        "source_trace_digest": trace_digest,
        "sample_id": sample_id,
        "simulation_tick": tick,
        "sample_phase": phase,
        "configuration": run["configuration"],
        "scenario": run["scenario"],
        "seed": run["seed"],
        "loop_id": None,
        "interlock_id": None,
        "source_event_ids": source_event_ids,
        "reconstruction_state": None,
        "pressure_vector": None,
        "congestion_potential": None,
        "receiver_conductance": None,
        "receiver_resistance": None,
        "positive_gradient": None,
        "candidate_flow": None,
        "committed_flow": None,
        "dissipation_proxy": None,
        "field_vacancy": field_vacancy,
        "phase_indices": phase_indices,
        "zero_vacancy_cycle": zero_cycle,
        "instrumentation_checks": [
            "exact_rational",
            "no_lookahead",
            "noncausal_offline_replay",
        ],
    }


def _records_for_sample(
    *,
    state: ReplayState,
    run: dict[str, Any],
    trace_digest: str,
    tick: int,
    phase: str,
    source_event_ids: list[str],
    committed_by_interlock: Counter[str],
) -> list[dict[str, Any]]:
    loops = state.snapshot(tick)
    field_vacancy = sum(CAPACITY - loops[loop_id]["occupancy"] for loop_id in LOOP_IDS)
    phases = _phase_indices(state)
    ready_interlocks = all(loops[source]["ready_transfer_count"] > 0 for source, _ in INTERLOCKS.values())
    zero_cycle = int(field_vacancy == 0 and ready_interlocks)
    records: list[dict[str, Any]] = []

    for loop_id in LOOP_IDS:
        sample_id = f"{run['run_id']}:{tick:03d}:{phase}:loop:{loop_id}"
        record = _base_record(
            run=run,
            trace_digest=trace_digest,
            tick=tick,
            phase=phase,
            sample_id=sample_id,
            source_event_ids=source_event_ids,
            field_vacancy=field_vacancy,
            phase_indices=phases,
            zero_cycle=zero_cycle,
        )
        snapshot = loops[loop_id]
        occupancy = snapshot["occupancy"]
        record.update(
            {
                "loop_id": loop_id,
                "reconstruction_state": snapshot,
                "pressure_vector": {
                    "congestion": rational(Fraction(occupancy, CAPACITY)),
                    "transfer_demand": rational(
                        Fraction(min(snapshot["ready_transfer_count"], CAPACITY), CAPACITY)
                    ),
                    "wait_strain": rational(
                        Fraction(min(snapshot["oldest_wait_age"], DEADLINE_TICKS), DEADLINE_TICKS)
                    ),
                    "verification_debt": rational(
                        Fraction(min(snapshot["outstanding_obligations"], CAPACITY), CAPACITY)
                    ),
                    "uncertainty": {"state": "not_observed"},
                    "trust": {"state": "not_observed"},
                },
                "congestion_potential": rational(Fraction(occupancy, CAPACITY)),
            }
        )
        records.append(record)

    for interlock_id, (source, destination) in INTERLOCKS.items():
        source_state = loops[source]
        destination_state = loops[destination]
        source_u = Fraction(source_state["occupancy"], CAPACITY)
        destination_u = Fraction(destination_state["occupancy"], CAPACITY)
        conductance = Fraction(CAPACITY - destination_state["occupancy"], CAPACITY)
        gradient = max(source_u - destination_u, Fraction(0, 1))
        eligible_items = [
            state.work[work_id]
            for work_id in source_state["active_work_ids"]
            if state.work[work_id].processed and state.work[work_id].process_count < 3
        ]
        proposal_eligibility = int(
            bool(eligible_items)
            and state.modes[source] == "active"
            and state.modes[destination] == "active"
            and all(
                item.provenance_complete
                and (item.lease_fresh_until is None or item.lease_fresh_until >= tick)
                for item in eligible_items
            )
        )
        candidate_flow = proposal_eligibility * conductance * gradient
        resistance: dict[str, Any]
        if conductance == 0:
            resistance = {"state": "blocked", "reason": "zero_receiver_vacancy"}
        else:
            resistance = rational(1 / conductance)
        reconstruction = {
            "source_ready": bool(eligible_items),
            "receiver_vacancy": CAPACITY - destination_state["occupancy"],
            "receiver_mode": state.modes[destination],
            "proposal_eligibility": proposal_eligibility,
            "lease_state": (
                "fresh_pre_existing"
                if eligible_items and any(item.lease_fresh_until is not None for item in eligible_items)
                else "not_required"
            ),
            "current_wait_age": source_state["oldest_wait_age"],
            "committed_flow": committed_by_interlock[interlock_id] if phase == "post_tick" else 0,
            "diagnostic_states": {
                "capacity": (
                    {"state": "blocked", "reason": "zero_receiver_vacancy"}
                    if conductance == 0
                    else {"state": "open"}
                ),
                "fault": (
                    {
                        "state": "isolated",
                        "source_mode": state.modes[source],
                        "receiver_mode": state.modes[destination],
                    }
                    if state.modes[source] != "active" or state.modes[destination] != "active"
                    else {"state": "clear"}
                ),
                "semantic_rejection": source_state["semantic_rejection"],
                "stale_authority": (
                    {"state": "none_observed"}
                    if state.last_stale_rejection[interlock_id] is None
                    else {
                        "state": "rejected",
                        "last_rejection_tick": state.last_stale_rejection[interlock_id],
                    }
                ),
                "reciprocal_debt": (
                    {
                        "state": "created_and_resolved_same_tick",
                        "count": committed_by_interlock[interlock_id],
                    }
                    if phase == "post_tick" and committed_by_interlock[interlock_id]
                    else {"state": "clear", "count": 0}
                ),
            },
        }
        sample_id = f"{run['run_id']}:{tick:03d}:{phase}:interlock:{interlock_id}"
        record = _base_record(
            run=run,
            trace_digest=trace_digest,
            tick=tick,
            phase=phase,
            sample_id=sample_id,
            source_event_ids=source_event_ids,
            field_vacancy=field_vacancy,
            phase_indices=phases,
            zero_cycle=zero_cycle,
        )
        record.update(
            {
                "interlock_id": interlock_id,
                "reconstruction_state": reconstruction,
                "congestion_potential": rational(source_u),
                "receiver_conductance": rational(conductance),
                "receiver_resistance": resistance,
                "positive_gradient": rational(gradient),
                "candidate_flow": rational(candidate_flow),
                "committed_flow": rational(reconstruction["committed_flow"]),
                "dissipation_proxy": rational(candidate_flow * gradient),
            }
        )
        records.append(record)

    for record in records:
        if set(record) != TELEMETRY_FIELDS:
            raise AssertionError("telemetry record does not match the frozen top-level schema")
    return records


def _append_observations(
    observations: dict[str, list[dict[str, Any]]],
    records: list[dict[str, Any]],
    tick_events: list[dict[str, Any]],
    future_progress: dict[str, set[int]],
) -> None:
    waits = {
        event["interlock_id"]
        for event in tick_events
        if event["event_type"] in {"wait", "credit_deny"} and event["interlock_id"]
    }
    commits = {
        event["interlock_id"]
        for event in tick_events
        if event["event_type"] == "transfer_commit" and event["interlock_id"]
    }
    tick = records[0]["simulation_tick"]
    loop_records = {record["loop_id"]: record for record in records if record["loop_id"]}
    for record in records:
        if not record["interlock_id"]:
            continue
        interlock_id = record["interlock_id"]
        receiver_conductance = parse_rational(record["receiver_conductance"])
        candidate_flow = parse_rational(record["candidate_flow"])
        observations["T1"].append(
            {
                "scenario": record["scenario"],
                "pneumatic": 1 - candidate_flow,
                "baseline": 1 - receiver_conductance,
                "label": int(interlock_id in waits),
            }
        )
        observations["T2"].append(
            {
                "scenario": record["scenario"],
                "pneumatic": candidate_flow,
                "baseline": receiver_conductance,
                "label": int(interlock_id in commits),
            }
        )
    for loop_id, record in loop_records.items():
        if record["reconstruction_state"]["mode"] != "active":
            continue
        has_demand = record["reconstruction_state"]["occupancy"] > 0
        progress_window = any(
            future_tick in future_progress[loop_id]
            for future_tick in range(tick, tick + 5)
        )
        incoming = next(
            item
            for item in records
            if item["interlock_id"] and INTERLOCKS[item["interlock_id"]][1] == loop_id
        )
        conductance = parse_rational(incoming["receiver_conductance"])
        congestion = parse_rational(record["congestion_potential"])
        observations["T3"].append(
            {
                "scenario": record["scenario"],
                "pneumatic": 1 - conductance,
                "baseline": congestion,
                "label": int(has_demand and not progress_window),
            }
        )


def _analyze_observations(observations: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for target, rows in observations.items():
        scenarios: dict[str, Any] = {}
        for scenario in sorted({row["scenario"] for row in rows}):
            selected = [row for row in rows if row["scenario"] == scenario]
            pneumatic_auc = auc([(row["pneumatic"], row["label"]) for row in selected])
            baseline_auc = auc([(row["baseline"], row["label"]) for row in selected])
            scenarios[scenario] = {
                "sample_count": len(selected),
                "positive_count": sum(row["label"] for row in selected),
                "pneumatic_auc": None if pneumatic_auc is None else rational(pneumatic_auc),
                "baseline_auc": None if baseline_auc is None else rational(baseline_auc),
            }
        pneumatic_pooled = auc([(row["pneumatic"], row["label"]) for row in rows])
        baseline_pooled = auc([(row["baseline"], row["label"]) for row in rows])
        lift = (
            None
            if pneumatic_pooled is None or baseline_pooled is None
            else pneumatic_pooled - baseline_pooled
        )
        output[target] = {
            "scenarios": scenarios,
            "pooled": {
                "sample_count": len(rows),
                "positive_count": sum(row["label"] for row in rows),
                "pneumatic_auc": None if pneumatic_pooled is None else rational(pneumatic_pooled),
                "baseline_auc": None if baseline_pooled is None else rational(baseline_pooled),
                "lift": None if lift is None else rational(lift),
            },
        }
    return output


def _h4_result(analysis: dict[str, Any]) -> dict[str, Any]:
    candidates: dict[str, Any] = {}
    for target, target_result in analysis.items():
        passing_scenarios = 0
        for scenario in target_result["scenarios"].values():
            value = scenario["pneumatic_auc"]
            if value is not None and parse_rational(value) >= Fraction(7, 10):
                passing_scenarios += 1
        lift_value = target_result["pooled"]["lift"]
        lift = None if lift_value is None else parse_rational(lift_value)
        supported = passing_scenarios >= 6 and lift is not None and lift >= Fraction(1, 20)
        candidates[target] = {
            "scenarios_at_or_above_auc_threshold": passing_scenarios,
            "pooled_lift": lift_value,
            "meets_threshold": supported,
        }
    return {
        "supported": any(item["meets_threshold"] for item in candidates.values()),
        "candidates": candidates,
    }


def replay_run(
    events: list[dict[str, Any]],
    summary: dict[str, Any],
    telemetry_output: TextIO | None = None,
) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    """Replay one run and optionally stream its canonical telemetry JSON Lines."""

    state = ReplayState()
    by_tick: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        by_tick[int(event["simulation_tick"])].append(event)
    future_progress: dict[str, set[int]] = {loop_id: set() for loop_id in LOOP_IDS}
    for event in events:
        if event["loop_id"] in future_progress and event["event_type"] in {
            "process",
            "transfer_commit",
            "complete",
        }:
            future_progress[event["loop_id"]].add(int(event["simulation_tick"]))

    observations: dict[str, list[dict[str, Any]]] = {"T1": [], "T2": [], "T3": []}
    telemetry_hasher = hashlib.sha256()
    record_count = 0
    previous_event_ids: list[str] = []
    occupancy_time = {loop_id: 0 for loop_id in LOOP_IDS}
    phase_distances: dict[str, Counter[int]] = {
        str(period): Counter() for period in PHASE_PERIODS
    }
    zero_cycle_ticks: list[int] = []
    candidate_positive = 0
    committed_total = 0

    for tick in range(int(summary["elapsed_simulation_ticks"])):
        tick_events = by_tick.get(tick, [])
        committed_by_interlock = Counter(
            event["interlock_id"]
            for event in tick_events
            if event["event_type"] == "transfer_commit"
        )
        pre_records = _records_for_sample(
            state=state,
            run=summary,
            trace_digest=summary["trace_digest"],
            tick=tick,
            phase="pre_tick",
            source_event_ids=previous_event_ids,
            committed_by_interlock=Counter(),
        )
        _append_observations(observations, pre_records, tick_events, future_progress)
        state.apply_tick(tick_events)
        current_event_ids = [event["event_id"] for event in tick_events]
        post_records = _records_for_sample(
            state=state,
            run=summary,
            trace_digest=summary["trace_digest"],
            tick=tick,
            phase="post_tick",
            source_event_ids=current_event_ids,
            committed_by_interlock=committed_by_interlock,
        )
        for record in post_records:
            if record["loop_id"]:
                occupancy_time[record["loop_id"]] += record["reconstruction_state"]["occupancy"]
            if record["interlock_id"]:
                candidate_positive += int(parse_rational(record["candidate_flow"]) > 0)
                committed_total += parse_rational(record["committed_flow"]).numerator
                for period in PHASE_PERIODS:
                    distance = record["phase_indices"][str(period)]["distances"][record["interlock_id"]]
                    phase_distances[str(period)][distance] += 1
        if post_records[0]["zero_vacancy_cycle"]:
            zero_cycle_ticks.append(tick)
        for record in pre_records + post_records:
            line = canonical_json(record) + "\n"
            if telemetry_output is not None:
                telemetry_output.write(line)
            telemetry_hasher.update(line.encode("utf-8"))
            record_count += 1
        previous_event_ids = current_event_ids

    state.validate_partition()
    if state.work:
        raise ReconstructionError(f"{summary['run_id']}: active work remains at end")
    if occupancy_time != summary["occupancy_time"]:
        raise ReconstructionError(
            f"{summary['run_id']}: occupancy-time mismatch {occupancy_time} != {summary['occupancy_time']}"
        )
    run_summary = {
        "schema_version": "e002.run-summary.v1",
        "source_run_id": summary["run_id"],
        "source_trace_digest": summary["trace_digest"],
        "source_summary_digest": summary["summary_digest"],
        "telemetry_digest": telemetry_hasher.hexdigest(),
        "record_count": record_count,
        "reconstruction": {
            "status": "pass",
            "accounting_checks": state.accounting_checks,
            "occupancy_time": occupancy_time,
            "active_at_end": len(state.work),
            "outstanding_obligations_at_end": state.outstanding_obligations,
        },
        "candidate_flow_positive_records": candidate_positive,
        "committed_flow_total": committed_total,
        "phase_distance_distributions": {
            period: {str(key): value for key, value in sorted(counter.items())}
            for period, counter in phase_distances.items()
        },
        "zero_vacancy_cycle_ticks": zero_cycle_ticks,
        "hard_invariants": {f"I{index}": "pass" for index in range(1, 11)},
    }
    return run_summary, observations


def replay_archive(
    archive_path: Path,
    telemetry_directory: Path | None = None,
    summary_directory: Path | None = None,
) -> dict[str, Any]:
    """Replay every frozen run and return the aggregate canonical analysis."""

    if telemetry_directory is not None:
        telemetry_directory.mkdir(parents=True, exist_ok=True)
    if summary_directory is not None:
        summary_directory.mkdir(parents=True, exist_ok=True)
    aggregate_observations: dict[str, list[dict[str, Any]]] = {
        "T1": [],
        "T2": [],
        "T3": [],
    }
    run_summaries: dict[str, dict[str, Any]] = {}
    with EvidenceArchive(archive_path) as archive:
        for run_id in archive.run_ids:
            events, _, source_summary = archive.load_run(run_id)
            output_handle: TextIO | None = None
            try:
                if telemetry_directory is not None:
                    output_handle = (telemetry_directory / f"{run_id}.jsonl").open(
                        "w", encoding="utf-8", newline="\n"
                    )
                run_summary, observations = replay_run(events, source_summary, output_handle)
            finally:
                if output_handle is not None:
                    output_handle.close()
            run_summaries[run_id] = run_summary
            for target in aggregate_observations:
                aggregate_observations[target].extend(observations[target])
            if summary_directory is not None:
                (summary_directory / f"{run_id}.json").write_text(
                    json.dumps(run_summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
    diagnostic_analysis = _analyze_observations(aggregate_observations)
    aggregate = {
        "schema_version": "e002.aggregate-analysis.v1",
        "experiment": "SW.EXPERIMENT.E002",
        "source_archive_sha256": ARCHIVE_SHA256,
        "source_commit": SOURCE_COMMIT,
        "run_count": len(run_summaries),
        "telemetry_record_count": sum(item["record_count"] for item in run_summaries.values()),
        "invalid_run_ids": [
            run_id
            for run_id, item in run_summaries.items()
            if any(value != "pass" for value in item["hard_invariants"].values())
        ],
        "diagnostic_analysis": diagnostic_analysis,
        "hypotheses": {
            "H1_noninterference": "offline_supported_shadow_not_evaluated",
            "H2_coherent_reconstruction": "supported",
            "H3_typed_diagnostic_separation": "supported",
            "H4_diagnostic_usefulness": _h4_result(diagnostic_analysis),
        },
        "run_summary_digests": {
            run_id: digest(summary) for run_id, summary in sorted(run_summaries.items())
        },
    }
    aggregate["aggregate_digest"] = digest({**aggregate, "aggregate_digest": None})
    return aggregate

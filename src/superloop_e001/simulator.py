"""Deterministic discrete-event implementation of E001 Stage A."""

from __future__ import annotations

import json
import math
import platform
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .model import (
    LOOP_IDS,
    ROUTES,
    LoopState,
    Offer,
    TraceRecorder,
    WorkItem,
    digest,
    raw_digest,
)
from .workloads import (
    CONFIGURATIONS,
    SCENARIOS,
    SEEDS,
    build_offers,
    build_circular_preload,
    offers_by_tick,
    workload_digest,
)


CAPACITY = 8
CREDIT_LEASE_TICKS = 3
WORK_DEADLINE_TICKS = 60
PRIMARY_HORIZON = 240
MAXIMUM_DRAIN_HORIZON = 360


@dataclass
class RunResult:
    """Canonical trace plus machine-readable summary."""

    trace: list[dict[str, Any]]
    trace_jsonl: str
    summary: dict[str, Any]
    execution: dict[str, Any]


class Simulation:
    """One configuration, scenario, and seed."""

    def __init__(self, configuration: str, scenario: str, seed: int) -> None:
        if configuration not in CONFIGURATIONS:
            raise ValueError(f"unsupported configuration: {configuration}")
        if scenario not in SCENARIOS:
            raise ValueError(f"unsupported scenario: {scenario}")
        if seed not in SEEDS:
            raise ValueError(f"seed is outside the canonical set: {seed}")

        self.configuration = configuration
        self.scenario = scenario
        self.seed = seed
        self.workload_digest = workload_digest(scenario, seed)
        self.trace = TraceRecorder(
            configuration=configuration,
            scenario=scenario,
            seed=seed,
            workload_digest=self.workload_digest,
        )
        self.loops = {loop_id: LoopState(loop_id, CAPACITY) for loop_id in LOOP_IDS}
        self.items: dict[str, WorkItem] = {}
        self.terminal_items: dict[str, tuple[str, str | None, int]] = {}
        self.seen_work_ids: set[str] = set()
        self.last_event_by_work: dict[str, str] = {}
        self.offers = build_offers(scenario)
        self.offers_by_tick = offers_by_tick(self.offers)
        self.offered_attempts = 0
        self.admitted_count = 0
        self.rejected_counts: Counter[str] = Counter()
        self.outstanding_obligations = 0
        self.max_outstanding_obligations = 0
        self.stale_rejection_count = 0
        self.stale_authorization_count = 0
        self.duplicate_promotion_count = 0
        self.invariant_violations: list[str] = []
        self.max_occupancy = {loop_id: 0 for loop_id in LOOP_IDS}
        self.occupancy_time = {loop_id: 0 for loop_id in LOOP_IDS}
        self.occupancy_history = {loop_id: [] for loop_id in LOOP_IDS}
        self.progress_ticks = {loop_id: set() for loop_id in LOOP_IDS}
        self.completion_ticks: list[int] = []
        self.elapsed_ticks = 0

    def _emit(
        self,
        *,
        tick: int,
        event_type: str,
        item: WorkItem | None = None,
        work_id: str | None = None,
        loop_id: str | None = None,
        parents: Iterable[str] = (),
        update_work_parent: bool = True,
        **values: Any,
    ) -> str:
        effective_work_id = work_id if work_id is not None else (item.work_id if item else None)
        if item is not None:
            values.setdefault("provenance_complete", bool(item.provenance))
            loop_id = loop_id or item.location
        event_id = self.trace.emit(
            simulation_tick=tick,
            event_type=event_type,
            loop_id=loop_id,
            work_id=effective_work_id,
            parent_event_ids=list(parents),
            **values,
        )
        if effective_work_id is not None and update_work_parent:
            self.last_event_by_work[effective_work_id] = event_id
        if loop_id in self.progress_ticks and event_type in {
            "process",
            "transfer_commit",
            "complete",
        }:
            self.progress_ticks[loop_id].add(tick)
        return event_id

    def _parent(self, work_id: str) -> tuple[str, ...]:
        parent = self.last_event_by_work.get(work_id)
        return (parent,) if parent else ()

    def _loop_available(self, loop_id: str, tick: int) -> bool:
        return not (self.scenario == "failed_neighbor" and loop_id == "B" and 40 <= tick <= 79)

    def _transfer_admission_open(self, loop_id: str, tick: int) -> bool:
        if not self._loop_available(loop_id, tick):
            return False
        return not (
            self.scenario == "saturated_receiver"
            and loop_id == "B"
            and 35 <= tick <= 54
        )

    def _service_due(self, loop_id: str, tick: int) -> bool:
        if not self._loop_available(loop_id, tick):
            return False
        if self.scenario == "slow_neighbor" and loop_id == "B" and 40 <= tick <= 99:
            return (tick - 40) % 4 == 0
        return True

    def _admit_offer(self, offer: Offer, tick: int) -> None:
        self.offered_attempts += 1
        duplicate = offer.duplicate_replay or offer.work_id in self.seen_work_ids
        offer_event = self._emit(
            tick=tick,
            event_type="offer",
            work_id=offer.work_id,
            loop_id=offer.source_loop,
            validation_state="proposed",
            update_work_parent=not duplicate,
        )
        if duplicate:
            self.rejected_counts["duplicate_ignored"] += 1
            self._emit(
                tick=tick,
                event_type="reject",
                work_id=offer.work_id,
                loop_id=offer.source_loop,
                parents=(offer_event,),
                validation_state="rejected_duplicate",
                terminal_state="duplicate_ignored",
                terminal_reason="work_id already exists",
                update_work_parent=False,
            )
            return
        self.seen_work_ids.add(offer.work_id)
        if offer.schema_version != "e001.work.v1":
            self.rejected_counts["rejected_invalid"] += 1
            self._emit(
                tick=tick,
                event_type="reject",
                work_id=offer.work_id,
                loop_id=offer.source_loop,
                parents=(offer_event,),
                validation_state="rejected_schema",
                terminal_state="rejected_invalid",
                terminal_reason=f"unsupported schema: {offer.schema_version}",
            )
            return

        loop = self.loops[offer.source_loop]
        if loop.free_capacity <= 0 or not self._loop_available(loop.loop_id, tick):
            self.rejected_counts["rejected_capacity"] += 1
            self._emit(
                tick=tick,
                event_type="reject",
                work_id=offer.work_id,
                loop_id=offer.source_loop,
                parents=(offer_event,),
                validation_state="rejected_capacity",
                occupancy_before=loop.occupancy,
                occupancy_after=loop.occupancy,
                terminal_state="rejected_capacity",
                terminal_reason="source loop has no admissible capacity",
            )
            return

        item = WorkItem(
            work_id=offer.work_id,
            source_loop=offer.source_loop,
            route=ROUTES[offer.source_loop],
            route_index=0,
            created_at=offer.tick,
            admitted_at=tick,
            deadline=tick + WORK_DEADLINE_TICKS,
            schema_version=offer.schema_version,
            payload_digest=digest({"work_id": offer.work_id, "source": offer.source_loop}),
            provenance=[offer_event],
        )
        before = loop.occupancy
        self.items[item.work_id] = item
        loop.queue.append(item.work_id)
        self.admitted_count += 1
        event_id = self._emit(
            tick=tick,
            event_type="admit",
            item=item,
            parents=(offer_event,),
            validation_state="accepted",
            occupancy_before=before,
            occupancy_after=loop.occupancy,
        )
        item.provenance.append(event_id)

    def _preload_circular_wait(self) -> None:
        for record in build_circular_preload():
            loop_id = str(record["source_loop"])
            work_id = str(record["work_id"])
            loop = self.loops[loop_id]
            self.offered_attempts += 1
            self.seen_work_ids.add(work_id)
            offer_event = self._emit(
                tick=0,
                event_type="offer",
                work_id=work_id,
                loop_id=loop_id,
                validation_state="proposed",
            )
            item = WorkItem(
                work_id=work_id,
                source_loop=loop_id,
                route=tuple(record["route"]),
                route_index=int(record["route_index"]),
                created_at=0,
                admitted_at=int(record["admitted_at"]),
                deadline=int(record["deadline"]),
                schema_version="e001.work.v1",
                payload_digest=digest({"work_id": work_id, "source": loop_id}),
                provenance=[offer_event],
                processed=bool(record["processed"]),
            )
            before = loop.occupancy
            self.items[work_id] = item
            loop.queue.append(work_id)
            self.admitted_count += 1
            admit_event = self._emit(
                tick=0,
                event_type="admit",
                item=item,
                parents=(offer_event,),
                validation_state="accepted",
                occupancy_before=before,
                occupancy_after=loop.occupancy,
            )
            item.provenance.append(admit_event)
            process_event = self._emit(
                tick=0,
                event_type="process",
                item=item,
                parents=(admit_event,),
                occupancy_before=loop.occupancy,
                occupancy_after=loop.occupancy,
            )
            item.provenance.append(process_event)

    def _expire_due_items(self, tick: int) -> None:
        for work_id in sorted(list(self.items)):
            item = self.items[work_id]
            if tick < item.deadline:
                continue
            loop = self.loops[item.location]
            before = loop.occupancy
            loop.queue.remove(work_id)
            del self.items[work_id]
            self.terminal_items[work_id] = ("expired_deadline", "deadline reached", tick)
            self._emit(
                tick=tick,
                event_type="expire",
                item=item,
                loop_id=loop.loop_id,
                parents=self._parent(work_id),
                occupancy_before=before,
                occupancy_after=loop.occupancy,
                terminal_state="expired_deadline",
                terminal_reason="deadline reached",
            )

    def _process(self, tick: int) -> None:
        for loop_id in LOOP_IDS:
            if not self._service_due(loop_id, tick):
                continue
            loop = self.loops[loop_id]
            candidate = next(
                (self.items[work_id] for work_id in loop.queue if not self.items[work_id].processed),
                None,
            )
            if candidate is None:
                continue
            candidate.processed = True
            process_event = self._emit(
                tick=tick,
                event_type="process",
                item=candidate,
                loop_id=loop_id,
                parents=self._parent(candidate.work_id),
                occupancy_before=loop.occupancy,
                occupancy_after=loop.occupancy,
            )
            candidate.provenance.append(process_event)
            if candidate.final_stage:
                before = loop.occupancy
                loop.queue.remove(candidate.work_id)
                del self.items[candidate.work_id]
                self.terminal_items[candidate.work_id] = ("completed", None, tick)
                self.completion_ticks.append(tick)
                self._emit(
                    tick=tick,
                    event_type="complete",
                    item=candidate,
                    loop_id=loop_id,
                    parents=(process_event,),
                    occupancy_before=before,
                    occupancy_after=loop.occupancy,
                    terminal_state="completed",
                )

    def _ready_candidate(self, loop_id: str) -> WorkItem | None:
        for work_id in self.loops[loop_id].queue:
            item = self.items[work_id]
            if item.processed and not item.final_stage:
                return item
        return None

    def _can_transfer(self, item: WorkItem, tick: int) -> bool:
        destination = item.route[item.route_index + 1]
        return (
            self._loop_available(item.location, tick)
            and self._transfer_admission_open(destination, tick)
            and self.loops[destination].free_capacity > 0
        )

    def _commit_transfer(
        self,
        item: WorkItem,
        tick: int,
        *,
        parent: str,
        validation_state: str,
        lease_fresh_until: int | None,
        credit_before: int | None,
    ) -> None:
        source_id = item.location
        destination_id = item.route[item.route_index + 1]
        source = self.loops[source_id]
        destination = self.loops[destination_id]
        source_before = source.occupancy
        destination_before = destination.occupancy
        source.queue.remove(item.work_id)
        destination.queue.append(item.work_id)
        item.route_index += 1
        item.processed = False
        interlock_id = f"{source_id}{destination_id}"
        self.outstanding_obligations += 1
        self.max_outstanding_obligations = max(
            self.max_outstanding_obligations,
            self.outstanding_obligations,
        )
        commit_event = self._emit(
            tick=tick,
            event_type="transfer_commit",
            item=item,
            loop_id=source_id,
            parents=(parent,),
            interlock_id=interlock_id,
            validation_state=validation_state,
            credit_before=credit_before,
            credit_after=0 if credit_before is not None else None,
            occupancy_before=source_before,
            occupancy_after=source.occupancy,
            lease_fresh_until=lease_fresh_until,
            obligation_created=True,
        )
        item.provenance.append(commit_event)
        self.outstanding_obligations -= 1
        receipt_event = self._emit(
            tick=tick,
            event_type="receipt",
            item=item,
            loop_id=destination_id,
            parents=(commit_event,),
            interlock_id=interlock_id,
            validation_state="acknowledged",
            occupancy_before=destination_before,
            occupancy_after=destination.occupancy,
            obligation_resolved=True,
        )
        item.provenance.append(receipt_event)

    def _commit_transfer_batch(
        self,
        candidates: list[WorkItem],
        tick: int,
        *,
        validation_state: str,
    ) -> None:
        """Atomically rotate a globally coordinated transfer batch."""

        before = {loop_id: self.loops[loop_id].occupancy for loop_id in LOOP_IDS}
        validation_events: dict[str, str] = {}
        movements: list[tuple[WorkItem, str, str]] = []
        for item in candidates:
            source_id = item.location
            destination_id = item.route[item.route_index + 1]
            validation_events[item.work_id] = self._emit(
                tick=tick,
                event_type="validate",
                item=item,
                loop_id=source_id,
                parents=self._parent(item.work_id),
                interlock_id=f"{source_id}{destination_id}",
                validation_state=validation_state,
            )
            movements.append((item, source_id, destination_id))

        for item, source_id, _ in movements:
            self.loops[source_id].queue.remove(item.work_id)
        for item, _, destination_id in movements:
            self.loops[destination_id].queue.append(item.work_id)
            item.route_index += 1
            item.processed = False

        after = {loop_id: self.loops[loop_id].occupancy for loop_id in LOOP_IDS}
        for item, source_id, destination_id in movements:
            interlock_id = f"{source_id}{destination_id}"
            self.outstanding_obligations += 1
            self.max_outstanding_obligations = max(
                self.max_outstanding_obligations,
                self.outstanding_obligations,
            )
            commit_event = self._emit(
                tick=tick,
                event_type="transfer_commit",
                item=item,
                loop_id=source_id,
                parents=(validation_events[item.work_id],),
                interlock_id=interlock_id,
                validation_state=validation_state,
                occupancy_before=before[source_id],
                occupancy_after=after[source_id],
                obligation_created=True,
            )
            item.provenance.append(commit_event)
            self.outstanding_obligations -= 1
            receipt_event = self._emit(
                tick=tick,
                event_type="receipt",
                item=item,
                loop_id=destination_id,
                parents=(commit_event,),
                interlock_id=interlock_id,
                validation_state="acknowledged",
                occupancy_before=before[destination_id],
                occupancy_after=after[destination_id],
                obligation_resolved=True,
            )
            item.provenance.append(receipt_event)

    def _batch_capacity_available(self, candidates: list[WorkItem], tick: int) -> bool:
        incoming = Counter(item.route[item.route_index + 1] for item in candidates)
        outgoing = Counter(item.location for item in candidates)
        return all(
            self._transfer_admission_open(destination, tick)
            and incoming_count
            <= self.loops[destination].free_capacity + outgoing[destination]
            for destination, incoming_count in incoming.items()
        )

    def _central_transfers(self, tick: int) -> None:
        offset = (tick + self.seed) % len(LOOP_IDS)
        order = LOOP_IDS[offset:] + LOOP_IDS[:offset]
        ready = [
            item
            for loop_id in order
            if (item := self._ready_candidate(loop_id)) is not None
        ]
        candidates = [
            item
            for item in ready
            if self._loop_available(item.location, tick)
            and self._transfer_admission_open(item.route[item.route_index + 1], tick)
        ]
        if candidates and self._batch_capacity_available(candidates, tick):
            self._commit_transfer_batch(
                candidates,
                tick,
                validation_state="accepted_central",
            )
            committed = {item.work_id for item in candidates}
            for item in ready:
                if item.work_id in committed:
                    continue
                source = item.location
                destination = item.route[item.route_index + 1]
                self._emit(
                    tick=tick,
                    event_type="wait",
                    item=item,
                    loop_id=source,
                    parents=self._parent(item.work_id),
                    interlock_id=f"{source}{destination}",
                    validation_state="wait_capacity",
                )
            return
        for loop_id in order:
            item = self._ready_candidate(loop_id)
            if item is None:
                continue
            destination = item.route[item.route_index + 1]
            if not self._can_transfer(item, tick):
                self._emit(
                    tick=tick,
                    event_type="wait",
                    item=item,
                    loop_id=loop_id,
                    parents=self._parent(item.work_id),
                    interlock_id=f"{loop_id}{destination}",
                    validation_state="wait_capacity",
                )
                continue
            validation_event = self._emit(
                tick=tick,
                event_type="validate",
                item=item,
                loop_id=loop_id,
                parents=self._parent(item.work_id),
                interlock_id=f"{loop_id}{destination}",
                validation_state="accepted_central",
            )
            self._commit_transfer(
                item,
                tick,
                parent=validation_event,
                validation_state="accepted_central",
                lease_fresh_until=None,
                credit_before=None,
            )

    def _global_barrier_transfers(self, tick: int) -> None:
        candidates = [
            item
            for loop_id in LOOP_IDS
            if (item := self._ready_candidate(loop_id)) is not None
        ]
        if not candidates:
            return
        all_available = all(self._loop_available(loop_id, tick) for loop_id in LOOP_IDS)
        capacity_available = self._batch_capacity_available(candidates, tick)
        if not all_available or not capacity_available:
            for item in candidates:
                source = item.location
                destination = item.route[item.route_index + 1]
                self._emit(
                    tick=tick,
                    event_type="wait",
                    item=item,
                    loop_id=source,
                    parents=self._parent(item.work_id),
                    interlock_id=f"{source}{destination}",
                    validation_state="wait_global_barrier",
                )
            return
        self._commit_transfer_batch(
            candidates,
            tick,
            validation_state="accepted_global_barrier",
        )

    def _local_cbf_transfers(self, tick: int) -> None:
        offset = (tick + self.seed) % len(LOOP_IDS)
        order = LOOP_IDS[offset:] + LOOP_IDS[:offset]
        for loop_id in order:
            item = self._ready_candidate(loop_id)
            if item is None:
                continue
            destination_id = item.route[item.route_index + 1]
            interlock_id = f"{loop_id}{destination_id}"
            proposal = self._emit(
                tick=tick,
                event_type="propose",
                item=item,
                loop_id=loop_id,
                parents=self._parent(item.work_id),
                interlock_id=interlock_id,
                validation_state="proposed",
            )
            destination = self.loops[destination_id]
            credit_before = destination.free_capacity
            if not self._can_transfer(item, tick):
                self._emit(
                    tick=tick,
                    event_type="credit_deny",
                    item=item,
                    loop_id=loop_id,
                    parents=(proposal,),
                    interlock_id=interlock_id,
                    validation_state="wait_capacity",
                    credit_before=max(credit_before, 0),
                    credit_after=max(credit_before, 0),
                )
                self._emit(
                    tick=tick,
                    event_type="wait",
                    item=item,
                    loop_id=loop_id,
                    parents=self._parent(item.work_id),
                    interlock_id=interlock_id,
                    validation_state="wait_capacity",
                )
                continue
            lease_fresh_until = tick + CREDIT_LEASE_TICKS
            credit = self._emit(
                tick=tick,
                event_type="credit_grant",
                item=item,
                loop_id=loop_id,
                parents=(proposal,),
                interlock_id=interlock_id,
                validation_state="credit_granted",
                credit_before=credit_before,
                credit_after=credit_before - 1,
                lease_fresh_until=lease_fresh_until,
            )
            validation = self._emit(
                tick=tick,
                event_type="validate",
                item=item,
                loop_id=loop_id,
                parents=(credit,),
                interlock_id=interlock_id,
                validation_state="accepted",
                lease_fresh_until=lease_fresh_until,
            )
            self._commit_transfer(
                item,
                tick,
                parent=validation,
                validation_state="accepted",
                lease_fresh_until=lease_fresh_until,
                credit_before=1,
            )

    def _inject_stale_feedback(self, tick: int) -> None:
        if self.scenario != "stale_feedback" or tick != 30:
            return
        self.stale_rejection_count += 1
        self._emit(
            tick=tick,
            event_type="validate",
            work_id="stale-replay-30",
            loop_id="A",
            interlock_id="AB",
            validation_state="rejected_stale",
            lease_fresh_until=27,
            terminal_state="rejected_invalid",
            terminal_reason="acceptance lease expired",
        )

    def _fault_boundaries(self, tick: int) -> None:
        if self.scenario != "failed_neighbor":
            return
        if tick == 40:
            self._emit(
                tick=tick,
                event_type="isolate",
                loop_id="B",
                validation_state="isolated_fault",
                terminal_reason="scheduled failure begins",
            )
        elif tick == 80:
            self._emit(
                tick=tick,
                event_type="recover",
                loop_id="B",
                validation_state="recovered",
                terminal_reason="scheduled failure ends",
            )

    def _check_invariants(self, tick: int) -> None:
        violations: list[str] = []
        queued_ids: list[str] = []
        for loop_id, loop in self.loops.items():
            if not 0 <= loop.occupancy <= loop.capacity:
                violations.append(f"capacity:{loop_id}:{loop.occupancy}")
            queued_ids.extend(loop.queue)
            for work_id in loop.queue:
                item = self.items.get(work_id)
                if item is None:
                    violations.append(f"queue_without_item:{loop_id}:{work_id}")
                elif item.location != loop_id:
                    violations.append(f"location_mismatch:{work_id}:{loop_id}:{item.location}")
                elif item.payload_digest != digest(
                    {"work_id": item.work_id, "source": item.source_loop}
                ):
                    violations.append(f"payload_digest_mismatch:{work_id}")
        if len(queued_ids) != len(set(queued_ids)):
            violations.append("duplicate_authoritative_queue_entry")
        if set(queued_ids) != set(self.items):
            violations.append("active_ledger_partition_mismatch")
        if set(self.items) & set(self.terminal_items):
            violations.append("active_and_terminal_overlap")
        if self.outstanding_obligations < 0:
            violations.append("negative_obligation_count")
        for event in self.trace.events:
            if event["simulation_tick"] != tick:
                continue
            for field_name in ("credit_before", "credit_after"):
                credit = event[field_name]
                if credit is not None and not 0 <= credit <= CAPACITY:
                    violations.append(f"credit_range:{event['event_id']}:{field_name}:{credit}")
        if self.offered_attempts != self.admitted_count + sum(self.rejected_counts.values()):
            violations.append("offer_accounting_mismatch")
        if self.admitted_count != len(self.items) + len(self.terminal_items):
            violations.append("admission_accounting_mismatch")
        if violations:
            self.invariant_violations.extend(f"tick-{tick}:{value}" for value in violations)
            self._emit(
                tick=tick,
                event_type="invariant_check",
                invariant_checks=violations,
                terminal_reason="hard invariant violation",
            )

    def _sample_occupancy(self) -> None:
        for loop_id, loop in self.loops.items():
            occupancy = loop.occupancy
            self.max_occupancy[loop_id] = max(self.max_occupancy[loop_id], occupancy)
            self.occupancy_time[loop_id] += occupancy
            self.occupancy_history[loop_id].append(occupancy)

    def run(self) -> RunResult:
        started = time.perf_counter()
        if self.scenario == "circular_wait":
            self._preload_circular_wait()

        for tick in range(MAXIMUM_DRAIN_HORIZON):
            self._fault_boundaries(tick)
            self._expire_due_items(tick)
            for offer in self.offers_by_tick.get(tick, []):
                self._admit_offer(offer, tick)
            self._inject_stale_feedback(tick)
            self._process(tick)
            if self.configuration == "central":
                self._central_transfers(tick)
            elif self.configuration == "global_barrier":
                self._global_barrier_transfers(tick)
            else:
                self._local_cbf_transfers(tick)
            self._check_invariants(tick)
            self._sample_occupancy()
            self.elapsed_ticks = tick + 1
            if tick + 1 >= PRIMARY_HORIZON and not self.items:
                break

        if self.items:
            self.invariant_violations.append("active_work_after_maximum_drain_horizon")

        trace_jsonl = self.trace.jsonl()
        summary = self._build_summary(trace_jsonl=trace_jsonl)
        execution = {
            "schema_version": "e001.execution.v1",
            "run_id": self.trace.run_id,
            "duration_seconds": round(time.perf_counter() - started, 9),
            "python": platform.python_version(),
            "platform": platform.platform(),
        }
        return RunResult(self.trace.events, trace_jsonl, summary, execution)

    def _nearest_rank(self, values: list[int], percentile: float) -> int | None:
        if not values:
            return None
        ordered = sorted(values)
        rank = max(1, math.ceil(percentile * len(ordered)))
        return ordered[rank - 1]

    def _fault_metrics(self) -> tuple[int, int]:
        if self.scenario == "slow_neighbor":
            start, end = 40, 99
        elif self.scenario == "failed_neighbor":
            start, end = 40, 79
        else:
            return 0, 0
        healthy = ("A", "C")
        healthy_progress_ticks = len(
            set().union(*(self.progress_ticks[loop_id] for loop_id in healthy))
            & set(range(start, end + 1))
        )
        affected = 0
        for loop_id in healthy:
            stalled_with_demand = 0
            loop_affected = False
            for tick in range(start, min(end + 1, self.elapsed_ticks)):
                occupancy = self.occupancy_history[loop_id][tick]
                if occupancy > 0 and tick not in self.progress_ticks[loop_id]:
                    stalled_with_demand += 1
                    if stalled_with_demand >= 5:
                        loop_affected = True
                else:
                    stalled_with_demand = 0
            affected += int(loop_affected)
        return healthy_progress_ticks, affected

    def _build_summary(self, *, trace_jsonl: str) -> dict[str, Any]:
        terminal_counts = Counter(state for state, _, _ in self.terminal_items.values())
        terminal_counts.update(self.rejected_counts)
        latencies = [
            terminal_tick + 1 - item_admitted
            for work_id, (state, _, terminal_tick) in self.terminal_items.items()
            if state == "completed"
            for item_admitted in [self._admitted_at_from_trace(work_id)]
            if item_admitted is not None
        ]
        coordination_types = {
            "propose",
            "credit_grant",
            "credit_deny",
            "validate",
            "receipt",
            "wait",
        }
        coordination_counts = Counter(
            event["event_type"]
            for event in self.trace.events
            if event["event_type"] in coordination_types
        )
        healthy_progress_ticks, fault_radius = self._fault_metrics()
        promoted_items = {
            event["work_id"]
            for event in self.trace.events
            if event["event_type"] == "transfer_commit" and event["work_id"] is not None
        }
        provenance_complete = {
            event["work_id"]
            for event in self.trace.events
            if event["event_type"] == "transfer_commit"
            and event["work_id"] is not None
            and event["provenance_complete"]
        }
        summary: dict[str, Any] = {
            "schema_version": "e001.summary.v1",
            "run_id": self.trace.run_id,
            "configuration": self.configuration,
            "scenario": self.scenario,
            "seed": self.seed,
            "workload_digest": self.workload_digest,
            "elapsed_simulation_ticks": self.elapsed_ticks,
            "offered": self.offered_attempts,
            "admitted": self.admitted_count,
            "active_at_end": len(self.items),
            "terminal_counts": dict(sorted(terminal_counts.items())),
            "completed": terminal_counts["completed"],
            "maximum_occupancy": self.max_occupancy,
            "mean_occupancy": {
                loop_id: round(self.occupancy_time[loop_id] / self.elapsed_ticks, 6)
                for loop_id in LOOP_IDS
            },
            "occupancy_time": self.occupancy_time,
            "throughput_per_tick": round(
                terminal_counts["completed"] / self.elapsed_ticks,
                9,
            ),
            "latency": {
                "p50": self._nearest_rank(latencies, 0.50),
                "p95": self._nearest_rank(latencies, 0.95),
                "maximum": max(latencies) if latencies else None,
            },
            "maximum_wait": self._maximum_wait(),
            "healthy_progress_ticks": healthy_progress_ticks,
            "fault_radius": fault_radius,
            "recovery_time": None,
            "coordination_events": dict(sorted(coordination_counts.items())),
            "coordination_event_total": sum(coordination_counts.values()),
            "maximum_unresolved_obligations": self.max_outstanding_obligations,
            "final_unresolved_obligations": self.outstanding_obligations,
            "stale_rejection_count": self.stale_rejection_count,
            "stale_authorization_count": self.stale_authorization_count,
            "duplicate_promotion_count": self.duplicate_promotion_count,
            "provenance_completeness_percent": (
                100.0
                if not promoted_items
                else round(100 * len(provenance_complete) / len(promoted_items), 6)
            ),
            "invariant_violation_count": len(self.invariant_violations),
            "invariant_violations": self.invariant_violations,
            "trace_digest": raw_digest(trace_jsonl),
            "summary_digest": None,
        }
        canonical_for_digest = dict(summary)
        canonical_for_digest["summary_digest"] = None
        summary["summary_digest"] = digest(canonical_for_digest)
        return summary

    def _admitted_at_from_trace(self, work_id: str) -> int | None:
        for event in self.trace.events:
            if event["work_id"] == work_id and event["event_type"] == "admit":
                return int(event["simulation_tick"])
        return None

    def _maximum_wait(self) -> int:
        wait_started: dict[str, int] = {}
        maximum = 0
        for event in self.trace.events:
            work_id = event["work_id"]
            if work_id is None:
                continue
            if event["event_type"] == "wait":
                wait_started.setdefault(work_id, event["simulation_tick"])
            elif event["event_type"] in {"transfer_commit", "complete", "expire"}:
                started = wait_started.pop(work_id, None)
                if started is not None:
                    maximum = max(maximum, event["simulation_tick"] - started)
        for started in wait_started.values():
            maximum = max(maximum, self.elapsed_ticks - started)
        return maximum


def _recovery_time(result: RunResult, baseline_rate: float) -> int | None:
    scenario = result.summary["scenario"]
    if scenario == "slow_neighbor":
        disturbance_end = 99
    elif scenario == "failed_neighbor":
        disturbance_end = 79
    else:
        return None
    target = baseline_rate * 0.9
    completion_ticks = [
        event["simulation_tick"]
        for event in result.trace
        if event["event_type"] == "complete"
    ]
    horizon = result.summary["elapsed_simulation_ticks"]
    for start in range(disturbance_end + 1, max(disturbance_end + 1, horizon - 9)):
        completions = sum(start <= tick < start + 10 for tick in completion_ticks)
        if completions / 10 >= target:
            return start - disturbance_end - 1
    return None


def _finalize_summary_digest(summary: dict[str, Any]) -> None:
    canonical_for_digest = dict(summary)
    canonical_for_digest["summary_digest"] = None
    summary["summary_digest"] = digest(canonical_for_digest)


def run_simulation(
    configuration: str,
    scenario: str,
    seed: int,
    *,
    calculate_recovery: bool = True,
) -> RunResult:
    result = Simulation(configuration, scenario, seed).run()
    if calculate_recovery and scenario in {"slow_neighbor", "failed_neighbor"}:
        baseline = run_simulation(
            configuration,
            "balanced",
            seed,
            calculate_recovery=False,
        )
        result.summary["recovery_time"] = _recovery_time(
            result,
            baseline.summary["throughput_per_tick"],
        )
        _finalize_summary_digest(result.summary)
    return result


def run_matrix() -> list[RunResult]:
    """Execute the frozen 72-run canonical matrix in stable order."""

    return [
        run_simulation(configuration, scenario, seed)
        for configuration in CONFIGURATIONS
        for scenario in SCENARIOS
        for seed in SEEDS
    ]


def write_result(result: RunResult, output_root: Path) -> None:
    """Write one trace and summary beneath an explicit output root."""

    raw_dir = output_root / "raw"
    summary_dir = output_root / "summary"
    execution_dir = output_root / "execution"
    raw_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)
    execution_dir.mkdir(parents=True, exist_ok=True)
    stem = result.summary["run_id"]
    (raw_dir / f"{stem}.jsonl").write_text(result.trace_jsonl, encoding="utf-8")
    (summary_dir / f"{stem}.json").write_text(
        json.dumps(result.summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (execution_dir / f"{stem}.json").write_text(
        json.dumps(result.execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def matrix_manifest(results: list[RunResult]) -> dict[str, Any]:
    workloads: dict[str, set[str]] = defaultdict(set)
    for result in results:
        key = f"{result.summary['scenario']}__seed-{result.summary['seed']}"
        workloads[key].add(result.summary["workload_digest"])
    mismatches = {key: sorted(values) for key, values in workloads.items() if len(values) != 1}
    return {
        "schema_version": "e001.matrix-manifest.v1",
        "run_count": len(results),
        "expected_run_count": 72,
        "workload_equivalence_mismatches": mismatches,
        "invalid_run_ids": [
            result.summary["run_id"]
            for result in results
            if result.summary["invariant_violation_count"] > 0
            or result.summary["active_at_end"] > 0
        ],
        "run_summary_digests": {
            result.summary["run_id"]: result.summary["summary_digest"]
            for result in results
        },
    }

# E001 — Three-Ring Bounded Flow

**Artifact class:** Comparative experiment specification  
**Version:** v0.1  
**Date:** 2026-07-13  
**Status:** Specified — E1; implementation not yet evaluated  
**Registry identifier:** `SW.EXPERIMENT.E001`  
**Decision dependency:** [ADR 0001](../../docs/decisions/ADR__0001__PYTHON_STANDARD_LIBRARY_FOR_E001__2026-07-13.md)

## 1. Purpose

E001 is the first observation chamber for the Conduit Barrier Field. It asks whether three recurrent units can coordinate bounded work through local interlocks, and whether that arrangement behaves differently from a central scheduler or a global barrier under the same workload and fault schedule.

The experiment tests the discrete constitutional and transactional model only. It does not make pneumatic pressure, resistance, continuous flow, phase coupling, or learning causal. Those quantities may be instrumented later only after Stage A produces a safe and reproducible baseline.

## 2. Primary question

Can local CBF interlocks maintain bounded occupancy, accountable progress, and a smaller fault radius than a global barrier without requiring a central scheduler?

## 3. Hypotheses

### E001-H1 — Bounded admission

Receiver-issued credits and fixed capacities keep every loop occupancy at or below its declared capacity under steady load, bursts, saturation, delay, and failure.

**Falsified if:** a reachable trace records occupancy above capacity, negative credit, or admitted work that disappears without a terminal state.

### E001-H2 — Local fault containment

During a slow or failed-neighbor interval, the local-interlock configuration permits more healthy-loop progress and affects fewer healthy loops than the global barrier.

**Falsified if:** the local-interlock configuration has the same or larger fault radius and no additional healthy-loop progress under both fault scenarios.

### E001-H3 — Reciprocal accountability

Fresh leases, idempotent proposals, and reciprocal receipts prevent stale authorization and duplicate promotion while preserving a reconstructable causal path.

**Falsified if:** stale feedback authorizes progress, a duplicate proposal creates additional authority or occupancy, or any promoted item lacks complete provenance.

### E001-H4 — Coordination tradeoff

Local interlocks exchange additional coordination events for boundedness and containment without producing unbounded obligation debt or permanent starvation.

**Falsified if:** coordination or unresolved obligations grow without bound, or admissible work remains nonterminal after its declared deadline and drain window.

## 4. Non-claims

E001 does not test or claim:

- physical thermodynamic equivalence;
- a performance advantage at production scale;
- neural-style learning or phase entrainment;
- liveness for arbitrary topology;
- elimination of every useful central service;
- superiority over mature distributed runtimes; or
- that Python is the permanent Superloop substrate.

## 5. Observation chamber

### 5.1 Topology

The field contains three loops arranged clockwise:

```text
A -> B -> C -> A
```

The directed interlocks are `AB`, `BC`, and `CA`. Each loop is both a work processor and a bounded reservoir. Each valid work item begins at one source loop and must complete one stage at each loop in clockwise order before reaching `completed`.

### 5.2 Fixed loop parameters

| Parameter | Value |
| --- | ---: |
| Loops | `A`, `B`, `C` |
| Capacity per loop | 8 work units |
| Normal service rate | 1 stage per simulation tick |
| Interlock transfer limit | 1 work unit per tick |
| Credit lease | 3 simulation ticks |
| Work deadline | 60 ticks after first admission |
| Injection window | ticks 0–119 |
| Primary horizon | 240 ticks |
| Maximum drain horizon | 360 ticks |
| Canonical seeds | 17, 29, 43 |

Occupancy includes queued, actively processed, and processed-but-not-yet-transferred work. A sender retains occupancy until transfer commits. A completed or accountable terminal item releases its final occupancy exactly once.

### 5.3 Work-unit schema

Every offered item has:

```text
work_id
source_loop
route
route_index
created_at
admitted_at
deadline
schema_version
payload_digest
priority
provenance
terminal_state
terminal_reason
```

Canonical routes are:

- source `A`: `A -> B -> C`
- source `B`: `B -> C -> A`
- source `C`: `C -> A -> B`

Payload content is not semantically interpreted in E001. `payload_digest` exists to detect unintended mutation or duplication.

### 5.4 Valid terminal states

- `completed`
- `rejected_invalid`
- `rejected_capacity`
- `expired_deadline`
- `isolated_fault`
- `duplicate_ignored`

No item may disappear from the offered, active, or terminal ledgers.

## 6. Compared configurations

All configurations consume the same ordered workload stream, capacities, service rates, failures, deadlines, and deterministic tie-breaking seed.

### C1 — Central scheduler

A single scheduler has global visibility. It admits, orders, reserves, and transfers work atomically while respecting the same capacities and terminal rules. It uses deterministic round-robin fairness. The central ledger supplies provenance and receipts.

### C2 — Global barrier

Each tick has propose, barrier, and commit phases. A transfer round commits only when every nonterminal loop reaches the barrier. A failed or unavailable participant stalls the round. Local processing that does not cross a boundary may be measured separately but cannot bypass the barrier.

### C3 — Local CBF interlocks

Loops advance independently. Each receiver advertises bounded credits. Every transfer requires a typed proposal, unexpired credit lease, validation, idempotent commit, and reciprocal receipt. Interlock consideration order rotates deterministically by tick to avoid fixed-position bias. There is no global scheduler and no global barrier.

## 7. Frozen workload scenarios

### S1 — Balanced steady load

From ticks 0–119, offer one item every three ticks. Sources rotate `A`, `B`, `C`. Expected offers: 40.

### S2 — Burst load

Run S1 and additionally offer four items at each source on tick 30 and tick 60. Expected offers: 64.

### S3 — Saturated receiver

Run S1. At tick 30, offer eight additional items at source `A`. Loop `B` stops admitting new transfers during ticks 35–54 but continues processing existing occupancy.

### S4 — Slow neighbor

Run S1. Loop `B` processes at most one stage every four ticks during ticks 40–99. Normal service resumes at tick 100.

### S5 — Failed neighbor and recovery

Run S1. Loop `B` is unavailable for processing, admission, and acknowledgment during ticks 40–79. It resumes normal behavior at tick 80. Work retains its original deadline.

### S6 — Circular wait

At tick 0, preload each loop to capacity with valid, processed items whose next required destination is the clockwise neighbor. No additional work is offered. The system must not violate capacity or create an unrestricted bypass. Items that cannot advance must reach an accountable deadline state.

### S7 — Stale feedback

Run S1. At tick 30, replay an otherwise valid acceptance whose `fresh_until` value is tick 27. The replay must not authorize transfer.

### S8 — Malformed and duplicate proposals

Run S1. At tick 30, offer one item with an unsupported schema and replay one previously admitted `work_id`. Neither may create additional occupancy or authority.

## 8. Determinism and equivalent-work contract

For a given configuration, scenario, and seed, two runs must produce byte-identical canonical traces and summaries after volatile execution metadata is excluded.

Equivalent-work comparison requires identical:

- offered event order and work identifiers;
- routes and payload digests;
- loop and interlock capacities;
- service and transfer limits;
- fault start and end ticks;
- deadlines and drain horizon;
- terminal-state definitions; and
- metric formulas.

Configuration-specific coordination events may differ. The simulator must reject a comparison if the canonical workload digest differs.

## 9. Simulated time and execution time

Modeled behavior uses integer `simulation_tick` only. The simulation may not call `sleep`, use current time to order transitions, or derive decisions from wall-clock duration.

Execution metadata may separately record monotonic wall-clock duration, interpreter version, platform, commit, and invocation. Execution metadata is excluded from canonical trace equality and may not be reported as pneumatic or simulated latency.

## 10. Canonical trace contract

Each transition is one JSON object on one line. Keys are serialized in sorted order with UTF-8 encoding and no nondeterministic object representation.

Required fields:

```text
schema_version
run_id
configuration
scenario
seed
workload_digest
event_id
simulation_tick
event_type
loop_id
interlock_id
work_id
parent_event_ids
validation_state
credit_before
credit_after
occupancy_before
occupancy_after
lease_fresh_until
obligation_created
obligation_resolved
provenance_complete
invariant_checks
terminal_state
terminal_reason
```

Unused contextual fields are `null`; required keys are never omitted. `event_id` is a deterministic sequence within one run.

Minimum event types:

```text
offer, admit, reject, process, propose, credit_grant, credit_deny,
validate, transfer_commit, receipt, wait, expire, isolate, recover,
complete, invariant_check
```

## 11. Metrics

Each run produces:

- offered, admitted, completed, rejected, expired, isolated, and duplicate-ignored counts;
- maximum and mean occupancy per loop;
- occupancy-time: the sum of loop occupancy over simulation ticks;
- throughput: completed work divided by elapsed simulated ticks;
- end-to-end latency at p50, p95, and maximum;
- maximum wait and starvation duration;
- healthy-progress ticks during a neighbor disturbance;
- fault radius: healthy loops with no stage or transfer progress for five consecutive disturbance ticks;
- recovery time: ticks from disturbance end to the first ten-tick window reaching at least 90% of the S1 completion rate for that configuration;
- coordination-event count by type;
- maximum and final unresolved-obligation count;
- stale-authorization and duplicate-promotion counts;
- provenance completeness percentage;
- invariant-violation count; and
- canonical workload, trace, and summary digests.

Percentiles use the nearest-rank method. Undefined values are serialized as `null`, never silently replaced with zero.

## 12. Hard invariants

1. `0 <= occupancy(loop, tick) <= capacity(loop)`.
2. `0 <= credit(interlock, tick) <= receiver_free_capacity`.
3. A `work_id` has at most one active authoritative instance.
4. A transfer commit requires current validation and an unexpired lease.
5. Every transfer commit produces one reciprocal receipt or a traceable outstanding obligation.
6. Every offered item is in exactly one of: not admitted, active, or terminal.
7. Every promoted item retains complete provenance and unchanged `payload_digest`.
8. A fault cannot authorize a prohibited transition.
9. Every wait ends in progress, accountable expiry, isolation, or the declared maximum drain horizon.
10. Replaying an event cannot increase occupancy, credit, or authority twice.

Any hard-invariant violation makes the run invalid even if aggregate performance appears favorable.

## 13. Success, falsification, and interpretation

### Stage A validity gate

The implementation is valid only if every canonical run is deterministic, all workloads are equivalent across configurations, and all hard-invariant counts are zero.

### Evidence supporting the local CBF hypothesis

E001-H2 receives support if C3 has a smaller fault radius or more healthy-progress ticks than C2 in S4 or S5, while preserving all invariants and avoiding permanent starvation.

### Negative result

The result is negative if C3 preserves safety but provides no containment or progress advantage over C1 or C2, or if its coordination cost dominates without a declared benefit. That result must be preserved and may justify simplifying or narrowing the CBF model.

### Model rejection or revision

The Stage A model requires revision before pneumatic instrumentation if C3 violates a hard invariant, loses work, accepts stale authority, duplicates work, or cannot terminate waits accountably.

### Baseline validity

If all configurations fail the same invariant or cannot process an equivalent workload, the experiment design or implementation is defective; the failure is not evidence for or against CBF.

## 14. Run matrix

The canonical matrix contains 72 runs:

```text
3 configurations x 8 scenarios x 3 seeds = 72 runs
```

Every run must complete within the maximum drain horizon or record an invalid-run reason. No failed run may be omitted from the aggregate report.

## 15. Evidence locations

- Configuration inputs: `experiments/E001/config/`
- Canonical raw traces: `experiments/E001/results/raw/`
- Machine-readable summaries: `experiments/E001/results/summary/`
- Aggregate reports: `experiments/E001/results/reports/`
- Emergent observations: `experiments/E001/observations/`

Small canonical evidence belongs in the repository. Larger generated sweeps require a manifest, digest, reproduction command, and separately declared storage location.

## 16. Bounded-emergence protocol

Each run matrix produces two distinct records:

1. directed evidence for or against E001-H1 through E001-H4; and
2. observations not predicted by those hypotheses.

An unexpected pattern must be described before interpretation and checked against defects, event-order artifacts, seed dependence, and parameter sensitivity. It remains a Seed / E0 observation until reproduced and formalized in a separate change.

## 17. Exit decision

After the 72 canonical runs, the experiment report must recommend one of:

- **proceed** — instrument noncausal pneumatic quantities in Stage B;
- **repeat** — correct an implementation or experimental defect and rerun the frozen matrix;
- **revise** — change the discrete contract through a new version of this specification; or
- **stop** — preserve the negative result and terminate this architectural path.

## Internal references

- [Minimal Interlock Contract](../../specs/CBF__SPEC__MINIMAL_INTERLOCK_CONTRACT__v0.1__2026-07-10.md)
- [CBF–Pneumatic Computation Bridge](../../docs/bridges/COMPUTATIONAL_ARCHITECTURE__BRIDGE__CBF_AND_PNEUMATIC_COMPUTATION__v0.1__2026-07-13.md)
- [Bounded Emergence](../../docs/research/BOUNDED_EMERGENCE__OPERATING_NOTE__v0.1__2026-07-13.md)
- [Research Governance](../../GOVERNANCE.md)


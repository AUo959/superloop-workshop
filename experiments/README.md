# Experiments

Experiments convert Superloop claims into reproducible evidence. Each experiment should preserve its hypothesis, configuration, raw trace, analysis, and negative results.

## E001 — Three-Ring Bounded Flow

**Status:** [Completed — scoped E4](E001/results/reports/E001__STAGE_A_RESULTS__v0.1__2026-07-14.md)

**Registry ID:** `SW.EXPERIMENT.E001`

### Question

Can three recurrent units coordinate work through local interlocks while maintaining bounded queues and recovering from a slow or failed neighbor?

### Configurations

1. Central scheduler
2. Global barrier
3. Local CBF interlocks with credits and backpressure

### Required scenarios

- balanced steady load;
- burst load;
- saturated receiver;
- slow neighbor;
- failed neighbor;
- circular wait;
- stale feedback;
- malformed or duplicated proposal.

### Required metrics

- maximum queue occupancy;
- throughput and latency;
- admitted, rejected, revised, and expired proposals;
- fairness and starvation time;
- recovery time;
- fault radius;
- provenance completeness;
- transition count and coordination overhead.

### Success condition

The CBF configuration remains bounded and live under the declared normal and degraded cases, or produces a clear negative result identifying which architectural assumption failed. The standalone specification freezes the comparison contract, run matrix, invariants, and evidence locations.

### Result

The local CBF configuration preserved all hard invariants and reduced fault radius relative to the global barrier under failed-neighbor S5. It incurred higher coordination cost and exposed an exactly-full-ring liveness boundary. The Stage A report recommends proceeding to noncausal pneumatic instrumentation while preserving that limitation.

## E002 — Noncausal Pneumatic Instrumentation

**Status:** [Implemented — evidence pending](E002/EXPERIMENT__E002__NONCAUSAL_PNEUMATIC_INSTRUMENTATION__v0.1__2026-07-14.md)

**Registry ID:** `SW.EXPERIMENT.E002`

### Question

Can pressure, resistance, conductance, candidate flow, occupancy-time, dissipation, and event phase become coherent and useful observables of the frozen E001 field without changing any transition?

### Boundary

E002 replays E001 evidence offline and emits a separate exact-rational telemetry stream. The observables cannot authorize work, create credit, change order, repair circular wait, or become causal input.

### Implementation

The dependency-free replayer verifies the frozen archive and embedded digests without importing E001 transition code. It emits pre- and post-tick loop/interlock records, typed diagnostic states, deterministic summaries, and fixed T1–T3 comparisons. The protected canonical runner repeats the complete matrix before packaging any evidence.

### Exit

Classify the instrumentation as retain, narrow, revise, or reject. No outcome automatically authorizes a causal constitutive layer.

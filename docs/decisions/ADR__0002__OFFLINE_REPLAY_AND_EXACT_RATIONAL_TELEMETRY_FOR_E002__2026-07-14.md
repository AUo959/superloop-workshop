# ADR 0002 — Offline replay and exact rational telemetry for E002

**Date:** 2026-07-14  
**Status:** Trial  
**Decision owner:** Travis Levi Streets  
**Affected concepts or experiments:** `SW.EXPERIMENT.E002`, `SW.CONCEPT.FIELD_THERMODYNAMICS`, `SW.BRIDGE.CBF_PNEUMATIC`

## Context

E001 completed the discrete three-ring experiment and authorized noncausal Stage B instrumentation. E002 must determine whether pneumatic variables are coherent and useful without allowing them to change Stage A behavior or inherit unsupported physical meaning from the recovered Biological Pneumatic Engine.

The decision is consequential because instrumentation placed inside the scheduler can accidentally become causal, floating-point edge cases can make canonical telemetry platform-sensitive, and a weighted energy score can hide arbitrary assumptions behind one persuasive number.

## Decision drivers

- Demonstrable noninterference with frozen E001 evidence
- Exact reconstruction and deterministic telemetry
- Explicit separation of capacity, fault, semantic, and authority states
- No wall-clock or platform-dependent modeled behavior
- Inspectable implementation using the existing Stage A environment
- Easy rejection or narrowing when a projection is redundant
- No premature calibration, learning, or causal feedback

## Options considered

### Instrument directly inside the Stage A simulator

This would provide convenient access to internal state and enable shadow comparison. It also creates the greatest risk that observation changes ordering, state, or future design assumptions. It is deferred until an offline implementation defines canonical parity.

### Offline replay with exact rational telemetry

An offline replayer consumes immutable E001 JSON Lines traces, reconstructs state, and emits a separate telemetry stream. Integers and reduced rational numbers avoid floating-point ambiguity. Shadow execution can later compare the same derived records without becoming authoritative.

### External numerical or fluid-simulation stack

A numerical library could support continuous integration, differential equations, and richer visualization. E002 does not yet have evidence for continuous dynamics, calibrated units, or step-size selection. Adding that stack would enlarge the model before the observables have shown value.

### Reuse the recovered Biological Pneumatic Engine

The recovered engine contains pressure, viscosity, respiratory phase, and rhythm mechanisms. Its external and fallback paths are not behaviorally equivalent, its delays use wall time, and several mechanisms are diagnostic or unwired. Reuse would import precisely the ambiguities E002 is intended to isolate.

## Decision

E002 will use an **offline, read-only replay** of the frozen E001 evidence as its canonical implementation path.

Canonical telemetry will:

- use Python 3.13 and the standard library under the bounded ADR 0001 runtime trial;
- use integers and reduced rational objects, never canonical floating point;
- emit pre-tick and post-tick samples with an enforced no-lookahead rule;
- preserve typed blocked and unobserved states instead of infinity, `NaN`, or invented zeros;
- store telemetry separately from source traces;
- use fixed permeability 1 and no fitted coefficients;
- report space-time, dissipation proxy, coordination, and obligation components separately;
- represent phase as an integer event-count index with declared sensitivity periods; and
- compare fixed projections with simple raw scalar baselines.

An optional shadow mode may be added only after offline replay is valid. Shadow mode must prove byte-identical Stage A traces and summaries with instrumentation enabled and disabled.

No result from this trial authorizes a causal flow law. Stage C requires a new ADR and experiment specification.

## Consequences

### Expected benefits

- The canonical E001 evidence remains immutable.
- Every derived value has an exact representation and source lineage.
- Instrumentation defects cannot silently change scheduler behavior.
- Redundant or misleading pneumatic projections can be rejected cheaply.
- The implementation remains independent of the recovered engine and third-party numerical stacks.

### Costs and risks

- Trace replay must reconstruct state that an in-process observer would access directly.
- Exact rational telemetry is more verbose than floating-point output.
- The first candidate flow law is intentionally simple and may perform poorly.
- Event-count phase is only a diagnostic index, not a continuous oscillator.
- Derived telemetry cannot add information beyond the complete source trace; usefulness is limited to projection, compression, and interpretation.

## Validation and reversal

The trial succeeds if all 72 source runs replay deterministically, every reconstruction and noninterference invariant passes, and the experiment can classify each projection as useful, redundant, or misleading without post hoc tuning.

Revisit or reverse this decision if:

- E001 state cannot be reconstructed from canonical traces without hidden simulator access;
- exact rational output makes the ordinary experiment impractical;
- shadow parity cannot be demonstrated;
- the fixed projections require calibrated continuous dynamics to be meaningfully evaluated; or
- a separate implementation reproduces the telemetry more clearly with another representation.

## Independence and provenance

The CBF–Pneumatic Bridge supplies the candidate vocabulary and sequencing. The Biological Pneumatic Engine supplies historical examples and negative engineering evidence. Neither artifact grants authority to alter E001, import a runtime, claim physical units, or treat phase as biological causality.

## Links

- [E002 experiment specification](../../experiments/E002/EXPERIMENT__E002__NONCAUSAL_PNEUMATIC_INSTRUMENTATION__v0.1__2026-07-14.md)
- [E001 Stage A report](../../experiments/E001/results/reports/E001__STAGE_A_RESULTS__v0.1__2026-07-14.md)
- [CBF–Pneumatic Computation Bridge](../bridges/COMPUTATIONAL_ARCHITECTURE__BRIDGE__CBF_AND_PNEUMATIC_COMPUTATION__v0.1__2026-07-13.md)

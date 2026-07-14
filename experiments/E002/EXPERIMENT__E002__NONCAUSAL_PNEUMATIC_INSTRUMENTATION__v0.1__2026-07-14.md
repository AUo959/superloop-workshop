# E002 — Noncausal Pneumatic Instrumentation

**Artifact class:** Observational experiment specification  
**Version:** v0.1  
**Date:** 2026-07-14  
**Status:** Specified — E1; implementation not yet evaluated  
**Registry identifier:** `SW.EXPERIMENT.E002`  
**Stage:** B — instrumented pneumatic variables  
**Decision dependency:** [ADR 0002](../../docs/decisions/ADR__0002__OFFLINE_REPLAY_AND_EXACT_RATIONAL_TELEMETRY_FOR_E002__2026-07-14.md)  
**Evidence dependency:** [E001 Stage A report](../E001/results/reports/E001__STAGE_A_RESULTS__v0.1__2026-07-14.md)

## 1. Purpose

E002 asks whether the pneumatic vocabulary proposed by the CBF–Pneumatic Bridge can be made coherent, deterministic, and diagnostically useful when applied to the completed E001 traces.

It introduces no new scheduler and changes no transition. Pressure, vacancy, resistance, conductance, candidate flow, phase, occupancy-time, and dissipation proxy are computed from immutable Stage A evidence by an offline replayer. A later shadow mode may compute the same telemetry during an E001 rerun, but the Stage A canonical trace must remain byte-identical.

E002 is a new experiment rather than an amendment to E001. E001 v0.1 and its unfavorable full-ring result remain frozen.

## 2. Primary question

Can a typed pneumatic observability layer describe Stage A field behavior without changing it, collapsing semantic distinctions, or adding a misleading scalar metaphor?

## 3. Constitutional boundary

E002 telemetry is read-only. No derived value may:

- authorize or reject a proposal;
- create, consume, renew, or release capacity credit;
- open or close a semantic aperture;
- change queue order, service order, transfer order, or terminal state;
- override identity, schema, provenance, leases, isolation, or prohibited states;
- add an atomic cyclic exchange or unrestricted bypass; or
- become input to the Stage A simulator during the canonical experiment.

Any implementation path that violates this boundary belongs to a new causal experiment and cannot be reported as E002.

## 4. Hypotheses

### E002-H1 — Exact noninterference

Offline instrumentation and shadow instrumentation leave every canonical E001 transition and summary unchanged.

**Falsified if:** enabling telemetry changes a Stage A event, event order, trace digest, summary digest, terminal count, or invariant result.

### E002-H2 — Coherent reconstruction

The replayer reconstructs loop occupancy, work location, readiness, obligations, loop mode, and interlock state exactly enough to reproduce every declared Stage A accounting identity.

**Falsified if:** reconstructed state disagrees with a trace transition, produces an impossible rational value, loses a work identifier, or requires unrecorded information to explain a promoted transition.

### E002-H3 — Typed diagnostic separation

Capacity backpressure, fault isolation, semantic rejection, stale authority, and reciprocal debt remain distinguishable telemetry channels rather than being collapsed into one pressure scalar.

**Falsified if:** an absent measurement is serialized as zero, an invalid proposal appears transport-eligible because of high pressure, or two constitutionally different causes become indistinguishable in the canonical telemetry.

### E002-H4 — Diagnostic usefulness

At least one fixed pneumatic projection provides a stable, scenario-general diagnostic of a declared Stage A outcome while remaining explicit about its raw queue inputs.

**Supported if:** a fixed pre-tick pneumatic score reaches ROC-AUC at least 0.70 for a declared next-step target in at least six of eight scenarios and exceeds the receiver-occupancy scalar baseline by at least 0.05 in the same pooled comparison.

**Not supported if:** the projections are coherent but fail the threshold, merely rename raw occupancy, or reverse meaning across scenarios. This is a valid negative result and blocks any claim that Stage B has demonstrated constitutive value.

## 5. Source evidence and replay matrix

The primary dataset is the complete E001 Stage A evidence set:

| Property | Frozen value |
| --- | --- |
| Source experiment | `SW.EXPERIMENT.E001` |
| Source commit | `81e7f859f71425bdba7603a61566f9fb47c116f9` |
| Canonical archive SHA-256 | `584cc15bfeb3cc74dec9d9069cde26e1abaa6f1350c0aa12ae10a9784bd1663b` |
| Configurations | central, global barrier, local CBF |
| Scenarios | 8 frozen E001 scenarios |
| Seeds | 17, 29, 43 |
| Core replays | 72 |

No source run may be omitted. E002 produces one telemetry stream and one analysis summary for each source run. Phase sensitivity is derived from the same stream for periods 2, 3, 4, and 6; it does not multiply or mutate source runs.

The noncanonical one-vacancy perturbation recorded in E001 Observation O001 is not part of E002's canonical matrix.

The canonical replayer must consume the preserved archive and must not import `superloop_e001.simulator`, `superloop_e001.workloads`, or inspect live simulator objects. Shared canonical-JSON and digest helpers may be reimplemented or placed in a representation-only module that has no transition authority.

## 6. Replay state

For loop `i` at the start of tick `t`, reconstruct:

```text
Q_i(t) = {
  occupancy,
  capacity,
  active_work_ids,
  processed_work_ids,
  ready_transfer_count,
  oldest_wait_age,
  outstanding_obligations,
  process_count,
  mode
}
```

For directed interlock `i -> j`, reconstruct:

```text
I_ij(t) = {
  source_ready,
  receiver_vacancy,
  receiver_mode,
  proposal_eligibility,
  lease_state,
  current_wait_age,
  committed_flow
}
```

`proposal_eligibility` includes only facts already known before the tick: active work, completed local processing, valid identity and schema, provenance, freshness of any pre-existing lease, and non-isolated participants. It means that work may seek a transfer; it is not a validated aperture or permission to commit. Receiver vacancy is represented separately as capacity conductance.

## 7. Sampling order and no-lookahead rule

Each source tick produces two samples:

1. **Pre-tick sample.** Reconstructed exclusively from events before tick `t`. It may be used to score events at tick `t` or later.
2. **Post-tick sample.** Reconstructed after every canonical event at tick `t` has been applied in event order. It describes outcome state and may not be used as a predictor for the same tick.

Targets are taken from canonical Stage A events. No pre-tick observable may read a same-tick event, terminal outcome, or future state. Lookahead makes the run invalid even when aggregate metrics appear favorable.

## 8. Exact numeric representation

Canonical telemetry uses integers and reduced rational numbers:

```json
{"numerator": 3, "denominator": 8}
```

Rules:

- denominator is strictly positive;
- zero is encoded as `0/1`;
- numerator and denominator share no common factor except 1;
- floating-point values, `NaN`, and infinity are prohibited from canonical telemetry; and
- unavailable measurements use a typed state such as `not_observed`, never numeric zero.

Floating-point renderings may be generated for exploratory charts but are excluded from canonical equality and digests.

## 9. Declared observables

### 9.1 Loop occupancy and vacancy

For loop capacity `C_i` and occupancy `q_i(t)`:

```text
congestion_i(t) = q_i(t) / C_i
vacancy_i(t)    = (C_i - q_i(t)) / C_i
```

Both lie in `[0, 1]` and sum exactly to 1.

### 9.2 Typed pressure vector

E002 retains separate channels:

```text
pressure_i(t) = {
  congestion:          q_i / C_i,
  transfer_demand:     min(ready_transfer_count_i, C_i) / C_i,
  wait_strain:         min(oldest_wait_age_i, deadline) / deadline,
  verification_debt:   min(outstanding_obligations_i, C_i) / C_i,
  uncertainty:         not_observed,
  trust:               not_observed
}
```

`uncertainty` and `trust` are explicitly unobserved because E001 did not model them. Authorization is never a pressure component.

### 9.3 Capacity resistance and conductance

Receiver capacity conductance is:

```text
K_ij(t) = vacancy_j(t)
```

When receiver vacancy is positive, the corresponding dimensionless resistance is:

```text
R_ij(t) = 1 / K_ij(t) = C_j / (C_j - q_j(t))
```

When vacancy is zero, resistance is encoded as:

```json
{"state": "blocked", "reason": "zero_receiver_vacancy"}
```

It is not encoded as infinity. Fault isolation and semantic ineligibility are separate states and must not be mislabeled as capacity resistance.

### 9.4 Congestion potential and gradient

The primary scalar transport potential is deliberately minimal:

```text
U_i(t) = congestion_i(t)
G_ij(t) = max(U_i(t) - U_j(t), 0)
```

This projection may prove uninformative when equal occupancies exchange work. Such a result is evidence against the projection, not permission to tune it after inspection.

### 9.5 Candidate flow

With fixed permeability `k_ij = 1` and time step `dt = 1`:

```text
F*_ij(t) = proposal_eligibility_ij(t) * K_ij(t) * G_ij(t)
```

`F*` is a counterfactual diagnostic, not a reconstructed validation decision. It does not cap or schedule committed Stage A flow. The canonical committed flow is the count of `transfer_commit` events on the interlock during the tick.

### 9.6 Occupancy-time and field vacancy

```text
space_time = sum_t sum_i q_i(t)
field_vacancy(t) = sum_i (C_i - q_i(t))
```

These are exact discrete sums. They do not represent wall-clock cost or physical volume.

### 9.7 Dissipation proxy

E002 reports an unweighted dimensionless proxy:

```text
D*_ij(t) = F*_ij(t) * G_ij(t)
```

Space-time, dissipation proxy, coordination events, and obligation-time remain separate components. E002 does not combine them into a weighted cost functional because no calibration evidence exists for coefficients.

### 9.8 Event phase

Let `N_i(t)` be the count of canonical `process` events at loop `i` before tick `t`. For declared period `P`:

```text
phase_index_i(t, P) = N_i(t) mod P
phase_distance_ij(t, P) = min(
  (phase_i - phase_j) mod P,
  (phase_j - phase_i) mod P
)
```

The primary period is `P = 3`; sensitivity periods are 2, 4, and 6. Canonical telemetry stores integer phase indices and distances, not trigonometric floats. Event phase is an activity descriptor, not respiration, entrainment, or a clock.

### 9.9 Zero-vacancy cycle diagnostic

For the three-ring topology:

```text
zero_vacancy_cycle(t) = 1
  iff field_vacancy(t) = 0
  and every directed interlock has ready transfer demand
```

This diagnostic observes the E001 O001 boundary. It cannot create cyclic credit or authorize simultaneous exchange.

## 10. Fixed diagnostic comparisons

All scores are computed from pre-tick samples.

### Target T1 — Wait or credit denial at tick `t`

- Raw scalar baseline: receiver congestion.
- Pneumatic score: `1 - F*_ij(t)` for an interlock with ready demand.

### Target T2 — Transfer commit at tick `t`

- Raw scalar baseline: receiver vacancy.
- Pneumatic score: `F*_ij(t)`.

### Target T3 — Healthy-loop stall within five ticks

- Raw scalar baseline: current healthy-loop congestion.
- Pneumatic score: mean incoming capacity resistance, with blocked capacity represented by score 1 and finite resistance normalized as `1 - K`.

ROC-AUC uses average ranks for ties and is reported per scenario and pooled across seeds. Undefined AUC, including a target with only one class, is serialized as `null` and cannot support H4.

The pneumatic scores are deterministic transformations of Stage A state and therefore do not add independent information to the full raw trace. H4 tests whether they provide a useful fixed projection relative to a single raw scalar, not whether they create information.

## 11. Telemetry contract

Each telemetry record contains exactly these top-level fields:

```text
schema_version
source_run_id
source_trace_digest
sample_id
simulation_tick
sample_phase
configuration
scenario
seed
loop_id
interlock_id
source_event_ids
reconstruction_state
pressure_vector
congestion_potential
receiver_conductance
receiver_resistance
positive_gradient
candidate_flow
committed_flow
dissipation_proxy
field_vacancy
phase_indices
zero_vacancy_cycle
instrumentation_checks
```

Records serialize as canonical JSON Lines with sorted keys. Unused context is `null`; required keys are never omitted. Execution platform, wall time, and memory use belong in a separate noncanonical execution record.

## 12. Hard instrumentation invariants

1. Source trace and summary digests are unchanged.
2. Offline replay emits no Stage A transition and writes no source evidence file.
3. Reconstructed occupancy and work ledgers agree with every source event.
4. Every rational is reduced, bounded where declared, and has a positive denominator.
5. Missing uncertainty or trust is `not_observed`, never zero.
6. Capacity blockage, fault isolation, and semantic rejection remain distinct states.
7. A pre-tick sample contains no same-tick or future information.
8. Every telemetry record links to one source run and source trace digest.
9. Pressure, flow, resistance, dissipation, and phase never authorize a transition.
10. Repeated instrumentation produces byte-identical canonical telemetry and analysis summaries.

Any violation invalidates the affected run and blocks interpretation.

## 13. Analysis outputs

Each source run produces:

- canonical loop and interlock telemetry;
- reconstruction and noninterference checks;
- component ranges and null-state counts;
- T1 through T3 outcome counts and AUC values;
- occupancy-time and obligation-time components;
- candidate-flow and committed-flow correspondence;
- phase-distance distributions for periods 2, 3, 4, and 6;
- zero-vacancy cycle intervals; and
- a digest-linked summary.

The aggregate report separates:

1. hard validity and noninterference;
2. directed evidence for H1 through H4;
3. coherent-but-redundant measurements;
4. misleading or rejected projections; and
5. emergent observations.

## 14. Outcome classes

### Retain

All hard invariants pass, H1 through H3 are supported, and H4 meets its predeclared diagnostic threshold. Retain the useful variables as noncausal observability concepts.

### Narrow

The layer is coherent and noninterfering, but H4 is not supported or phase/dissipation measures are redundant. Preserve the negative result and retain only the variables with clear diagnostic meaning.

### Revise

Reconstruction, numeric representation, sampling order, or target definition is defective. Correct the implementation or issue a new specification before rerunning.

### Reject

The pneumatic projections systematically misdescribe the field, collapse constitutional distinctions, or require post hoc tuning to appear useful. Reject or retire those projections without weakening the CBF contract.

No E002 outcome authorizes Stage C automatically. A causal constitutive layer requires a new frozen experiment with equivalent-work controls and explicit safety review.

## 15. Evidence locations

- Configuration: `experiments/E002/config/`
- Raw telemetry: `experiments/E002/results/raw/`
- Run summaries: `experiments/E002/results/summary/`
- Aggregate reports: `experiments/E002/results/reports/`
- Emergent observations: `experiments/E002/observations/`

## 16. Non-claims

E002 does not claim:

- physical, pneumatic, biological, or thermodynamic equivalence;
- that pressure is information, authority, correctness, or trust;
- causal scheduling or improved workload behavior;
- conservation of semantic information;
- useful entrainment or neural-style learning;
- calibrated energy, monetary cost, or hardware-resource prediction;
- generality beyond the E001 evidence set; or
- permission to repair the full-ring boundary through hidden coordination.

## Internal references

- [CBF–Pneumatic Computation Bridge](../../docs/bridges/COMPUTATIONAL_ARCHITECTURE__BRIDGE__CBF_AND_PNEUMATIC_COMPUTATION__v0.1__2026-07-13.md)
- [Biological Pneumatic Engine paper](../../docs/whitepapers/PNEUMATIC_COMPUTATION__WHITEPAPER__BIOLOGICAL_PNEUMATIC_ENGINE__v0.1__2026-07-10.md)
- [Minimal Interlock Contract](../../specs/CBF__SPEC__MINIMAL_INTERLOCK_CONTRACT__v0.1__2026-07-10.md)
- [E001 Observation O001](../E001/observations/E001__OBSERVATION__FULL_RING_CIRCULATION_ASYMMETRY__v0.1__2026-07-14.md)
- [Research Governance](../../GOVERNANCE.md)

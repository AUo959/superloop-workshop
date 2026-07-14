# CBF–Pneumatic Computation Bridge

## A controlled synthesis for equilibrium-governed distributed computation

**Artifact class:** Computational architecture bridge  
**Version:** v0.1  
**Date:** 2026-07-13  
**Status:** Formalized research hypothesis — E1  
**Originator:** Travis Levi Streets  
**Project:** Superloop Workshop  
**Concept identifier:** `SW.BRIDGE.CBF_PNEUMATIC`

> This bridge connects two independently traceable research lines. It does not rewrite either source paper, promote the recovered Biological Pneumatic Engine into the Superloop runtime, or claim that computational pressure is physically thermodynamic.

## Abstract

The Conduit Barrier Field (CBF) proposes a computational topology composed of recurrent loops joined by regulated interlocks. Pneumatic computation proposes that pressure differentials, resistance, storage, valves, dissipation, and oscillation can perform or regulate computation. The two ideas are compatible, but they operate at different architectural levels.

This document defines their narrowest useful composition. The CBF supplies the **structural and constitutional layer**: loop identity, local closure, typed boundaries, capacity credits, validation, provenance, reciprocal obligations, and fault containment. Pneumatic computation supplies a candidate **constitutive and dynamical layer**: measurable potentials, conductance, backpressure, compliant storage, damping, phase, and flow-dependent cost. An interlock remains a semantic and safety boundary even when pneumatic variables influence how quickly it conducts.

The combined architecture is a field of recurrent units in which eligible work moves according to local gradients while ineligible work is blocked by hard contracts. Computational cost can then be studied as both resource expenditure and field occupancy over time. This is a formal sketch, not a demonstrated advantage. Its purpose is to establish equations, non-equivalences, failure modes, and falsifiable hypotheses for simulation.

## 1. Source identities and bridge boundary

### 1.1 Conduit Barrier Field

The [CBF white paper](../whitepapers/COMPUTATIONAL_ARCHITECTURE__WHITEPAPER__CONDUIT_BARRIER_FIELD__v0.1__2026-07-10.md) defines:

- a **Conduit Barrier Loop (CBL)** as a recurrent unit with local identity, state, capacity, invariants, and ports;
- an **interlock** as a stateful junction that validates, admits, accounts for, and returns feedback about transfers; and
- a **field** as a topology of interlocking loops whose local rules produce distributed workload regulation, boundary formation, and recovery.

CBF pressure is presently an architectural variable: a representation of demand relative to capacity or another locally meaningful disequilibrium. It is not yet tied to one constitutive equation.

### 1.2 Pneumatic computation and the recovered engine

The [Biological Pneumatic Engine paper](../whitepapers/PNEUMATIC_COMPUTATION__WHITEPAPER__BIOLOGICAL_PNEUMATIC_ENGINE__v0.1__2026-07-10.md) documents a recovered dialogue-processing prototype with five candidate mechanisms:

- pressure-gradient flow across a node hierarchy;
- attention-weighted valve behavior;
- pneumatic Boolean gates;
- respiratory-phase modulation; and
- dialogue-rhythm entrainment.

The prototype also provides important negative evidence. Its external and fallback implementations are not behaviorally equivalent; its logic gates are not connected to the integrator; most respiratory state is diagnostic rather than causal; and its wall-clock delays conflate simulation with execution. Those limitations are part of what this bridge inherits as design guidance.

### 1.3 Disposition decision

For Superloop Workshop, the Biological Pneumatic Engine is:

1. a **research precedent** showing one executable interpretation of computational pressure and rhythm;
2. a **source of candidate constitutive mechanisms** to isolate and test; and
3. a **failure record** demonstrating the need for dimensional definitions, implementation parity, simulated time, and causal wiring.

It is not:

- the local runtime of a CBL;
- a required dependency of the field;
- a validated biological model;
- evidence of a performance advantage; or
- authority for Superloop architecture.

## 2. Correspondence classification

The bridge uses four relationship classes. “Exact” means the two source lines already require the same abstract function, not that their implementations or physical meanings are identical.

### 2.1 Exact structural correspondences

| CBF function | Pneumatic function | Shared abstraction |
| --- | --- | --- |
| Bounded loop capacity | Finite vessel or line capacity | Local state cannot grow without limit |
| Interlock admission state | Valve aperture state | A relationship can resist or permit transfer |
| Capacity credit | Receiving headroom | Downstream capacity constrains upstream release |
| Backpressure | Reverse or opposing pressure signal | Congestion propagates feedback toward its source |
| Loop or conduit occupancy | Stored fluid quantity | Work can occupy a bounded region over time |
| Interlock resistance | Flow resistance | Equal driving potential may produce unequal transfer rates |
| Local phase variable | Oscillator phase | Recurrent units can coordinate without a universal clock |
| Isolation state | Closed isolation valve | A region can be disconnected without stopping the whole field |

These are exact only at the level of system role. A software credit is not a gas volume, and a validation state is richer than a physical valve position.

### 2.2 Useful analogies

- **Loop as compliant reservoir.** A loop can absorb a bounded disturbance and release it later, but its internal state may be structured, typed, and non-fungible.
- **Interlock as valve.** Conductance can vary continuously, while authorization and safety remain discrete.
- **Workload as pressure.** Demand relative to available capacity can generate a local potential, but urgency, uncertainty, trust, and congestion should not be collapsed into one scalar without evidence.
- **Execution as flow.** Admitted work advances through relationships, although semantic transformation may create or destroy representations rather than conserve them.
- **Coordination as entrainment.** Neighboring loops may synchronize phase when useful, but phase agreement does not imply correctness.
- **Compute cost as dissipation.** Resistance and repeated transitions consume resources, but useful irreversible computation and waste must be measured separately.

### 2.3 Speculative extensions introduced by this bridge

- A field may expose capacity as **habitable computational space**, allocated through local credits rather than one global scheduler.
- Interlock conductance may adapt from observed flow and recovery while hard admission invariants remain fixed.
- Phase coupling may lower coordination overhead for cyclic workloads without imposing global barriers.
- Occupancy-time may become a substrate-independent component of compute accounting.
- Mixed discrete–continuous simulation may reveal operating regimes that queue-only models do not expose.

### 2.4 Contradictions and non-equivalences

1. **Validation is not pressure.** Schema compatibility, authorization, provenance, and prohibited-state rules are predicates. A high gradient cannot override them.
2. **Information is not generally conserved.** It may be copied, compressed, summarized, transformed, or discarded. The conserved quantities must instead be named explicitly, such as capacity credit, resource occupancy, authority, or outstanding obligation.
3. **A CBF is not a processing chain.** The recovered engine uses an ordered five-node hierarchy; a field may contain cycles, branches, heterogeneous loops, and changing neighborhoods.
4. **Stable equilibrium is not necessarily correct.** A field can settle into deadlock, collusion, starvation, or a semantically invalid state.
5. **Attention is not authorization.** A soft attention weight may influence conductance but cannot serve as an access-control decision.
6. **Biological rhythm is not a universal scheduler.** Respiratory or conversational phase may inspire an oscillator, but Superloop must justify every coupling through workload evidence.
7. **Pneumatic latency is not execution latency.** A modeled delay is an experimental variable. Real wall-clock performance must be measured independently.
8. **Physical universality does not imply architectural advantage.** Pneumatic logic can implement Boolean operations, but that fact alone does not show that a pneumatic field outperforms ordinary software.

## 3. Combined architectural model

### 3.1 Layer separation

The proposed architecture has four layers:

1. **Constitutional layer — hard.** Identity, authorization, schema, provenance, bounded capacity, prohibited states, leases, and reciprocal obligations.
2. **Transactional layer — discrete.** Proposal, reservation, validation, commit, acknowledgment, release, revision, rejection, isolation, and expiry.
3. **Constitutive layer — measurable and replaceable.** Potential, storage, conductance, resistance, damping, phase, and flow rules.
4. **Adaptive layer — soft and optional.** Local updates to permeability, routing preference, or phase coupling within hard bounds.

This separation is the bridge’s main safety condition. Pneumatic dynamics may select among already permissible transitions. They may not make an impermissible transition valid.

### 3.2 Loop state

For loop `i`, define the state at simulation step `t` as:

```text
L_i(t) = {
  identity_i,
  x_i(t),            semantic/local computational state
  q_i(t),            occupied work capacity
  C_i,               declared capacity, with 0 <= q_i <= C_i
  phi_i(t),          phase
  mode_i(t),         normal | degraded | isolated | terminal
  obligations_i(t), outstanding reciprocal commitments
  ports_i
}
```

The field must be able to operate with the pneumatic variables disabled. This makes the constitutive layer testable against a simpler queue-and-credit baseline.

### 3.3 Interlock state

For an interlock from loop `i` to loop `j`:

```text
I_ij(t) = {
  contract_ij,       minimal interlock contract
  aperture_ij(t),    hard admissibility: 0 or 1
  credit_ij(t),      receiver-granted bounded capacity
  k_ij(t),           soft permeability within declared bounds
  R_ij(t),           effective resistance, R_ij > 0
  f_ij(t),           committed flow rate
  lease_ij(t),
  receipt_ij(t),
  phase_offset_ij(t)
}
```

`aperture_ij` becomes 1 only after identity, schema, provenance, lease, and validation requirements are satisfied. `k_ij` can influence the rate of a permitted transfer but cannot open a closed aperture.

### 3.4 Potential and pressure

The first implementation should avoid one overloaded pressure number. It should retain a typed pressure vector:

```text
p_i(t) = [congestion, urgency, uncertainty, verification_debt]
```

Each experiment declares a projection `U(p_i)` that produces a scalar transport potential only for a specific flow policy. A minimal congestion potential is:

```text
U_i(t) = q_i(t) / C_i
```

where `0 <= U_i <= 1`. Other components may influence scheduling or validation separately. Trust and authorization must never be reduced to transport potential.

### 3.5 Candidate flow law

For a permitted direction `i -> j`, define an unconstrained candidate flow:

```text
f*_ij(t) = aperture_ij(t) * k_ij(t) * max(U_i(t) - U_j(t), 0) / R_ij(t)
```

The committed rate is bounded by the sender’s transferable occupancy, the receiver’s credit, and the interlock rate limit:

```text
f_ij(t) = min(
  f*_ij(t),
  transferable_i(t) / dt,
  credit_ij(t) / dt,
  rate_limit_ij
)
```

This is a candidate constitutive law, not a final definition. E001 should begin with discrete unit transfers. The continuous form should be introduced only after the discrete contract is validated, so that any added value can be measured.

### 3.6 Storage and continuity

For a fungible occupancy quantity:

```text
q_i(t + dt) = q_i(t)
              + dt * sum_j f_ji(t)
              - dt * sum_j f_ij(t)
              + admitted_i(t)
              - resolved_i(t)
              - expired_i(t)
```

Every term must be recorded in the trace. Semantic state `x_i` follows its own typed transition function and is not presumed conserved. Credits, authority, and reciprocal obligations each require separate ledgers so a transfer cannot silently duplicate rights or erase debt.

### 3.7 Barrier–conduit transaction

Every consequential transfer follows this sequence:

1. **Propose.** The sender presents typed state, provenance, requested capacity, and an idempotence key.
2. **Reserve.** The receiver grants bounded credit with a freshness lease.
3. **Validate.** Hard predicates determine whether the aperture may open.
4. **Conduct.** The constitutive law determines the rate of the permitted transfer.
5. **Commit.** Sender, interlock, and receiver record one causally linked transition.
6. **Reciprocate.** The receiver returns acknowledgment, revision, rejection, or an explicit continuing obligation.
7. **Release.** Credits and temporary reservations are consumed, renewed, or returned.

The interlock is a barrier during steps 1–3 and a conduit during step 4. Its continuing receipt and obligation state make feedback part of the transfer rather than an optional message sent afterward.

## 4. Field thermodynamics as operating behavior

### 4.1 Distributed scheduling

Ordinary work is scheduled by local eligibility and gradient rather than a central assignment queue. Loops advertise bounded headroom. Interlocks admit only fresh, validated proposals. Congestion raises local resistance or withdraws credit, which propagates backpressure. A central service may still exist for observation, bootstrapping, or workloads that require global knowledge, but it is not assumed to authorize every transition.

### 4.2 Computational space and occupancy cost

The idea that future compute cost may reflect “space in the field” becomes testable through occupancy-time. For an experiment lasting `T`, define:

```text
space_time = integral_0^T sum_i q_i(t) dt
```

A broader cost functional may be:

```text
J = alpha * space_time
  + beta  * integral_0^T sum_(i,j) R_ij(t) * f_ij(t)^2 dt
  + gamma * coordination_events
  + delta * unresolved_obligation_time
  + penalties(invariant_violations)
```

The terms represent occupied capacity, resistive work or dissipation, coordination overhead, and feedback debt. Coefficients must be declared before a comparison. A lower `J` is meaningful only when the configurations resolve equivalent workloads and satisfy the same correctness predicates.

### 4.3 Damping, hysteresis, and metastability

Pure gradient following can oscillate when gates open and close near a threshold. Each adaptive interlock therefore needs bounded rate-of-change, hysteresis, or a minimum dwell time. A useful field may remain metastable—continually processing disturbances without converging to rest. Stability metrics must distinguish productive bounded motion from circular wait or uncontrolled oscillation.

### 4.4 Phase and entrainment

Each loop may expose phase `phi_i`. For workloads with cyclic exchange, neighboring loops may adjust toward a bounded phase relationship. Entrainment is optional and local. It must not become a hidden global clock, and phase agreement must not satisfy validation. The recovered engine’s dialogue-rhythm mechanism is a precedent for gradual coupling; its biological framing is not imported.

## 5. Neural-style operations

The combined field can support neural-style computation without treating the architecture as a conventional neural network.

- Loop state can act as a recurrent activation or local memory.
- Interlock permeability can act as a bounded, typed relation weight.
- Neighbor pressure and receipts can provide local error or constraint signals.
- Field relaxation can compute a fixed point or a stable orbit.
- A nudged condition can alter local targets and produce a measurable response.

Learning is permitted only in soft parameters such as `k_ij`, routing preference, damping, or phase coupling. Identity, authorization, provenance, capacity ceilings, prohibited states, and acceptance predicates remain non-learned. Any learning rule must be tested for feedback capture, starvation, topology gaming, and convergence to false equilibrium.

## 6. Failure modes introduced or sharpened by the bridge

| Failure mode | Bridge mechanism | Required observation or control |
| --- | --- | --- |
| Pressure laundering | Invalid work is made to appear admissible through high urgency or low congestion | Hard predicates evaluated independently of potential |
| Credit–flow mismatch | Continuous flow exceeds discrete reservation | Atomic credit ledger and rate cap |
| Numerical instability | Step size or stiffness produces artificial oscillation | Fixed-step sensitivity tests and stable integration |
| Hidden duplication | Semantic state copies while occupancy appears conserved | Separate authority, provenance, and obligation ledgers |
| Valve chatter | Aperture or permeability changes repeatedly near a threshold | Hysteresis and dwell time |
| Backpressure cascade | One slow loop stalls unrelated regions | Isolation, alternate routes, dependency-radius limits |
| False equilibrium | The field settles into a stable invalid state | External predicates and challenge perturbations |
| Phase capture | High-connectivity loops impose cadence on the field | Coupling bounds, degree limits, and desynchronization tests |
| Metric substitution | Low modeled dissipation is mistaken for useful computation | Equivalent-work and correctness constraints |
| Model/runtime conflation | Simulated delay is reported as measured performance | Separate simulation time, operation count, and wall time |

## 7. Falsifiable bridge hypotheses

### H1 — Bounded local admission

Under sustained burst load, receiver-issued credits and interlock rate limits keep every loop occupancy at or below declared capacity.

**Falsified if:** any reachable trace exceeds capacity or silently drops admitted work without an accountable terminal state.

### H2 — Local fault containment

Under one slow or failed neighbor, isolation and bounded dependency propagation permit unrelated loops to continue.

**Falsified if:** the local-interlock configuration stalls the full field no less often than a global barrier under the same workload.

### H3 — Constitutive-layer value

After the discrete CBF baseline is established, a calibrated pressure/resistance layer improves at least one declared overload metric—such as recovery time, rejected-work rate, or occupancy-time—without weakening correctness, boundedness, liveness, or fairness.

**Falsified if:** improvements disappear under equivalent-work controls, or the queue-and-credit baseline is equal or better at lower complexity.

### H4 — Reciprocal feedback value

Making acknowledgment and continuing obligation part of the interlock reduces stale progress and untraceable work compared with one-way message passing.

**Falsified if:** reciprocal state adds coordination cost without a measurable reduction in stale, duplicated, or provenance-incomplete transitions.

### H5 — Local entrainment value

For cyclic workloads, bounded local phase coupling reduces idle coordination events or latency variance relative to independent phases without creating global synchronization or starvation.

**Falsified if:** coupling increases tail latency, enlarges fault radius, or allows high-degree loops to capture field cadence.

### H6 — Occupancy-time accounting

Space-time plus explicit coordination and obligation costs predicts resource consumption across centralized, global-barrier, and local-field configurations more consistently than throughput alone.

**Falsified if:** the cost functional fails to track measured CPU, memory, network, or elapsed-resource use across declared scenarios.

## 8. Validation sequence

### Stage A — Discrete contract first

Use E001’s three-ring topology with integer work units, bounded queues, fixed credits, leases, receipts, and no continuous pressure law. Compare centralized scheduling, a global barrier, and local interlocks.

### Stage B — Instrumented pneumatic variables

Compute potential, resistance, candidate flow, occupancy-time, and estimated dissipation from the Stage A trace without allowing them to affect transitions. This tests whether the variables are coherent and informative before making them causal.

### Stage C — Causal constitutive layer

Allow the candidate flow law to influence permitted transfer rates. Run identical workloads, seeds, and fault schedules. Perform step-size and parameter-sensitivity analysis.

### Stage D — Storage and damping

Add compliant buffering, hysteresis, and isolation thresholds. Test burst absorption, valve chatter, backpressure cascades, and recovery.

### Stage E — Phase coupling

Introduce local oscillators only for workloads with a declared cyclic structure. Compare uncoupled, fixed-coupling, and adaptive-coupling configurations.

### Stage F — Adaptive permeability

Permit bounded updates to soft conductance. Keep hard invariants outside the learned state and inject collusion, starvation, topology, and false-equilibrium challenges.

## 9. Minimum trace schema

Every simulation transition should emit:

```text
event_id, simulation_time, configuration, scenario, seed,
loop_id, interlock_id, proposal_id, parent_event_ids,
event_type, validation_state, aperture, credit_before, credit_after,
occupancy_before, occupancy_after, potential_before, potential_after,
permeability, resistance, candidate_flow, committed_flow,
lease_state, obligation_created, obligation_resolved,
provenance_complete, invariant_checks, terminal_reason
```

Wall time and host-resource measurements belong in a separate execution record. This prevents simulated pneumatic time from being confused with implementation performance.

## 10. Promotion and rejection criteria

The bridge may advance beyond E1 only when:

- the combined model is implemented independently of the recovered engine;
- each parameter has a definition, unit or normalization, and valid range;
- the discrete baseline and pneumatic variant process equivalent workloads;
- raw traces reproduce all reported metrics;
- failure and sensitivity tests are preserved; and
- at least one bridge hypothesis survives its declared falsification test.

The pneumatic constitutive layer should be rejected or narrowed if it adds parameters and failure modes without measurable explanatory or operational value. Such a result would not invalidate the CBF. It would show that bounded contracts and local feedback are sufficient without a fluid dynamics layer for the tested workload.

## 11. Non-claims

This bridge does not claim:

- physical thermodynamic equivalence;
- biological fidelity, consciousness, or cognition from respiratory analogy;
- elimination of every central service;
- liveness for arbitrary topology and policy;
- conservation of information as a general law;
- superiority over actors, queues, dataflow, Petri nets, or centralized schedulers;
- infinite scalability; or
- that field occupancy replaces monetary or physical resource cost.

It claims only that the CBF and pneumatic computation can be composed coherently if their architectural levels remain separate, their shared variables become measurable, and the resulting system is compared against simpler alternatives.

## 12. Bridge conclusion

The CBF and pneumatic computation meet most cleanly at the interlock. The CBF says what a relationship is allowed to do, what it must remember, and what feedback it owes. The pneumatic layer proposes how quickly an allowed relationship conducts, how congestion resists it, how capacity stores it, and how neighboring cycles may coordinate.

That division preserves the central image of interlocking rings of light without asking the image to serve as proof. The field is a barrier because every consequential transition encounters a local constitution. It is a conduit because the same interlocks expose capacity and carry validated state. Its “thermodynamics” become engineering only when pressure, flow, resistance, storage, phase, and dissipation are explicit variables in reproducible traces.

The next step is E001: validate the discrete barrier–conduit contract first, instrument pneumatic quantities second, and make those quantities causal only after they demonstrate value.

## Internal references

- [The Conduit Barrier Field v0.1](../whitepapers/COMPUTATIONAL_ARCHITECTURE__WHITEPAPER__CONDUIT_BARRIER_FIELD__v0.1__2026-07-10.md)
- [The Biological Pneumatic Engine v0.1](../whitepapers/PNEUMATIC_COMPUTATION__WHITEPAPER__BIOLOGICAL_PNEUMATIC_ENGINE__v0.1__2026-07-10.md)
- [Minimal Interlock Contract v0.1](../../specs/CBF__SPEC__MINIMAL_INTERLOCK_CONTRACT__v0.1__2026-07-10.md)
- [Research Governance](../../GOVERNANCE.md)
- [Research Roadmap](../../ROADMAP.md)


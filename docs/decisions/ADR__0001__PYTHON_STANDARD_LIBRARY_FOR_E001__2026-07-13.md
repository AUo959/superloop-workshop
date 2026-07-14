# ADR 0001 — Python standard library for E001

**Date:** 2026-07-13  
**Status:** Trial  
**Decision owner:** Travis Levi Streets  
**Affected experiment:** `SW.EXPERIMENT.E001`

## Context

E001 needs a deterministic discrete-event simulator before Superloop Workshop has evidence for a permanent runtime or substrate. The implementation must compare three coordination models under identical workloads, emit reconstructable traces, separate simulated time from wall-clock execution, and remain easy to replace if the experiment exposes a better representation.

The runtime decision must serve the experiment without becoming an architectural claim about Superloop itself.

## Decision drivers

- Deterministic execution and explicit ordering
- Minimal setup and no third-party runtime dependency
- Readable state-transition code suitable for architectural review
- Native support for structured data, queues, priority events, JSON Lines, and unit tests
- Compatibility with the repository's existing integrity workflow
- Fast iteration while the model is still expected to change
- Straightforward portability of traces and experiment configurations

## Options considered

### Python 3.13 standard library

Python provides dataclasses, enumerations, deterministic collection handling, `heapq`, JSON serialization, command-line parsing, and `unittest` without external packages. It favors inspection and experimentation over maximum throughput or compile-time guarantees.

### Rust

Rust would provide strong type and ownership guarantees and a credible path toward high-performance simulation. Its additional implementation ceremony would slow the first formal sketch, and those guarantees are not yet the principal variable under test.

### TypeScript and Node.js

TypeScript would provide accessible typed models and a natural path to browser visualization. Its runtime and package-management surface would add dependencies before the state model has stabilized.

### Formal modeling tool first

TLA+, a Petri-net tool, or a model checker could strengthen invariant analysis. Starting there would not replace the need for comparative traces and measured workload behavior. Formal verification remains a later complementary lane.

## Decision

E001 Stage A will use **Python 3.13 and the Python standard library only**.

The trial implementation will:

- live under `src/superloop_e001/`;
- use `unittest` under `tests/`;
- use integer simulation ticks, never sleeps or wall-clock time, for modeled behavior;
- write canonical JSON Lines transition traces and JSON summaries;
- accept an explicit configuration and seed;
- keep scheduler implementations interchangeable behind one experiment interface; and
- avoid NumPy, SimPy, pandas, plotting libraries, and external runtime services in Stage A.

Python is an experimental instrument here, not the Superloop substrate. Later stages may replay the same canonical inputs and compare traces from another implementation.

## Consequences

### Expected benefits

- The first model can remain small, inspectable, and dependency-free.
- CI and local execution require no package installation.
- Every transition can be serialized directly from the model state.
- A second implementation can treat E001 traces as a behavioral comparison target.

### Costs and risks

- Python's dynamic typing permits classes of mistakes that a stricter compiler might prevent.
- Interpreter performance may eventually constrain large parameter sweeps.
- Floating-point constitutive models may require stricter numerical controls in later stages.
- Convenience could encourage the prototype to become a permanent runtime without evidence.

## Validation and reversal

This trial is successful if the Stage A implementation is deterministic, dependency-free, readable, and fast enough to execute the frozen E001 matrix in ordinary CI.

The decision should be revisited if:

- repeated runs produce different canonical traces;
- the full matrix cannot complete within the declared CI budget;
- the state model becomes unsafe or opaque without stronger type guarantees;
- another implementation exposes an ambiguity hidden by Python; or
- a later physical or distributed substrate requires different semantics.

## Independence and provenance

This decision does not import Aurora modules, runtime conventions, or canonical code. Python is selected as a general experimental tool. The recovered Biological Pneumatic Engine is not a dependency and will not be copied into E001.

## Links

- [E001 experiment specification](../../experiments/E001/EXPERIMENT__E001__THREE_RING_BOUNDED_FLOW__v0.1__2026-07-13.md)
- [Minimal Interlock Contract](../../specs/CBF__SPEC__MINIMAL_INTERLOCK_CONTRACT__v0.1__2026-07-10.md)

